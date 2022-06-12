"""Command line setup."""
from typing import Optional

from pathlib import Path

import rich_click as click

from cookie_composer.commands.create import create_cmd


@click.group()
def cli():
    """Rendering templates using composition."""
    pass


@cli.command()
@click.argument("path_or_url", type=str, required=True)
@click.argument(
    "output_dir",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
)
def create(path_or_url: str, output_dir: Optional[Path]):
    """
    Create a project from a template or configuration.

    Args:
        path_or_url: The path or URL to the template or composition file
        output_dir: Where to write the output
    """
    create_cmd(path_or_url, output_dir)


@cli.command()
@click.argument("path_or_url", type=str, required=True)
def add(path_or_url: str):
    """
    Add a template or configuration to an existing project.

    Args:
        path_or_url: A URL or string to add the template or configuration
    """


@cli.command()
def update():
    """
    Update the project to the latest version of each template.
    """
