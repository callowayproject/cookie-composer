"""Command line setup."""

import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any, MutableMapping, Optional

import click_log
import rich_click as click

from cookie_composer import __version__
from cookie_composer.commands.add import add_cmd
from cookie_composer.commands.authn import auth
from cookie_composer.commands.create import create_cmd
from cookie_composer.commands.link import link_cmd
from cookie_composer.commands.update import update_cmd
from cookie_composer.exceptions import GitError

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """Render templates using composition."""
    pass


cli.add_command(auth)


def validate_context_params(ctx: Any, param: Any, value: list) -> Optional[OrderedDict]:
    """
    Validate context parameters.

    Convert a tuple to a dict

     e.g.: `('program_name=foobar', 'startsecs=66')` -> `{'program_name': 'foobar', 'startsecs': '66'}`

    Arguments:
        ctx: Click context (unused)
        param: Click parameter (unused)
        value: Click parameter value

    Returns:
        An ordered dict of the parameter values or `None` if no parameters.

    Raises:
        BadParameter: If the parameters are not `key=value`.
    """
    for string in value:
        if "=" not in string:
            raise click.BadParameter(
                f"EXTRA_CONTEXT should contain items of the form key=value." f"'{string}' doesn't match that form."
            )

    return OrderedDict(s.split("=", 1) for s in value) or None


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
@click.option(
    "-d",
    "--destination",
    "-o",
    "--output-dir",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="The directory to render the templates to. Defaults to the current working directory.",
)
@click.option(
    "--accept-hooks",
    type=click.Choice(["yes", "ask", "no", "first", "last", "all", "none"], case_sensitive=False),
    default="all",
    help="Accept pre/host hooks",
)
@click.argument("path_or_url", type=str, required=True)
@click.argument("context_params", nargs=-1, callback=validate_context_params)
def create(
    no_input: bool,
    checkout: str,
    directory: str,
    overwrite_if_exists: bool,
    skip_if_file_exists: bool,
    default_config: bool,
    destination: Path,
    accept_hooks: str,
    path_or_url: str,
    context_params: Optional[MutableMapping[str, Any]] = None,
) -> None:
    """Create a project from the template or configuration PATH_OR_URL in using optional [CONTEXT_PARAMS]."""
    create_cmd(
        path_or_url,
        destination,
        no_input,
        checkout,
        directory,
        overwrite_if_exists,
        skip_if_file_exists,
        default_config,
        accept_hooks,
        initial_context=context_params or {},
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
@click.option(
    "-d",
    "--destination",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="The directory to add the templates to. Defaults to the current working directory.",
)
@click.option(
    "--accept-hooks",
    type=click.Choice(["yes", "ask", "no", "first", "last", "all", "none"], case_sensitive=False),
    default="all",
    help="Accept pre/host hooks",
)
@click.argument("path_or_url", type=str, required=True)
@click.argument("context_params", nargs=-1, callback=validate_context_params)
def add(
    no_input: bool,
    checkout: str,
    directory: str,
    overwrite_if_exists: bool,
    skip_if_file_exists: bool,
    default_config: bool,
    destination: Path,
    accept_hooks: str,
    path_or_url: str,
    context_params: Optional[MutableMapping[str, Any]] = None,
) -> None:
    """Add the template or configuration PATH_OR_URL to an existing project."""
    output_dir = destination or Path.cwd()
    try:
        add_cmd(
            path_or_url,
            output_dir,
            no_input=no_input,
            checkout=checkout,
            directory=directory,
            overwrite_if_exists=overwrite_if_exists,
            skip_if_file_exists=skip_if_file_exists,
            default_config=default_config,
            accept_hooks=accept_hooks,
            initial_context=context_params or {},
        )
    except GitError as e:
        raise click.UsageError(str(e)) from e


@cli.command()
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use cookiecutter.json file content. "
    "Defaults to deleting any cached resources and re-downloading them.",
)
@click.option(
    "-d",
    "--destination",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="The directory to update. Defaults to the current working directory.",
)
@click.argument("context_params", nargs=-1, callback=validate_context_params)
def update(no_input: bool, destination: Path, context_params: Optional[OrderedDict] = None) -> None:
    """Update the project to the latest version of each template."""
    destination = destination or Path.cwd()
    try:
        update_cmd(destination, no_input=no_input)
    except GitError as e:
        raise click.UsageError(str(e)) from e


@cli.command()
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
@click.option(
    "-d",
    "--destination",
    required=False,
    default=lambda: Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="The directory to link the template to. Defaults to the current working directory.",
)
@click.argument("path_or_url", type=str, required=True)
@click.argument("context_params", nargs=-1, callback=validate_context_params)
def link(
    no_input: bool,
    checkout: str,
    directory: str,
    overwrite_if_exists: bool,
    skip_if_file_exists: bool,
    default_config: bool,
    destination: Optional[Path],
    path_or_url: str,
    context_params: Optional[MutableMapping[str, Any]] = None,
) -> None:
    """Link an existing git repo to the template or composition PATH_OR_URL using optional [CONTEXT_PARAMS]."""
    destination = destination or Path.cwd()
    try:
        link_cmd(
            path_or_url,
            destination,
            no_input=no_input,
            checkout=checkout,
            directory=directory,
            overwrite_if_exists=overwrite_if_exists,
            skip_if_file_exists=skip_if_file_exists,
            default_config=default_config,
            initial_context=context_params or {},
        )
    except GitError as e:
        raise click.UsageError(str(e)) from e


if __name__ == "__main__":
    cli()
