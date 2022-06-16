"""Test layer rendering."""
import json
import os
import shutil
from pathlib import Path

from cookie_composer import layers
from cookie_composer.composition import LayerConfig, MergeStrategy, RenderedLayer
from cookie_composer.data_merge import comprehensive_merge


def test_render_layer(fixtures_path, tmp_path):
    """Test rendering a layer."""
    layer_conf = LayerConfig(template=str(fixtures_path / "template1"), no_input=True)
    rendered_layer = layers.render_layer(layer_conf, tmp_path)
    expected_context = json.loads(Path(fixtures_path / "template1/cookiecutter.json").read_text())
    expected_context["repo_name"] = "fake-project-template"
    expected = RenderedLayer(
        layer=layer_conf,
        location=tmp_path,
        new_context=expected_context,
    )
    assert rendered_layer == expected
    assert len(list(tmp_path.iterdir())) == 1


def test_get_write_strategy_skip_generation(fixtures_path):
    """Files matching a skip generation glob are skipped."""
    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        skip_generation=["README.md"],
        skip_if_file_exists=False,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "template1" / "{{cookiecutter.repo_name}}" / "README.md"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_dest_not_exist(tmp_path, fixtures_path):
    """If the destination path doesn't exist, return the write strategy."""

    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "template1" / "{{cookiecutter.repo_name}}" / "README.md"
    dest_path = tmp_path / "foo" / "README.md"
    assert layers.get_write_strategy(filepath, dest_path, rendered_layer) == layers.WriteStrategy.WRITE


def test_get_write_strategy_merge_strategy(fixtures_path):
    """Return the correct write strategy for mergable files."""

    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        merge_strategies={
            "*.yml": MergeStrategy.OVERWRITE,
            "*.yaml": MergeStrategy.OVERWRITE,
            "*.json": MergeStrategy.DO_NOT_MERGE,
        },
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.MERGE
    filepath = fixtures_path / "existing.json"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_overwrite_exclude(fixtures_path):
    """Return SKIP if the file matches an overwrite_exclude pattern."""

    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        overwrite_exclude=["*.yaml"],
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP


def test_get_write_strategy_overwrite(fixtures_path):
    """Return WRITE if the file matches an overwrite pattern."""

    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        overwrite=["*.yaml"],
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.WRITE


def test_get_write_strategy_skip_if_file_exists(fixtures_path):
    """Return SKIP or WRITE based on the skip_if_file_exists setting."""

    layer_config = LayerConfig(
        template=str(fixtures_path / "template1"),
        skip_if_file_exists=True,
    )
    rendered_layer = RenderedLayer(layer=layer_config, location=fixtures_path, new_context={})
    filepath = fixtures_path / "existing.yaml"
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.SKIP

    rendered_layer.layer.skip_if_file_exists = False
    assert layers.get_write_strategy(filepath, filepath, rendered_layer) == layers.WriteStrategy.WRITE


def test_merge_layers(tmp_path, fixtures_path):
    """Test merging layers together."""
    # copy rendered1 layer to temp dir
    rendered1 = fixtures_path / "rendered1"
    rendered_layer_path = shutil.copytree(rendered1, tmp_path, dirs_exist_ok=True)
    context1 = json.loads((rendered1 / "context.json").read_text())

    # create a rendered layer object for rendered2
    layer_config = LayerConfig(
        template=str(fixtures_path / "template2"),
        skip_if_file_exists=False,
        merge_strategies={
            "*.json": MergeStrategy.DO_NOT_MERGE,
            "*.yaml": MergeStrategy.OVERWRITE,
        },
    )
    context2 = json.loads((fixtures_path / "rendered2" / "context.json").read_text())
    full_context = comprehensive_merge(context1, context2)
    rendered2_config = RenderedLayer(
        layer=layer_config,
        location=fixtures_path / "rendered2",
        new_context=full_context,
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
