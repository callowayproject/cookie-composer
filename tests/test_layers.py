"""Test layer rendering."""
import json
import os
from collections import OrderedDict
from pathlib import Path
from shutil import copytree

import pytest
from cookiecutter.config import get_user_config

from cookie_composer import layers
from cookie_composer.layers import LayerConfig, RenderedLayer
from cookie_composer.data_merge import Context, comprehensive_merge, DO_NOT_MERGE, OVERWRITE
from cookie_composer.templates.source import get_template_repo
from cookie_composer.templates.types import Template


@pytest.fixture
def template_one(fixtures_path: Path, tmp_path: Path) -> Template:
    """Return a Template using the template1 fixture."""
    template_repo = get_template_repo(str(fixtures_path.joinpath("template1")), tmp_path)
    return Template(repo=template_repo)


@pytest.fixture
def template_two(fixtures_path: Path, tmp_path: Path) -> Template:
    """Return a Template using the template2 fixture."""
    template_repo = get_template_repo(str(fixtures_path.joinpath("template2")), tmp_path)
    return Template(repo=template_repo)


def test_render_layer(fixtures_path: Path, tmp_path: Path, template_one: Template):
    """Test rendering a layer."""
    layer_conf = LayerConfig(template=template_one, no_input=True)
    initial_dir_items = len(list(tmp_path.iterdir()))
    rendered_layer = layers.render_layer(layer_conf, tmp_path)
    expected_context = json.loads(Path(fixtures_path / "template1/cookiecutter.json").read_text())
    expected_context["repo_name"] = "fake-project-template"
    expected_context["repo_slug"] = "fake-project-template"
    expected = RenderedLayer(
        layer=layer_conf,
        location=tmp_path,
        rendered_context=expected_context,
        rendered_name="fake-project-template",
    )
    assert rendered_layer == expected
    assert len(list(tmp_path.iterdir())) == initial_dir_items + 1


def test_get_write_strategy_skip_generation(fixtures_path: Path, template_one: Template):
    """Files matching a skip generation glob are skipped."""
    layer_config = LayerConfig(
        template=template_one,
        skip_generation=["README.md"],
        skip_if_file_exists=False,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "template1" / "{{cookiecutter.repo_name}}" / "README.md"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_dest_not_exist(tmp_path: Path, fixtures_path: Path, template_one: Template):
    """If the destination path doesn't exist, return the write strategy."""
    layer_config = LayerConfig(
        template=template_one,
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "template1" / "{{cookiecutter.repo_name}}" / "README.md"
    dest_path = tmp_path / "foo" / "README.md"
    assert layers.get_write_strategy(filepath, dest_path, rendered_layer) == layers.WriteStrategy.WRITE


def test_get_write_strategy_merge_strategy(fixtures_path: Path, template_one: Template):
    """Return the correct write strategy for mergable files."""
    layer_config = LayerConfig(
        template=template_one,
        merge_strategies={
            "*.yml": OVERWRITE,
            "*.yaml": OVERWRITE,
            "*.json": DO_NOT_MERGE,
        },
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.MERGE
    filepath = fixtures_path / "existing.json"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_overwrite_exclude(fixtures_path: Path, template_one: Template):
    """Return SKIP if the file matches an overwrite_exclude pattern."""
    layer_config = LayerConfig(
        template=template_one,
        overwrite_exclude=["*.yaml"],
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_overwrite(fixtures_path: Path, template_one: Template):
    """Return WRITE if the file matches an overwrite pattern."""
    layer_config = LayerConfig(
        template=template_one,
        overwrite=["*.yaml"],
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.WRITE


def test_get_write_strategy_skip_if_file_exists(fixtures_path: Path, template_one: Template):
    """Return SKIP or WRITE based on the skip_if_file_exists setting."""
    layer_config = LayerConfig(
        template=template_one,
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(
        layer=layer_config, location=fixtures_path, rendered_context={}, rendered_name="test"
    )
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP

    rendered_layer.layer.skip_if_file_exists = False
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.WRITE


def test_merge_layers(tmp_path: Path, fixtures_path: Path, template_one: Template):
    """Test merging layers together."""
    # copy rendered1 layer to temp dir
    rendered1 = fixtures_path / "rendered1"
    rendered_layer_path = copytree(rendered1, tmp_path, dirs_exist_ok=True)
    context1 = json.loads((rendered1 / "context.json").read_text())

    # create a rendered layer object for rendered2
    layer_config = LayerConfig(
        template=template_one,
        skip_if_file_exists=False,
        merge_strategies={
            "*.json": DO_NOT_MERGE,
            "*.yaml": OVERWRITE,
        },
    )
    context2 = json.loads((fixtures_path / "rendered2" / "context.json").read_text())
    full_context = comprehensive_merge(context1, context2)
    rendered2_config = RenderedLayer(
        layer=layer_config,
        location=fixtures_path / "rendered2",
        rendered_context=full_context,
        rendered_name="testproject",
    )
    # merge the layers
    layers.merge_layers(rendered_layer_path, rendered2_config)

    # check the merged layers in the temp dir are accurate
    readme_content = (rendered_layer_path / "testproject/README.md").read_text()
    assert readme_content == "# testproject\n"

    about_content = (rendered_layer_path / "testproject/ABOUT.md").read_text()
    assert about_content == "# Intentionally different name\n"

    requirements_content = (rendered_layer_path / "testproject/requirements.txt").read_text()
    assert requirements_content == "bar>=5.0.0\nbaz\nfoo\n"


def test_render_layers(fixtures_path: Path, tmp_path: Path, template_one: Template, template_two: Template):
    """Render layers generates a list of rendered layer objects."""
    tmpl_layers = [
        LayerConfig(template=template_one),
        LayerConfig(template=template_two),
    ]
    context1 = json.loads((fixtures_path / "template1" / "cookiecutter.json").read_text())
    context2 = json.loads((fixtures_path / "template2" / "cookiecutter.json").read_text())
    comprehensive_merge(context1, context2)

    rendered_layers = layers.render_layers(tmpl_layers, tmp_path, None, no_input=True)
    rendered_project = tmp_path / rendered_layers[0].rendered_name
    rendered_items = {item.name for item in os.scandir(rendered_project)}

    assert rendered_items == {"ABOUT.md", "README.md", "requirements.txt"}


def test_render_layer_git_template(fixtures_path: Path, tmp_path: Path):
    """Render layer of a git-based template includes the latest_commit."""
    from git import Actor, Repo

    template_path = fixtures_path / "template1"
    git_tmpl_path = copytree(template_path, tmp_path / "template1")
    repo = Repo.init(str(git_tmpl_path))
    repo.git.add(".")
    repo.index.commit(
        message="Another commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-02 10:00:00"
    )
    latest_sha = repo.head.commit.hexsha
    assert latest_sha is not None

    template = Template(
        repo=get_template_repo(str(git_tmpl_path), tmp_path),
    )
    assert template.repo.format == "git"
    assert template.repo.latest_sha == latest_sha

    layer_conf = LayerConfig(template=template, no_input=True)
    render_dir = tmp_path / "render"
    rendered_layer = layers.render_layer(layer_conf, render_dir)
    expected_context = template.context
    expected_context["repo_name"] = "fake-project-template"
    expected_context["repo_slug"] = "fake-project-template"
    expected = RenderedLayer(
        layer=layer_conf,
        location=render_dir,
        rendered_context=expected_context,
    )
    assert rendered_layer == expected
    assert rendered_layer.latest_commit == latest_sha
    assert rendered_layer.layer.template.repo.latest_sha == latest_sha
    assert {x.name for x in Path(render_dir / "fake-project-template").iterdir()} == {"README.md", "requirements.txt"}


def test_get_layer_context(fixtures_path: Path, template_one: Template):
    layer_conf = LayerConfig(template=template_one, no_input=True)
    user_config = get_user_config(config_file=None, default_config=False)

    context = layers.get_layer_context(layer_conf, user_config)
    assert context == Context(
        {
            "project_name": "Fake Project Template",
            "repo_name": "fake-project-template",
            "repo_slug": "fake-project-template",
            "service_name": "foo",
            "_requirements": OrderedDict([("foo", ""), ("bar", ">=5.0.0")]),
        }
    )


def test_get_layer_context_with_extra(fixtures_path: Path, template_two: Template):
    layer_conf = LayerConfig(
        template=template_two, initial_context={"project_slug": "{{ cookiecutter.repo_slug }}"}, no_input=True
    )
    user_config = get_user_config(config_file=None, default_config=False)
    full_context = Context(
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "repo_slug": "fake-project-template-two",
            "service_name": "foo",
            "_requirements": {"foo": "", "bar": ">=5.0.0"},
        }
    )
    context = layers.get_layer_context(layer_conf, user_config, full_context)

    assert context == Context(
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "project_slug": "fake-project-template-two",
            "_requirements": OrderedDict([("bar", ">=5.0.0"), ("baz", "")]),
            "lower_project_name": "fake project template2",
            "repo_slug": "fake-project-template-two",
            "service_name": "foo",
        },
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "repo_slug": "fake-project-template-two",
            "service_name": "foo",
            "_requirements": {"foo": "", "bar": ">=5.0.0"},
        },
    )


@pytest.mark.parametrize(
    "value, num_layers, expected",
    [
        ("yes", 3, ["yes", "yes", "yes"]),
        ("all", 3, ["yes", "yes", "yes"]),
        ("no", 3, ["no", "no", "no"]),
        ("none", 3, ["no", "no", "no"]),
        ("first", 3, ["yes", "no", "no"]),
        ("last", 3, ["no", "no", "yes"]),
        ("ask", 3, ["ask", "ask", "ask"]),
        ("what", 3, ["ask", "ask", "ask"]),
    ],
)
def test_get_accept_hooks_per_layer(value: str, num_layers: int, expected: list):
    assert layers.get_accept_hooks_per_layer(value, num_layers) == expected


def test_get_template_rendered_name(template_one: Template):
    context = Context({"cookiecutter": {"repo_name": "fake-project-template"}})
    assert layers.get_template_rendered_name(template_one, context) == "fake-project-template"
