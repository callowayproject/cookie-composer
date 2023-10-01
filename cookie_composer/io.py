"""Functions for handling input/output operations."""
import copy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional, Union

import fsspec
from cookiecutter.config import get_user_config

from cookie_composer.composition import Composition, RenderedComposition, logger
from cookie_composer.data_merge import comprehensive_merge
from cookie_composer.exceptions import MissingCompositionFileError
from cookie_composer.layers import LayerConfig, RenderedLayer
from cookie_composer.templates.types import Template


def serialize_layer(layer: LayerConfig) -> dict:
    """Serialize the layer configuration for outputting in a rendered layer."""
    layer_info = layer.model_dump(exclude={"template"})
    layer_info.update(
        {
            "template": layer.template.repo.source,
            "directory": layer.template.directory,
            "checkout": layer.template.repo.checkout,
            "password": layer.template.repo.password,
        }
    )
    return layer_info


def deserialize_layer(layer_info: dict, local_path: Optional[Path] = None, **kwargs) -> LayerConfig:
    """Deserialize a layer configuration from a rendered layer."""
    from cookie_composer.templates.source import get_template_repo

    layer_info = copy.deepcopy(layer_info)
    if kwargs:
        layer_info = comprehensive_merge(layer_info, kwargs)

    template = Template(
        repo=get_template_repo(
            url=layer_info.pop("template"),
            local_path=local_path,
            checkout=layer_info.pop("checkout", None),
            password=layer_info.pop("password", None),
        ),
        directory=layer_info.pop("directory", ""),
    )
    initial_context = layer_info.pop("context", {})  # Context from the composition file
    extra_context = kwargs.get("extra_context", {})  # Context from the command line
    layer_info["initial_context"] = comprehensive_merge(initial_context, extra_context)
    layer_info["template"] = template
    return LayerConfig(**layer_info)


def serialize_rendered_layer(rendered_layer: RenderedLayer) -> dict:
    """Serialize a rendered layer for output."""
    layer_info = serialize_layer(rendered_layer.layer)
    del layer_info["initial_context"]
    layer_info["commit"] = rendered_layer.rendered_commit
    layer_info["context"] = rendered_layer.rendered_context
    layer_info["rendered_name"] = rendered_layer.rendered_name
    return layer_info


def deserialize_rendered_layer(rendered_layer_info: dict, location: Path) -> RenderedLayer:
    """
    Deserialize a rendered layer from output.

    Args:
        rendered_layer_info: A dictionary containing the rendered layer information
        location: The location of the rendered layer, typically the
            parent directory of the parent directory of the .composition.yaml file

    Returns:
        A rendered layer object
    """
    layer_info = copy.deepcopy(rendered_layer_info)
    rendered_layer = {
        "rendered_context": layer_info["context"],
        "rendered_commit": layer_info.pop("commit"),
        "location": location,
    }
    if "rendered_name" in layer_info:
        rendered_layer["rendered_name"] = layer_info.pop("rendered_name")

    return RenderedLayer(
        layer=deserialize_layer(layer_info, local_path=location),
        **rendered_layer,
    )


def serialize_composition(layers: List[LayerConfig]) -> List[dict]:
    """Serialize a composition for output."""
    return [serialize_layer(layer) for layer in layers]


def deserialize_composition(composition_info: List[dict], local_path: Optional[Path] = None, **kwargs) -> Composition:
    """Deserialize a composition from output."""
    return Composition(
        layers=[deserialize_layer(layer_info, local_path=local_path, **kwargs) for layer_info in composition_info]
    )


def serialize_rendered_composition(composition: RenderedComposition) -> List[dict]:
    """Serialize a rendered composition for output."""
    return [serialize_rendered_layer(layer) for layer in composition.layers]


def deserialize_rendered_composition(composition_info: List[dict], location: Path) -> RenderedComposition:
    """Deserialize a rendered composition from output."""
    rendered_name = composition_info[0]["rendered_name"]
    return RenderedComposition(
        layers=[deserialize_rendered_layer(layer_info, location) for layer_info in composition_info],
        render_dir=location.parent,
        rendered_name=rendered_name,
    )


def read_yaml(path_or_url: Union[str, Path]) -> List[dict]:
    """Read a YAML file and return a list of dictionaries."""
    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    try:
        of = fsspec.open(path_or_url, mode="rt")
        with of as f:
            return list(yaml.load_all(f))
    except FileNotFoundError as e:
        raise MissingCompositionFileError(str(path_or_url)) from e


def write_yaml(path: Path, contents: List[dict]) -> None:
    """Write a YAML file."""
    import fsspec
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    of = fsspec.open(str(path), mode="wt")
    with of as f:
        yaml.dump_all(contents, f)


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
    """
    of = fsspec.open(path_or_url, mode="rt")
    contents: List[dict] = read_yaml(path_or_url)
    if of.fs.fsid == "local":
        return deserialize_composition(contents, local_path=Path(path_or_url).parent, **kwargs)
    return deserialize_composition(contents, **kwargs)


def read_rendered_composition(path: Path) -> RenderedComposition:
    """
    Read a ``.composition.yaml`` from a rendered project.

    Args:
        path: The path to the .composition.yaml file to read

    Returns:
        The rendered composition information
    """
    path = path.expanduser().resolve()
    contents = read_yaml(path)
    return deserialize_rendered_composition(contents, path.parent)


def write_rendered_composition(composition: RenderedComposition) -> None:
    """
    Write the composition file using the rendered layers to the appropriate place.

    Args:
        composition: The rendered composition object to export
    """
    composition_info = serialize_rendered_composition(composition)
    composition_file = composition.render_dir / composition.rendered_name / ".composition.yaml"
    logger.debug(f"Writing rendered composition to {composition_file}")
    write_yaml(composition_file, composition_info)


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
    get_user_config()

    if is_composition_file(path_or_url):
        composition = read_composition(
            path_or_url=path_or_url,
            checkout=checkout,
            no_input=no_input or default_config,
            skip_if_file_exists=skip_if_file_exists,
            extra_context=initial_context or {},
        )
        logger.info(f"Rendering composition {path_or_url} to {output_dir}.")
    else:
        template_info = {
            "template": path_or_url,
            "directory": directory,
            "checkout": checkout,
            "password": None,
            "no_input": no_input or default_config,
            "skip_if_file_exists": skip_if_file_exists,
            "overwrite": ["*"] if overwrite_if_exists else [],
            "context": initial_context or {},
        }
        composition = Composition(layers=[deserialize_layer(template_info)])
        logger.info(f"Rendering template {path_or_url} to {output_dir}.")
    return composition
