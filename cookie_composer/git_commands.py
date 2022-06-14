"""Functions for using git."""
from ctypes import Union
from pathlib import Path

from git import InvalidGitRepositoryError, Repo

from cookie_composer.exceptions import GitError


def get_repo(project_dir: Union[str, Path]) -> Repo:
    """
    Get the git Repo object for a directory.

    Args:
        project_dir: The directory containing the .git folder

    Raises:
        GitError: If the directory is not a git repo

    Returns:
        The GitPython Repo object
    """
    try:
        return Repo(str(project_dir))
    except InvalidGitRepositoryError as e:
        raise GitError("Some cookie composer commands only work on git repositories.") from e


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
    return branch_name in repo.remotes[remote_name].refs


def checkout_branch(repo: Repo, branch_name: str, remote_name: str = "origin"):
    """Checkout a local or remote branch."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    repo.remotes[0].fetch()
    if branch_exists(repo, branch_name):
        repo.heads[branch_name].checkout()
    elif remote_branch_exists(repo, branch_name, remote_name):
        repo.create_head(branch_name, f"origin/{branch_name}")
        repo.heads[branch_name].checkout()


def branch_from_first_commit(repo: Repo, branch_name: str):
    """Create and checkout a branch from the repo's first commit."""
    if repo.is_dirty():
        raise GitError(
            "Cookie composer cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    first_commit = list(repo.iter_commits("HEAD", max_parents=0, max_count=1))[0]
    repo.create_head(branch_name, first_commit.hexsha)
    repo.heads[branch_name].checkout()
