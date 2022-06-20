"""Methods for generating projects."""

from typing import Optional

import logging
from pathlib import Path

from cookie_composer.composition import (
    Composition,
    LayerConfig,
    RenderedComposition,
    is_composition_file,
    read_composition,
    write_rendered_composition,
)
from cookie_composer.layers import render_layers

logger = logging.getLogger(__name__)


def create_cmd(
    path_or_url: str,
    output_dir: Optional[Path] = None,
    no_input: bool = False,
) -> Path:
    """
    Generate a new project from a composition file, local template or remote template.

    Args:
        path_or_url: The path or url to the composition file or template
        output_dir: Where to generate the project
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``

    Returns:
        The path to the generated project.
    """
    output_dir = Path(output_dir).resolve() or Path().cwd().resolve()
    if is_composition_file(path_or_url):
        composition = read_composition(path_or_url)
        logger.info(f"Rendering composition {path_or_url} to {output_dir}.")
    else:
        tmpl = LayerConfig(template=path_or_url)
        composition = Composition(layers=[tmpl], destination=output_dir)
        logger.info(f"Rendering template {path_or_url} to {output_dir}.")
    rendered_layers = render_layers(composition.layers, output_dir, no_input=no_input)
    rendered_composition = RenderedComposition(
        layers=rendered_layers,
        render_dir=output_dir,
        rendered_name=rendered_layers[0].rendered_name,
    )
    write_rendered_composition(rendered_composition)
    return rendered_composition.render_dir / rendered_composition.rendered_name
