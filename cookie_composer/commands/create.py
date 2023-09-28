"""Methods for generating projects."""

import logging
from pathlib import Path
from typing import Any, MutableMapping, Optional

from cookie_composer.composition import RenderedComposition
from cookie_composer.io import get_composition_from_path_or_url, write_rendered_composition
from cookie_composer.layers import render_layers

logger = logging.getLogger(__name__)


def create_cmd(
    path_or_url: str,
    output_dir: Optional[Path] = None,
    no_input: bool = False,
    checkout: Optional[str] = None,
    directory: Optional[str] = None,
    overwrite_if_exists: bool = False,
    skip_if_file_exists: bool = False,
    default_config: bool = False,
    accept_hooks: str = "all",
    initial_context: Optional[MutableMapping[str, Any]] = None,
) -> Path:
    """
    Generate a new project from a composition file, local template or remote template.

    Args:
        path_or_url: The path or url to the composition file or template
        output_dir: Where to generate the project
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        checkout: The branch, tag or commit to check out after git clone
        directory: Directory within repo that holds cookiecutter.json file
        overwrite_if_exists: Overwrite the contents of the output directory if it already exists
        skip_if_file_exists: Skip the files in the corresponding directories if they already exist
        default_config: Do not load a config file. Use the defaults instead
        accept_hooks: Which pre/post hooks should be applied?
        initial_context: The initial context for the composition

    Returns:
        The path to the generated project.
    """
    output_dir = Path(output_dir).resolve() or Path().cwd().resolve()
    composition = get_composition_from_path_or_url(
        path_or_url,
        checkout,
        default_config,
        directory,
        no_input,
        output_dir,
        overwrite_if_exists,
        skip_if_file_exists,
        initial_context or {},
    )
    rendered_layers = render_layers(composition.layers, output_dir, no_input=no_input, accept_hooks=accept_hooks)
    rendered_composition = RenderedComposition(
        layers=rendered_layers,
        render_dir=output_dir,
        rendered_name=rendered_layers[0].rendered_name,
    )
    write_rendered_composition(rendered_composition)
    return rendered_composition.render_dir / rendered_composition.rendered_name
