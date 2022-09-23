"""Test the link command."""
import shutil
from pathlib import Path

import pytest
from git import Repo

from cookie_composer.commands import link
from cookie_composer.git_commands import get_repo


@pytest.fixture
def linkable_repo(fixtures_path, tmp_path) -> Path:
    """A default repo for testing."""
    rendered_layer = fixtures_path / "rendered1" / "testproject"
    dest_path = tmp_path / "fake-project-template"
    shutil.copytree(rendered_layer, dest_path)
    repo = Repo.init(dest_path)
    repo.index.add(repo.untracked_files)
    repo.index.commit(message="Initial commit")
    assert not repo.is_dirty()
    return dest_path


def test_link(linkable_repo: Path, fixtures_path: Path):
    """Linking an existing repo should create another branch."""
    template = fixtures_path / "template1"

    repo = get_repo(linkable_repo)

    link.link_cmd(str(template), linkable_repo, no_input=True)

    assert {head.name for head in repo.heads} == {"master", "link_composition"}


def test_link_cant_install_over_composition(linkable_repo: Path, fixtures_path: Path):
    """Can't link a repo with a .composition.yaml file."""
    repo = get_repo(linkable_repo)
    comp_file = linkable_repo / ".composition.yaml"
    comp_file.write_text("")
    repo.index.add(str(comp_file))
    repo.index.commit("Adding comp")

    template = fixtures_path / "template1"

    with pytest.raises(ValueError) as e:
        link.link_cmd(str(template), linkable_repo, no_input=True)
        assert str(e).startswith("There is already a .composition.yaml")


def test_link_checks_out_existing_branch(linkable_repo: Path, fixtures_path: Path):
    """Link command should check out existing link_composition branch."""
    template = fixtures_path / "template1"

    repo = get_repo(linkable_repo)
    repo.create_head("link_composition")

    link.link_cmd(str(template), linkable_repo, no_input=True)

    assert {head.name for head in repo.heads} == {"master", "link_composition"}
