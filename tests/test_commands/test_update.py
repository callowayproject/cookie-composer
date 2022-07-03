"""Test the update command."""
import os
import re
import shutil
from pathlib import Path

import pytest
from git import Actor, Repo

from cookie_composer.commands import update
from cookie_composer.git_commands import get_repo


@pytest.fixture
def git_template(fixtures_path, tmp_path) -> dict:
    """Set up the template in a git repo."""
    template_path = fixtures_path / "template1"
    dest_path = tmp_path / "template1"
    shutil.copytree(template_path, dest_path)

    template_repo = Repo.init(dest_path)
    template_repo.index.add(".")
    template_repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    template_initial_sha = template_repo.head.object.hexsha
    new_file = dest_path / "{{cookiecutter.repo_name}}" / "newfile.txt"
    new_file.write_text("")
    template_repo.index.add(str(new_file))
    template_repo.index.commit(
        message="second commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 11:00:00"
    )
    template_updated_sha = template_repo.head.object.hexsha
    assert template_initial_sha != template_updated_sha
    return {"first_commit": template_initial_sha, "second_commit": template_updated_sha, "template_path": dest_path}


@pytest.fixture
def git_project(fixtures_path, tmp_path, git_template: dict) -> dict:
    """Make the base repo for adding template."""
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)

    rendered_layer = fixtures_path / "rendered1" / "testproject"
    dest_path = tmp_path / "fake-project-template"
    shutil.copytree(rendered_layer, dest_path)

    rendered_comp_path = dest_path / ".composition.yaml"
    rendered_comp = {
        "checkout": None,
        "commit": git_template["first_commit"],
        "context": {
            "_requirements": {"bar": ">=5.0.0", "foo": ""},
            "project_name": "Fake Project Template",
            "repo_name": "fake-project-template",
            "repo_slug": "fake-project-template",
        },
        "directory": None,
        "merge_strategies": {"*": "do-not-merge"},
        "no_input": True,
        "overwrite": [],
        "overwrite_exclude": [],
        "password": None,
        "skip_generation": [],
        "skip_hooks": False,
        "skip_if_file_exists": True,
        "template": str(git_template["template_path"]),
    }
    with open(rendered_comp_path, "w") as f:
        yaml.dump(rendered_comp, f)

    repo = Repo.init(dest_path)
    repo.index.add(".")
    repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    result = {"project_path": dest_path}
    result.update(git_template)
    rendered_items = {item.name for item in os.scandir(dest_path)}
    assert rendered_items == {
        ".composition.yaml",
        ".git",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "requirements.txt",
    }

    return result


def test_update_command(git_project: dict):
    """Basic test of the update command."""
    update.update_cmd(git_project["project_path"], no_input=True)
    rendered_items = {item.name for item in os.scandir(git_project["project_path"])}
    assert rendered_items == {
        ".composition.yaml",
        ".git",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "newfile.txt",
        "requirements.txt",
    }
    repo = get_repo(git_project["project_path"])
    assert repo.active_branch.name == "update_composition"
    comp_text = Path(git_project["project_path"] / ".composition.yaml").read_text()
    assert re.search(f"commit: {git_project['second_commit']}", comp_text)


def test_update_command_no_update_required(git_project: dict, capsys):
    """Should output a message and do nothing."""
    repo = get_repo(git_project["project_path"])

    # rewrite the composition to change the commit to the latest of the template
    rendered_comp_path = Path(git_project["project_path"] / ".composition.yaml")
    rendered_comp = rendered_comp_path.read_text().replace(
        f"commit: {git_project['first_commit']}", f"commit: {git_project['second_commit']}"
    )
    rendered_comp_path.write_text(rendered_comp)
    repo.index.add(str(rendered_comp_path))
    repo.index.commit(
        message="updated composition", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-02 10:00:00"
    )

    update.update_cmd(git_project["project_path"], no_input=True)
    captured = capsys.readouterr()
    assert "already up-to-date" in captured.out
    assert repo.active_branch.name == "master"
    comp_text = Path(git_project["project_path"] / ".composition.yaml").read_text()
    assert re.search(f"commit: {git_project['second_commit']}", comp_text)
