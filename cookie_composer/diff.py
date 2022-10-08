"""
Generating the difference between two directories.

Nabbed from Cruft: https://github.com/cruft/cruft/
"""
from typing import List

from pathlib import Path
from re import sub
from subprocess import PIPE, run  # nosec

from cookie_composer.exceptions import ChangesetUnicodeError

DIFF_SRC_PREFIX = "upstream-template-old"
DIFF_DST_PREFIX = "upstream-template-new"


def _git_diff_command(*args: str) -> List[str]:
    """Get the git diff command with the supplied arguments added in."""
    # https://git-scm.com/docs/git-diff#Documentation/git-diff.txt---binary support for binary patch
    return [
        "git",
        "-c",
        "diff.noprefix=",
        "diff",
        "--no-index",
        "--relative",
        "--binary",
        f"--src-prefix={DIFF_SRC_PREFIX}/",
        f"--dst-prefix={DIFF_DST_PREFIX}/",
        *args,
    ]


def get_diff(repo0: Path, repo1: Path) -> str:
    """Compute the raw diff between two repositories."""
    # Use Path methods in order to straighten out the differences between the OSs.
    repo0_str = repo0.resolve().as_posix()
    repo1_str = repo1.resolve().as_posix()
    try:
        diff = run(
            _git_diff_command("--no-ext-diff", "--no-color", repo0_str, repo1_str),
            cwd=repo0_str,
            stdout=PIPE,
            stderr=PIPE,
        ).stdout.decode()
    except UnicodeDecodeError as e:
        raise ChangesetUnicodeError() from e

    diff = replace_diff_prefixes(diff, repo0_str, repo1_str)

    return diff


def replace_diff_prefixes(diff: str, repo0_path: str, repo1_path: str) -> str:
    """
    Replace the changed file prefixes in the diff output.

    Our ``git diff --no-index`` command will output full paths like so::

        --- upstream-template-old/tmp/tmpmp34g21y/remote/.coveragerc
        +++ upstream-template-new/tmp/tmpmp34g21y/local/.coveragerc

    This isn't the format we need in order to apply the diff later on. The result of
    this command will change the paths to::

        --- upstream-template-old/.coveragerc
        +++ upstream-template-new/.coveragerc


    NIX OPs have ``{prefix}/folder/file``
    WIN OPS have ``{prefix}/c:/folder/file``

    More info on git-diff can be found here: http://git-scm.com/docs/git-diff

    Args:
        diff: The diff output to change
        repo0_path: The full string path to the source repo
        repo1_path: The full string path to the destination repo

    Returns:
        The modified diff string
    """
    for repo in [repo0_path, repo1_path]:
        repo = sub("/[a-z]:", "", repo)  # Make repo look like a NIX absolute path.

        diff = diff.replace(f"{DIFF_SRC_PREFIX}{repo}", DIFF_SRC_PREFIX).replace(
            f"{DIFF_DST_PREFIX}{repo}", DIFF_DST_PREFIX
        )

    # This replacement is needed for renamed/moved files to be recognized properly
    # Renamed files in the diff don't have the prefixes and instead look like
    #
    # /tmp/tmpmp34g21y/remote/.coveragerc
    #
    # We need to include a trailing slash in the repo path when we replace them
    # (they don't include it). This would interfere with the above operation.
    # As a result, we only do this after the above replacement is made.
    diff = diff.replace(f"{repo0_path}/", "").replace(f"{repo1_path}/", "")

    return diff


def display_diff(repo0: Path, repo1: Path):
    """Displays the diff between two repositories."""
    run(_git_diff_command(repo0.as_posix(), repo1.as_posix()))
