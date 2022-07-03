"""Utilities not easily categorized."""
from typing import IO, Any, Optional

from pathlib import Path

from cookie_composer.composition import RenderedComposition
from cookie_composer.data_merge import comprehensive_merge


def get_context_for_layer(composition: RenderedComposition, index: Optional[int] = None) -> dict:
    """
    Merge the contexts for all layers up to index.

    An ``index`` of ``None`` does all the layers.

    Args:
        composition: The rendered composition
        index: Merge the contexts of the layers up to this 0-based index. ``None`` to do all layers.

    Returns:
        The comprehensively merged context
    """
    full_context = {}
    if index is None:
        layers = composition.layers
    else:
        layers = composition.layers[: index + 1]

    for layer in layers:
        full_context = comprehensive_merge(full_context, layer.new_context)

    return full_context


def get_template_name(path_or_url: str, directory: Optional[str] = None, checkout: Optional[str] = None) -> str:
    """
    Get the name of the template using the path or URL.

    Args:
        path_or_url: The URL or path to the template
        directory: Directory within a git repository template that holds the cookiecutter.json file.
        checkout: The branch, tag or commit to use if template is a git repository.

    Raises:
        ValueError: If the path_or_url is not parsable

    Returns:
        The name of the template without extensions
    """
    from urllib.parse import urlparse

    path = urlparse(path_or_url).path
    if not path:
        raise ValueError("There is no path.")

    base_path = Path(path).stem
    dir_name = Path(directory).name if directory else None
    parts = [base_path, dir_name, checkout]
    return "-".join([x for x in parts if x])


def echo(
    message: Optional[Any] = None,
    file: Optional[IO] = None,
    nl: bool = True,
    err: bool = False,
    color: Optional[bool] = None,
    **styles
):
    """
    A local abstraction for printing messages.

    Default behavior is that of ``click.secho`` .

    This is to allow user feedback without every function requiring a click dependency.
    Especially during testing.

    Args:
        message: The string or bytes to output. Other objects are converted to strings.
        file: The file to write to. Defaults to stdout.
        err: Write to stderr instead of stdout.
        nl: Print a newline after the message. Enabled by default.
        color: Force showing or hiding colors and other styles. By default Click will remove color if the output
            does not look like an interactive terminal.
        **styles: Style keyword arguments
    """
    import click

    click.secho(message, file, nl, err, color, **styles)
