"""Utilities not easily categorized."""

import os
import stat
from contextlib import contextmanager
from pathlib import Path
from typing import IO, Any, Callable, Iterator, Optional, Set


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
        nl: Print a newline after the message. Enabled by default.
        err: Write to stderr instead of stdout.
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


@contextmanager
def temporary_copy(original_path: Path) -> Iterator[Path]:
    """
    Create a temporary copy of a file or directory.

    Args:
        original_path: The path to the file or directory to copy

    Yields:
        The path to the temporary copy
    """
    import tempfile
    from shutil import copy2, copytree, rmtree

    if original_path.is_dir():
        temp_dir = tempfile.mkdtemp()
        copytree(original_path, temp_dir, dirs_exist_ok=True)
        yield Path(temp_dir)
        rmtree(temp_dir)
    else:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        copy2(original_path, temp_file.name)
        yield Path(temp_file.name)
        os.remove(temp_file.name)
