"""Testing configuration."""
from pathlib import Path

import pytest
from git import Actor, Repo


@pytest.fixture
def fixtures_path() -> Path:
    """Return the path to the testing fixtures."""

    return Path(__file__).parent / "fixtures"


@pytest.fixture
def default_repo(tmp_path):
    """Make a bunch of default commits to a temporary bare git repo."""
    origin = Repo.init(tmp_path / "origin", bare=True)
    origin.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    origin.create_head("remote-branch")

    repo = origin.clone(tmp_path / "repo")
    repo.heads.master.checkout()
    repo.remotes.origin.pull()
    return repo
