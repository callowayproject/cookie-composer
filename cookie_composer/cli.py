"""Command line setup."""
from typing import Optional

from pathlib import Path

import typer

from cookie_composer._commands import _create

app = typer.Typer()


@app.command()
def create(path_or_url: str, output_dir: Optional[Path] = None):
    """
    Create a project from a template or configuration.

    Args:
        path_or_url: The path or URL to the template or composition file
        output_dir: Where to write the output
    """
    _create.create(path_or_url, output_dir)


@app.command()
def add(path_or_url: str):
    """
    Add a template or configuration to an existing project.

    Args:
        path_or_url: A URL or string to add the template or configuration
    """


@app.command()
def update():
    """
    Update the project to the latest version of each template.
    """
