"""Tests for the diff module."""

from pathlib import Path
from typing import Tuple

import pytest

from cookie_composer.diff import get_diff


@pytest.fixture()
def test_repos(tmp_path) -> Tuple[Path, Path]:
    """Create two empty repositories."""
    repo0 = tmp_path / "repo0"
    repo1 = tmp_path / "repo1"
    repo0.mkdir()
    repo1.mkdir()
    return repo0, repo1


def test_get_diff_with_add(test_repos: Tuple[Path, Path]):
    """Adding a file to the second repo should show up in the diff."""

    test_repos[1].joinpath("file").touch()

    diff = get_diff(test_repos[0], test_repos[1])
    diff_lines = diff.splitlines()

    assert diff_lines[0] == "diff --git upstream-template-old/file upstream-template-new/file"
    assert diff_lines[1] == "new file mode 100644"
    assert diff_lines[2].startswith("index 0000000")


def test_get_diff_with_delete(test_repos: Tuple[Path, Path]):
    """Deleting a file from the second repo should show up in the diff."""
    test_repos[0].joinpath("file").touch()

    diff = get_diff(test_repos[0], test_repos[1])
    diff_lines = diff.splitlines()

    assert diff_lines[0] == "diff --git upstream-template-old/file upstream-template-new/file"
    assert diff_lines[1] == "deleted file mode 100644"
    assert diff_lines[2].startswith("index")
    assert diff_lines[2].endswith("0000000")
