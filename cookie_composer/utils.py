"""Utilities not easily categorized."""
import os
import stat
from pathlib import Path
from typing import IO, Any, Callable, Dict, Optional, Set

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
    full_context: Dict[str, Any] = {}
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
    **styles,
) -> None:
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


def get_deleted_files(template_dir: Path, project_dir: Path) -> Set[Path]:
    """
    Get a list of files in the rendered template that do not exist in the project.

    This is to avoid introducing changes that won't apply cleanly to the current project.

    Nabbed from Cruft: https://github.com/cruft/cruft/

    Args:
        template_dir: The path to the directory rendered with the same context as the project
        project_dir: The path to the current project

    Returns:
        A set of paths that are missing
    """
    cwd = Path.cwd()
    os.chdir(template_dir)
    template_paths = set(Path(".").glob("**/*"))
    os.chdir(cwd)
    os.chdir(project_dir)
    deleted_paths = set(filter(lambda path: not path.exists(), template_paths))
    os.chdir(cwd)
    return deleted_paths


def remove_paths(root: Path, paths_to_remove: Set[Path]) -> None:
    """
    Remove all paths in ``paths_to_remove`` from ``root``.

    Nabbed from Cruft: https://github.com/cruft/cruft/

    Args:
        root: The absolute path of the directory requiring path removal
        paths_to_remove: The set of relative paths to remove from ``root``
    """
    # There is some redundancy here in chmod-ing dirs and/or files differently.
    abs_paths_to_remove = [root / path_to_remove for path_to_remove in paths_to_remove]

    for path in abs_paths_to_remove:
        remove_single_path(path)


def remove_readonly_bit(func: Callable[[str], None], path: str, _: Any) -> None:  # pragma: no-coverage
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)  # WINDOWS
    func(path)


def remove_single_path(path: Path) -> None:
    """
    Remove a path with extra error handling for Windows.

    Args:
        path: The path to remove

    Raises:
        IOError: If the file could not be removed
    """
    from shutil import rmtree

    if path.is_dir():
        try:
            rmtree(path, ignore_errors=False, onerror=remove_readonly_bit)
        except Exception as e:  # noqa: BLE001 pragma: no-coverage
            raise IOError("Failed to remove directory.") from e
    elif path.is_file():
        try:
            path.unlink()
        except PermissionError:  # pragma: no-coverage
            path.chmod(stat.S_IWRITE)
            path.unlink()
        except Exception as exc:  # noqa: BLE001 pragma: no-coverage
            raise IOError("Failed to remove file.") from exc
