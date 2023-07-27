"""Tests for the commands.add module."""
import os
import shutil
from pathlib import Path

import pytest
from git import Actor, Repo

from cookie_composer.commands import add


@pytest.fixture
def create_base_repo(fixtures_path, tmp_path):
    """Make the base repo for adding template."""
    rendered_layer = fixtures_path / "rendered1" / "testproject"
    dest_path = tmp_path / "fake-project-template"
    shutil.copytree(rendered_layer, dest_path)

    rendered_comp = Path(rendered_layer.parent / "rendered-composition.yaml").read_text()
    Path(dest_path / ".composition.yaml").write_text(rendered_comp)

    repo = Repo.init(dest_path)
    repo.index.add(".")
    repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )

    return dest_path


def test_render_template(fixtures_path, create_base_repo):
    """Test rendering a single template."""
    template_path = fixtures_path / "template2"

    add.add_cmd(str(template_path), create_base_repo, no_input=True)

    rendered_items = {item.name for item in os.scandir(create_base_repo)}
    assert rendered_items == {
        ".composition.yaml",
        ".git",
        "ABOUT.md",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "requirements.txt",
    }


def test_render_composition(fixtures_path, create_base_repo, tmp_path):
    """Test rendering a composition file."""
    from ruamel.yaml import YAML

    composition = [{"template": str(fixtures_path / "template2")}]
    template_path = tmp_path / "test_composition.yaml"

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(template_path, "w") as f:
        yaml.dump_all(composition, f)

    assert template_path.exists()

    add.add_cmd(str(template_path), create_base_repo, no_input=True)
    rendered_items = {item.name for item in os.scandir(create_base_repo)}

    assert rendered_items == {
        ".composition.yaml",
        ".git",
        "ABOUT.md",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "requirements.txt",
    }
