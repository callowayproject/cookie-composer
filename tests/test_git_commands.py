"""Tests for cookie_composer.git_commands."""
from pathlib import Path

import pytest
from git import Actor, Repo

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


def test_branch_from_first_commit_dirty(default_repo):
    """Should raise an error if the repo is dirty."""
    new_file_path = Path(default_repo.working_tree_dir) / "new-file.txt"
    new_file_path.write_text("hello")
    default_repo.index.add(str(new_file_path))

    with pytest.raises(GitError):
        git_commands.branch_from_first_commit(default_repo, "mybranch")


def test_branch_from_first_commit(default_repo):
    """Should raise an error if the repo is dirty."""
    first_commit_sha = next(default_repo.iter_commits()).hexsha
    default_repo.index.commit(
        message="Another commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-02 10:00:00"
    )
    git_commands.branch_from_first_commit(default_repo, "newbranch")
    assert default_repo.head.commit.hexsha == first_commit_sha


def test_get_latest_template_commit(default_repo):
    """Should return the latest hexsha."""
    first_sha = default_repo.head.commit.hexsha
    assert git_commands.get_latest_template_commit(default_repo.working_tree_dir) == first_sha

    second_commit = default_repo.index.commit(
        message="Another commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-02 10:00:00"
    )
    assert git_commands.get_latest_template_commit(default_repo.working_tree_dir) == second_commit.hexsha

    third_commit = default_repo.index.commit(
        message="Another commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-02 11:00:00"
    )
    assert git_commands.get_latest_template_commit(default_repo.working_tree_dir) == third_commit.hexsha


def test_clone_existing_repo(default_repo):
    """Should return the same repo if the repo already exists."""
    repo_path = Path(default_repo.working_tree_dir)
    repo = git_commands.clone("git://someplace/else.git", repo_path)
    assert repo.working_tree_dir == str(repo_path)
