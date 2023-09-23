"""Project configuration and options."""
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, MutableMapping, Optional, Union

from pydantic import BaseModel, DirectoryPath, Field, root_validator

from cookie_composer.data_merge import comprehensive_merge
from cookie_composer.exceptions import GitError, MissingCompositionFileError
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
    template: str
    """The path or URL to the template."""

    directory: Optional[str] = None
    """Directory within a git repository template that holds the cookiecutter.json file."""

    checkout: Optional[str] = None
    """The branch, tag or commit to tell Cookie Cutter to use."""

    password: Optional[str] = None
    """The password to use if template is a password-protected Zip archive."""

    commit: Optional[str] = None
    """What git hash was applied if the template is a git repository."""

    #
    # Input specification
    #
    no_input: bool = False
    """Do not prompt for parameters and only use cookiecutter.json file content.

    This is only used for initial generation. After initial generation, the results
    are stored in the context."""

    context: MutableMapping[str, Any] = Field(default_factory=dict)
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

    @property
    def layer_name(self) -> str:
        """The name of the template layer."""
        from cookie_composer.utils import get_template_name

        return get_template_name(str(self.template), self.directory, self.checkout)


class RenderedLayer(BaseModel):
    """Information about a rendered layer."""

    layer: LayerConfig
    """The original layer configuration that was rendered."""

    location: DirectoryPath
    """The directory where the layer was rendered."""

    new_context: MutableMapping[str, Any]
    """The context based on questions asked."""

    latest_commit: Optional[str] = None
    """The latest commit checked out if the layer source was a git repo."""

    rendered_name: Optional[str] = None
    """The name of the rendered template directory."""

    @root_validator(pre=True)
    def set_rendered_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:  # noqa: N805
        """Set the :attr:`~.RenderedLayer.layer_name`` to the name of the rendered template directory."""
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

    def latest_template_sha(self) -> Optional[str]:
        """
        Return the latest SHA of this rendered layer's template.

        If the template is not a git repository, it will always return ``None``.

        Returns:
            The latest hexsha of the template or ``None`` if the template isn't a git repo
        """
        from cookiecutter.config import get_user_config
        from cookiecutter.repository import determine_repo_dir

        from cookie_composer.git_commands import get_repo

        user_config = get_user_config(config_file=None, default_config=False)
        repo_dir, _ = determine_repo_dir(
            template=self.layer.template,
            abbreviations=user_config["abbreviations"],
            clone_to_dir=user_config["cookiecutters_dir"],
            checkout=self.layer.commit or self.layer.checkout,
            no_input=self.layer.no_input,
            password=self.layer.password,
            directory=self.layer.directory,
        )
        try:
            template_repo = get_repo(repo_dir, search_parent_directories=True)
            return template_repo.head.object.hexsha
        except GitError:
            # It probably isn't a git repository
            return None


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

    @property
    def layer_names(self) -> List[str]:
        """Return a list of the names of all the layers."""
        return [x.layer.layer_name for x in self.layers]


def is_composition_file(path_or_url: Union[str, Path]) -> bool:
    """
    Return ``True`` if the filename a composition file.

    Args:
        path_or_url: The path or URL to check

    Returns:
        ``True`` if the path is a configuration file.
    """
    return Path(path_or_url).suffix in {".yaml", ".yml"}


def read_composition(path_or_url: Union[str, Path], **kwargs) -> Composition:
    """
    Read a YAML file and return a :class:`~.Composition`.

    Args:
        path_or_url: The location of the configuration file
        **kwargs: Additional keyword arguments passed to the composition

    Returns:
        A composition

    Raises:
        MissingCompositionFileError: Raised when it can not access the configuration file.
    """
    import urllib.parse

    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    try:
        of = fsspec.open(path_or_url, mode="rt")
        with of as f:
            contents = list(yaml.load_all(f))
            templates = []
            for doc in contents:
                new_doc = comprehensive_merge(doc, kwargs)
                templates.append(LayerConfig(**new_doc))

        for tmpl in templates:
            tmpl.template = urllib.parse.urljoin(str(path_or_url), str(tmpl.template))

        return Composition(layers=templates)
    except FileNotFoundError as e:
        raise MissingCompositionFileError(str(path_or_url)) from e


def read_rendered_composition(path: Path) -> RenderedComposition:
    """
    Read a ``.composition.yaml`` from a rendered project.

    Args:
        path: The path to the .composition.yaml file to read

    Returns:
        The rendered composition information
    """
    path = path.resolve()
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
        render_dir=path.parent.parent,
        rendered_name=path.parent.name,
    )


def write_composition(layers: List[LayerConfig], destination: Union[str, Path]) -> None:
    """
    Write a YAML composition file.

    Args:
        layers: The layers of the composition
        destination: Where to write the file
    """
    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    of = fsspec.open(destination, mode="wt")
    dict_layers = [layer.dict() for layer in layers]
    with of as f:
        yaml.dump_all(dict_layers, f)


def write_rendered_composition(composition: RenderedComposition) -> None:
    """
    Write the composition file using the rendered layers to the appropriate place.

    Args:
        composition: The rendered composition object to export
    """
    layers = [rendered_layer.layer for rendered_layer in composition.layers]
    composition_file = composition.render_dir / composition.rendered_name / ".composition.yaml"
    logger.debug(f"Writing rendered composition to {composition_file}")
    write_composition(layers, composition_file)


def get_merge_strategy(path: Path, merge_strategies: Dict[str, str]) -> str:
    """
    Return the merge strategy of the path based on the layer configured rules.

    Files that are not mergable return :attr:`~cookie_composer.composition.DO_NOT_MERGE`

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


def get_composition_from_path_or_url(
    path_or_url: str,
    checkout: Optional[str] = None,
    default_config: bool = False,
    directory: Optional[str] = None,
    no_input: bool = False,
    output_dir: Optional[Path] = None,
    overwrite_if_exists: bool = False,
    skip_if_file_exists: bool = False,
    initial_context: Optional[MutableMapping[str, Any]] = None,
) -> Composition:
    """
    Generate a :class:`Composition` from a path or URL.

    Args:
        path_or_url: The path or url to the composition file or template
        checkout: The branch, tag or commit to check out after git clone
        default_config: Do not load a config file. Use the defaults instead
        directory: Directory within repo that holds cookiecutter.json file
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        output_dir: Where to generate the project
        overwrite_if_exists: Overwrite the contents of the output directory if it already exists
        skip_if_file_exists: Skip the files in the corresponding directories if they already exist
        initial_context: The initial context for the composition

    Returns:
        The composition object.
    """
    if is_composition_file(path_or_url):
        composition = read_composition(
            path_or_url=path_or_url,
            checkout=checkout,
            no_input=no_input or default_config,
            skip_if_file_exists=skip_if_file_exists,
            context=initial_context or {},
        )
        logger.info(f"Rendering composition {path_or_url} to {output_dir}.")
    else:
        overwrite_rules = ["*"] if overwrite_if_exists else []
        tmpl = LayerConfig(
            template=path_or_url,
            directory=directory,
            checkout=checkout,
            no_input=no_input or default_config,
            skip_if_file_exists=skip_if_file_exists,
            overwrite=overwrite_rules,
            context=initial_context or {},
        )
        composition = Composition(layers=[tmpl])
        logger.info(f"Rendering template {path_or_url} to {output_dir}.")
    return composition
