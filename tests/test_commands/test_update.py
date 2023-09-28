"""Test the update command."""
import os
import re
import shutil
from pathlib import Path

import pytest
from git import Actor, Repo

from cookie_composer.commands import update
from cookie_composer.git_commands import checkout_branch, get_repo


@pytest.fixture
def git_template(fixtures_path: Path, tmp_path: Path) -> dict:
    """Set up the template in a git repo."""
    template_path = fixtures_path / "template1"
    tmp_repo_path = tmp_path / "template1"
    shutil.copytree(template_path, tmp_repo_path)

    tmp_repo = Repo.init(tmp_repo_path, b="master")
    tmp_repo.index.add(tmp_repo.untracked_files)
    tmp_repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    new_file = tmp_repo_path / "{{cookiecutter.repo_name}}" / "newfile.txt"
    new_file.write_text("")
    tmp_repo.index.add(str(new_file))
    tmp_repo.index.commit(
        message="second commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 11:00:00"
    )

    origin_path = tmp_path / "origin"
    origin = Repo.init(origin_path, bare=True)
    tmp_repo.create_remote("origin", str(origin_path))
    tmp_repo.remotes.origin.push("master")
    shutil.rmtree(tmp_repo_path)

    template_updated_sha = origin.heads.master.commit.hexsha
    template_initial_sha = origin.heads.master.commit.parents[0].hexsha
    return {
        "first_commit": template_initial_sha,
        "second_commit": template_updated_sha,
        "template_path": origin.working_dir,
    }


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
        "template": f'git+file://{git_template["template_path"]}',
    }
    with open(rendered_comp_path, "w") as f:
        yaml.dump(rendered_comp, f)

    repo = Repo.init(dest_path)
    rendered_items = {item.name for item in os.scandir(dest_path)}
    assert rendered_items == {
        ".composition.yaml",
        ".git",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "requirements.txt",
    }

    repo.index.add(
        [
            ".composition.yaml",
            "README.md",
            "dontmerge.json",
            "merge.yaml",
            "requirements.txt",
        ]
    )
    repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    result = {"project_path": dest_path}
    result.update(git_template)

    assert not repo.untracked_files
    return result


def test_update_command(git_project: dict):
    """Basic test of the update command."""
    repo = get_repo(git_project["project_path"])
    assert repo.active_branch.name == "master"
    current_items = {item.name for item in os.scandir(git_project["project_path"])}
    assert current_items == {
        ".composition.yaml",
        ".git",
        "README.md",
        "dontmerge.json",
        "merge.yaml",
        "requirements.txt",
    }

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

    # we should be on the update_composition branch
    assert repo.active_branch.name == "update_composition"

    # All the files should have been committed in the update_cmd
    assert not repo.untracked_files

    # Make sure the composition was updated to the latest commit
    comp_text = Path(git_project["project_path"] / ".composition.yaml").read_text()
    assert re.search(f"commit: {git_project['second_commit']}", comp_text)
    previous_sha = repo.active_branch.commit.hexsha

    # Check for idempotence
    checkout_branch(repo, "master")
    update.update_cmd(git_project["project_path"], no_input=True)
    assert repo.active_branch.commit.hexsha == previous_sha


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
    assert "All layers are up-to-date." in captured.out
    assert repo.active_branch.name == "master"
    comp_text = Path(git_project["project_path"] / ".composition.yaml").read_text()
    assert re.search(f"commit: {git_project['second_commit']}", comp_text)
