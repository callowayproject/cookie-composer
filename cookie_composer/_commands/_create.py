"""Methods for generating projects."""

from typing import Optional

from pathlib import Path

from cookie_composer.composition import (
    LayerConfig,
    ProjectComposition,
    is_composition_file,
    read_composition,
)
from cookie_composer.layers import process_composition


def create(
    path_or_url: str,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Generate a new project from a composition file, local template or remote template.

    Args:
        path_or_url: The path or url to the composition file or template
        output_dir: Where to generate the project

    Returns:
        The path to the generated project.
    """
    output_dir = output_dir or Path(".")
    if is_composition_file(path_or_url):
        composition = read_composition(path_or_url, output_dir)
    else:
        tmpl = LayerConfig(template=path_or_url)
        composition = ProjectComposition(layers=[tmpl], destination=output_dir)
    process_composition(composition)
    return output_dir
