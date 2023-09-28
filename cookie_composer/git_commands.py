"""Functions for using git."""
import logging
import subprocess
from pathlib import Path
from typing import Optional, Union

from git import InvalidGitRepositoryError, NoSuchPathError, Repo

from cookie_composer.exceptions import GitError

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

    repo.create_head(branch_name)
    repo.heads[branch_name].checkout()


def branch_from_first_commit(repo: Repo, branch_name: str) -> None:
    """Create and checkout a branch from the repo's first commit."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    first_commit = next(iter(repo.iter_commits("HEAD", max_parents=0, max_count=1)))
    repo.create_head(branch_name, first_commit.hexsha)
    repo.heads[branch_name].checkout()


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
        subprocess.run(
            three_way_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
    except subprocess.CalledProcessError:
        reject_command = [
            "git",
            "apply",
            "--3way",
            "--whitespace=fix",
        ]
        subprocess.run(
            reject_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
