"""Functions for using git."""
import logging
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union

from git import InvalidGitRepositoryError, NoSuchPathError, Repo

from cookie_composer.exceptions import GitError
from cookie_composer.utils import echo

logger = logging.getLogger(__name__)


def get_repo(
    project_dir: Union[str, Path], search_parent_directories: bool = False, ensure_clean: bool = False
) -> Repo:
    """
    Get the git Repo object for a directory.

    Args:
        project_dir: The directory containing the .git folder
        search_parent_directories: if ``True``, all parent directories will be searched for a valid repo as well.
        ensure_clean: if ``True``, raise an error if the repo is dirty

    Raises:
        GitError: If the directory is not a git repo
        GitError: If the directory git repository is dirty

    Returns:
        The GitPython Repo object
    """
    try:
        repo = Repo(str(project_dir), search_parent_directories=search_parent_directories)

        if ensure_clean and repo.is_dirty():
            raise GitError("The destination git repository is dirty. Please commit or stash the pending changes.")
        return repo
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise GitError(
            "Some cookie composer commands only work on git repositories. "
            "Please make the destination directory a git repo."
        ) from e


def clone(repo_url: str, dest_path: Optional[Path] = None) -> Repo:
    """
    Clone a repo.

    Args:
        repo_url: Repo URL or local path.
        dest_path: The path to clone to.

    Returns:
        The repository.
    """
    dest_path = dest_path or Path.cwd()

    if dest_path.exists():
        logger.debug(f"Found {dest_path}, attempting to update")
        return get_repo(dest_path, ensure_clean=True)
    else:
        logger.debug(f"Cloning {repo_url} into {dest_path}")
        return Repo.clone_from(repo_url, dest_path)


def branch_exists(repo: Repo, branch_name: str) -> bool:
    """
    Does the branch exist in the repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for

    Returns:
        ``True`` if the branch exists
    """
    return branch_name in repo.refs


def remote_branch_exists(repo: Repo, branch_name: str, remote_name: str = "origin") -> bool:
    """
    Does the branch exist in the remote repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for
        remote_name: The name of the remote reference. Defaults to ``origin``

    Returns:
        ``True`` if the branch exists in the remote repository
    """
    if remote_name in repo.remotes:
        return branch_name in repo.remotes[remote_name].refs

    return False


def checkout_ref(repo: Repo, ref: str) -> None:
    """
    Checkout a ref.

    Args:
        repo: The repository to check out
        ref: The ref to check out
    """
    repo.git.checkout(ref)


def checkout_branch(repo: Repo, branch_name: str, remote_name: str = "origin") -> None:
    """Checkout a local or remote branch."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    if len(repo.remotes) > 0:
        repo.remotes[0].fetch()

    if branch_exists(repo, branch_name):
        repo.heads[branch_name].checkout()
    elif remote_branch_exists(repo, branch_name, remote_name):
        repo.create_head(branch_name, f"origin/{branch_name}")
        repo.heads[branch_name].checkout()
    else:
        repo.create_head(branch_name)
        repo.heads[branch_name].checkout()


def _apply_patch_with_reject(repo: Repo, diff: str) -> None:
    """
    Apply a patch to a destination directory.

    Args:
        repo: The git repo to apply the patch to
        diff: The previously calculated diff
    """
    reject_command = ["git", "apply", "--reject"]
    try:
        echo("Attempting to apply patch with rejections.")
        subprocess.run(
            reject_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
        echo("Patch applied successfully.", fg="green")
    except subprocess.CalledProcessError as e2:
        echo(e2.stderr.decode(), err=True, fg="red")
        echo(
            "Project directory may have *.rej files reflecting merge conflicts with the update."
            " Please resolve those conflicts manually.",
            fg="yellow",
        )


def apply_patch(repo: Repo, diff: str) -> None:
    """
    Apply a patch to a destination directory.

    A git 3 way merge is the best bet at applying patches.

    Args:
        repo: The git repo to apply the patch to
        diff: The previously calculated diff
    """
    three_way_command = [
        "git",
        "apply",
        "--3way",
        "--whitespace=fix",
    ]

    try:
        echo("Attempting to apply patch with 3-way merge.")
        subprocess.run(
            three_way_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
        echo("Patch applied successfully.", fg="green")
    except subprocess.CalledProcessError as e:
        echo(f"There was a problem with the 3-way merge: {e.stderr.decode()}", err=True, fg="red")
        _apply_patch_with_reject(repo, diff)


@contextmanager
def temp_git_worktree_dir(
    repo_path: Path, worktree_path: Optional[Path] = None, branch: str = "master", commit: Optional[str] = None
) -> Iterator[Path]:
    """
    Context Manager for a temporary working directory of a branch in a git repo.

    Inspired by https://github.com/thomasjahoda/cookiecutter_project_upgrader/blob/master/
    cookiecutter_project_upgrader/logic.py

    Args:
        repo_path: The path to the template git repo
        worktree_path: The path put the worktree in. Defaults to a temporary directory.
        branch: The branch to check out
        commit: The optional commit to check out

    Yields:
        The worktree_path
    """
    # Create a temporary working directory of a branch in a git repo.
    repo = get_repo(repo_path)
    tmp_dir = Path(tempfile.mkdtemp(prefix=repo_path.name))
    worktree_path = worktree_path or tmp_dir
    worktree_path.mkdir(parents=True, exist_ok=True)
    repo.git.worktree(
        "add",
        str(worktree_path),
        commit or branch,
    )
    try:
        yield Path(worktree_path)
    finally:
        # Clean up the temporary working directory.
        shutil.rmtree(worktree_path)
        shutil.rmtree(tmp_dir)
        repo.git.worktree("prune")
