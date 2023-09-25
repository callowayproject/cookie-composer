"""Testing configuration."""
import shutil
from pathlib import Path

import pytest
from git import Actor, Repo


@pytest.fixture
def fixtures_path() -> Path:
    """Return the path to the testing fixtures."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def default_origin(tmp_path: Path) -> Repo:
    """Create a default origin repo."""
    tmp_repo_path = tmp_path / "tmp_repo"
    tmp_repo = Repo.init(tmp_repo_path)
    tmp_repo_path.joinpath("README.md").write_text("Hello World!")
    tmp_repo.index.add(["README.md"])
    tmp_repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    tmp_repo_path.joinpath("README.md").write_text("Hello World!\n\nThis is a test.")
    tmp_repo.index.add(["README.md"])
    tmp_repo.index.commit(
        message="second commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 11:00:00"
    )
    tmp_repo.create_tag("v1.0.0")
    tmp_repo.create_head("remote-branch")
    tmp_repo.heads["remote-branch"].checkout()
    tmp_repo_path.joinpath("newfile.md").write_text("Hello World!\n\nThis is a test.\n\nThis is a new line.")
    tmp_repo.index.add(["newfile.md"])
    tmp_repo.index.commit(
        message="first commit on a branch",
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-01 12:00:00",
    )
    origin_path = tmp_path / "origin.git"
    origin = Repo.init(origin_path, bare=True)

    tmp_repo.create_remote("origin", str(origin_path))
    tmp_repo.remotes.origin.push("master")
    tmp_repo.remotes.origin.push("remote-branch")
    tmp_repo.remotes.origin.push("v1.0.0")

    shutil.rmtree(tmp_repo_path)
    return origin


@pytest.fixture
def default_repo(default_origin: Repo, tmp_path: Path) -> Repo:
    """Clone the default origin repo."""
    repo = default_origin.clone(tmp_path / "repo")
    repo.heads.master.checkout()
    repo.remotes.origin.pull()

    return repo
