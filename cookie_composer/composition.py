"""Project configuration and options."""
from typing import Any, Dict, List, Optional, Union

import logging
import os
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, DirectoryPath, Field, root_validator

from cookie_composer.exceptions import MissingCompositionFileError
from cookie_composer.matching import rel_fnmatch

logger = logging.getLogger(__name__)


# Strategies merging files and data.

DO_NOT_MERGE = "do-not-merge"
"""Do not merge the data, use the file path to determine what to do."""

NESTED_OVERWRITE = "nested-overwrite"
"""Merge deeply nested structures and overwrite at the lowest level; A deep ``dict.update()``."""

OVERWRITE = "overwrite"
"""Overwrite at the top level like ``dict.update()``."""

COMPREHENSIVE = "comprehensive"
"""Comprehensively merge the two data structures.

- Scalars are overwritten by the new values
- lists are merged and de-duplicated
- dicts are recursively merged
"""


class LayerConfig(BaseModel):
    """Configuration for a layer of a composition."""

    #
    # Template specification
    #
    template: Union[str, AnyHttpUrl]
    """The path or URL to the template."""

    directory: Optional[str]
    """Directory within a git repository template that holds the cookiecutter.json file."""

    checkout: Optional[str]
    """The branch, tag or commit to use if template is a git repository.

    Also used for updating projects."""

    password: Optional[str]
    """The password to use if template is a password-protected Zip archive."""

    commit: Optional[str]
    """What git hash was applied if the template is a git repository."""

    #
    # Input specification
    #
    no_input: bool = False
    """Do not prompt for parameters and only use cookiecutter.json file content.

    This is only used for initial generation. After initial generation, the results
    are stored in the context."""

    context: Dict[str, Any] = Field(default_factory=dict)
    """Dictionary that will provide values for input.

    Also stores the answers for missing context parameters after initial generation."""

    #
    # File generation
    #
    skip_hooks: bool = False
    """Skip the template hooks."""

    skip_if_file_exists: bool = True
    """Skip the files in the corresponding directories if they already exist."""

    skip_generation: List[str] = Field(default_factory=list)
    """Paths or glob patterns to skip attempting to generate."""

    overwrite: List[str] = Field(default_factory=list)
    """Paths or glob patterns to always overwrite."""

    overwrite_exclude: List[str] = Field(default_factory=list)
    """Paths or glob patterns to exclude from overwriting."""

    merge_strategies: Dict[str, str] = Field(default_factory=lambda: {"*": DO_NOT_MERGE})
    """The method to merge specific paths or glob patterns."""


class RenderedLayer(BaseModel):
    """Information about a rendered layer."""

    layer: LayerConfig
    """The original layer configuration that was rendered."""

    location: DirectoryPath
    """The directory where the layer was rendered."""

    new_context: Dict[str, Any]
    """The context based on questions asked."""

    latest_commit: Optional[str] = None
    """The latest commit checked out if the layer source was a git repo."""

    rendered_name: Optional[str] = None
    """The name of the rendered template directory."""

    @root_validator(pre=True)
    def set_rendered_name(cls, values):
        """Set the ``layer_name`` to the name of the rendered template directory."""
        if "rendered_name" in values:
            return values

        dirs = list(os.scandir(values["location"]))
        if len(dirs) > 1:
            raise ValueError("More than one item in render location.")
        elif not dirs:
            raise ValueError("There are no items in render location.")
        if not dirs[0].is_dir():
            raise ValueError("The rendered template is not a directory.")
        values["rendered_name"] = dirs[0].name
        return values


class Composition(BaseModel):
    """Composition of templates for a project."""

    layers: List[LayerConfig]


class RenderedComposition(BaseModel):
    """A rendered composition of templates for a project."""

    layers: List[RenderedLayer]
    """Rendered layers."""

    render_dir: DirectoryPath
    """The directory in which the layers were rendered.

    The ``render_dir`` + ``rendered_name`` is the location of the project."""

    rendered_name: str
    """The name of the rendered project."""


def is_composition_file(path_or_url: Union[str, Path]) -> bool:
    """
    Is the filename a composition file?

    Args:
        path_or_url: The path or URL to check

    Returns:
        ``True`` if the path is a configuration file.
    """
    return Path(path_or_url).suffix in {".yaml", ".yml"}


def read_composition(path_or_url: Union[str, Path]) -> Composition:
    """
    Read a JSON or YAML file and return a Composition.

    Args:
        path_or_url: The location of the configuration file

    Returns:
        A project composition

    Raises:
        MissingCompositionFileError: Raised when it can not access the configuration file.
    """
    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    try:
        of = fsspec.open(path_or_url, mode="rt")
        with of as f:
            contents = list(yaml.load_all(f))
            templates = [LayerConfig(**doc) for doc in contents]
        return Composition(layers=templates)
    except (ValueError, FileNotFoundError) as e:
        raise MissingCompositionFileError(path_or_url) from e


def read_rendered_composition(path: Path) -> RenderedComposition:
    """
    Read a ``.composition.yaml`` from a rendered project.

    Args:
        path: The path to the .composition.yaml file to read

    Returns:
        The rendered composition information
    """
    composition = read_composition(path)
    rendered_layers = [
        RenderedLayer(
            layer=layer,
            location=path.parent,
            new_context=layer.context,
            latest_commit=layer.commit,
            rendered_name=path.parent.name,
        )
        for layer in composition.layers
    ]
    return RenderedComposition(
        layers=rendered_layers,
        render_dir=path.parent,
        rendered_name=path.parent.name,
    )


def write_composition(layers: List[LayerConfig], destination: Union[str, Path]):
    """
    Write a JSON or YAML composition file.

    Args:
        layers: The layers of the composition
        destination: Where to write the file
    """
    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    of = fsspec.open(destination, mode="wt")
    dict_layers = [layer.dict() for layer in layers]
    with of as f:
        yaml.dump_all(dict_layers, f)


def write_rendered_composition(composition: RenderedComposition):
    """
    Write the composition file using the rendered layers to the appropriate.

    Args:
        composition: The rendered composition object to export
    """
    layers = []
    for rendered_layer in composition.layers:
        layers.append(rendered_layer.layer)

    composition_file = composition.render_dir / composition.rendered_name / ".composition.yaml"
    write_composition(layers, composition_file)


def get_merge_strategy(path: Path, merge_strategies: Dict[str, str]) -> str:
    """
    Return the merge strategy of the path based on the layer configured rules.

    Files that are not mergable return ``DO_NOT_MERGE``

    Args:
        path: The file path to evaluate.
        merge_strategies: The glob pattern->strategy mapping

    Returns:
        The appropriate merge strategy.
    """
    from cookie_composer.merge_files import MERGE_FUNCTIONS

    strategy = DO_NOT_MERGE  # The default

    if path.suffix not in MERGE_FUNCTIONS:
        return DO_NOT_MERGE

    for pattern, strat in merge_strategies.items():
        if rel_fnmatch(str(path), pattern):
            logger.debug(f"{path} matches merge strategy pattern {pattern} for {strat}")
            strategy = strat
            break

    return strategy
