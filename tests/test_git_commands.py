"""Tests for cookie_composer.git_commands."""

from pathlib import Path
from typing import Optional

import pytest
from pytest import param
from git import Repo

from cookie_composer import git_commands
from cookie_composer.exceptions import GitError


def test_get_repo(tmp_path):
    """Should return the repo object."""
    repo_path = tmp_path / "bare-repo"
    expected = Repo.init(repo_path)
    result = git_commands.get_repo(repo_path)
    assert result == expected


def test_get_repo_not_a_repo(tmp_path):
    """Should raise an error if the path doesn't exist or is not a git repo."""
    repo_path = tmp_path / "bare-repo"

    with pytest.raises(GitError):
        git_commands.get_repo(repo_path)

    repo_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(GitError):
        git_commands.get_repo(repo_path)


def test_branch_exists(default_repo):
    """Should return True if the branch exists in the repo."""
    assert not git_commands.branch_exists(default_repo, "mybranch")

    default_repo.create_head("mybranch")
    default_repo.heads.mybranch.checkout()

    assert git_commands.branch_exists(default_repo, "mybranch")


def test_remote_branch_exists(default_repo):
    """Should return True if the remote branch exists."""
    assert git_commands.remote_branch_exists(default_repo, "remote-branch")
    assert not git_commands.remote_branch_exists(default_repo, "missingbranch")


def test_remote_branch_exists_missing(default_repo):
    """Should return False if there are no remotes."""
    assert not git_commands.remote_branch_exists(default_repo, "missingbranch", "missingremote")


def test_checkout_branch_dirty_repo(default_repo):
    """Should raise an error if the repo is dirty."""
    new_file_path = Path(default_repo.working_tree_dir) / "new-file.txt"
    new_file_path.write_text("hello")
    default_repo.index.add(str(new_file_path))

    with pytest.raises(GitError):
        git_commands.checkout_branch(default_repo, "mybranch")


def test_checkout_branch_remote_branch(default_repo):
    """Checks out the remote-branch."""
    git_commands.checkout_branch(default_repo, "remote-branch")
    assert default_repo.active_branch.name == "remote-branch"


def test_checkout_branch_local_branch(default_repo):
    """Checks out the remote-branch."""
    default_repo.create_head("local-branch")
    git_commands.checkout_branch(default_repo, "local-branch")
    assert default_repo.active_branch.name == "local-branch"


def test_checkout_branch_missing_branch(default_repo):
    """Creates the branch if the branch doesn't exist."""
    git_commands.checkout_branch(default_repo, "local-branch")
    assert default_repo.active_branch.name == "local-branch"


def test_clone_existing_repo(default_repo):
    """Should return the same repo if the repo already exists."""
    repo_path = Path(default_repo.working_tree_dir)
    repo = git_commands.clone("git://someplace/else.git", repo_path)
    assert repo.working_tree_dir == str(repo_path)


@pytest.mark.parametrize(
    ["checkout", "commit", "expected_ref"],
    [
        param(None, None, "master", id="default"),
        param("remote-branch", None, "remote-branch", id="checkout branch"),
        param("v1.0.0", None, "v1.0.0", id="checkout tag"),
        param(None, "HEAD~1", "HEAD~1", id="checkout commit"),
    ],
)
def test_temp_git_worktree_dir(
    default_origin: Repo, tmp_path: Path, checkout: Optional[str], commit: Optional[str], expected_ref: str
):
    """Should return the path to the worktree and check out the appropriate ref."""

    dest_path = tmp_path / "dest"
    with git_commands.temp_git_worktree_dir(
        Path(default_origin.working_dir), dest_path, branch=checkout, commit=commit
    ) as wtree_dir:
        assert wtree_dir == dest_path
        r = git_commands.get_repo(wtree_dir)
        assert r.head.commit.hexsha == default_origin.commit(expected_ref).hexsha
