"""Command line setup."""
from typing import Optional

import logging
from pathlib import Path

import click_log
import rich_click as click

from cookie_composer.commands.add import add_cmd
from cookie_composer.commands.create import create_cmd
from cookie_composer.exceptions import GitError

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
def cli():
    """Rendering templates using composition."""
    pass


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use cookiecutter.json file content. "
    "Defaults to deleting any cached resources and redownloading them.",
)
@click.option(
    "-c",
    "--checkout",
    help="branch, tag or commit to checkout after git clone",
)
@click.option(
    "--directory",
    help="Directory within repo that holds cookiecutter.json file "
    "for advanced repositories with multi templates in it",
)
@click.option(
    "-f",
    "--overwrite-if-exists",
    is_flag=True,
    help="Overwrite the contents of the output directory if it already exists",
)
@click.option(
    "-s",
    "--skip-if-file-exists",
    is_flag=True,
    help="Skip the files in the corresponding directories if they already exist",
    default=False,
)
@click.option(
    "--default-config",
    is_flag=True,
    help="Do not load a config file. Use the defaults instead",
)
@click.argument("path_or_url", type=str, required=True)
@click.argument(
    "output_dir",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
)
def create(
    no_input: bool,
    checkout: str,
    directory: str,
    overwrite_if_exists: bool,
    skip_if_file_exists: bool,
    default_config: bool,
    path_or_url: str,
    output_dir: Optional[Path],
):
    """Create a project from a template or configuration."""
    create_cmd(
        path_or_url,
        output_dir,
        no_input,
        checkout,
        directory,
        overwrite_if_exists,
        skip_if_file_exists,
        default_config,
    )


@cli.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use cookiecutter.json file content. "
    "Defaults to deleting any cached resources and redownloading them.",
)
@click.option(
    "-c",
    "--checkout",
    help="branch, tag or commit to checkout after git clone",
)
@click.option(
    "--directory",
    help="Directory within repo that holds cookiecutter.json file "
    "for advanced repositories with multi templates in it",
)
@click.option(
    "-f",
    "--overwrite-if-exists",
    is_flag=True,
    help="Overwrite the contents of the output directory if it already exists",
)
@click.option(
    "-s",
    "--skip-if-file-exists",
    is_flag=True,
    help="Skip the files in the corresponding directories if they already exist",
    default=False,
)
@click.option(
    "--default-config",
    is_flag=True,
    help="Do not load a config file. Use the defaults instead",
)
@click.argument("path_or_url", type=str, required=True)
@click.argument(
    "destination", required=False, type=click.Path(exists=True, file_okay=False, writable=True, path_type=Path)
)
def add(
    no_input: bool,
    checkout: str,
    directory: str,
    overwrite_if_exists: bool,
    skip_if_file_exists: bool,
    default_config: bool,
    path_or_url: str,
    destination: Optional[Path],
):
    """Add a template or configuration to an existing project."""
    destination = destination or Path(".")
    try:
        add_cmd(path_or_url, destination, no_input=no_input)
    except GitError as e:
        raise click.UsageError(str(e)) from e


@cli.command()
def update():
    """
    Update the project to the latest version of each template.
    """
    pass


@cli.command()
@click.argument("path_or_url", type=str, required=True)
def link():
    """Link an existing project to a template or composition."""
    pass

if __name__ == '__main__':
    cli()
