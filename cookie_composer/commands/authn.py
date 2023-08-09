"""Authentication subcommands."""
import sys

import rich_click as click

from cookie_composer.authentication import get_cached_token, login_to_svc


@click.group()
def auth() -> None:
    """Authenticate cookie-composer to a service."""
    pass


@auth.command()
@click.option(
    "-p",
    "--git-protocol",
    type=click.Choice(["https", "ssh"]),
    default="https",
    help="The protocol to use for git operations",
)
@click.option(
    "-h",
    "--service",
    type=str,
    help="The host name of the service to authenticate with",
    default="github.com",
)
@click.option("-s", "--scopes", type=str, help="Additional authentication scopes to request")
@click.option(
    "--with-token", type=click.File("r"), is_flag=False, flag_value=sys.stdin, help="Read token from standard input"
)
def login(git_protocol: str, service: str, scopes: str, with_token: click.File) -> None:
    """Authenticate to a service."""
    w_token = with_token.read() if with_token else None
    if not w_token and get_cached_token(service):
        click.echo("Already logged in.")
    else:
        login_to_svc(service, git_protocol, scopes, w_token)


# TODO: Implement logout command
# @auth_cli.command()
# def logout():
#     """Log out of a host."""
#     pass


# TODO: Implement refresh command
# @auth_cli.command()
# def refresh():
#     """Refresh stored authentication credentials."""
#     pass


# TODO: Implement status command
# @auth_cli.command()
# def status():
#     """View authentication status."""
#     pass


@auth.command()
@click.option(
    "-h",
    "--service",
    type=str,
    help="The host name of the service to authenticate with",
    default="github.com",
)
def token(service: str) -> None:
    """Print the auth token cookie-composer is configured to use."""
    oauth_token = get_cached_token(service)
    if oauth_token:
        click.echo(oauth_token)
    else:
        raise click.UsageError(f"No cookie-composer auth token configured for {service}.")
