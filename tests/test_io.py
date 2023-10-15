"""Tests for the io module."""
from pathlib import Path
from typing import Tuple

import pytest

from cookie_composer import io
from cookie_composer.layers import RenderedLayer, LayerConfig
from cookie_composer.templates.types import Template, TemplateRepo, Locality, TemplateFormat


@pytest.fixture
def rendered_layer_info(fixtures_path: Path) -> Tuple[dict, RenderedLayer]:
    """Return the default composition."""
    source = fixtures_path.joinpath("template1")
    layer_info = {
        "checkout": None,
        "commit": None,
        "context": {
            "_requirements": {"bar": ">=5.0.0", "foo": ""},
            "project_name": "Fake Project Template",
            "repo_name": "fake-project-template",
            "repo_slug": "fake-project-template",
        },
        "directory": "",
        "merge_strategies": {"*": "do-not-merge"},
        "no_input": True,
        "overwrite": [],
        "overwrite_exclude": [],
        "password": None,
        "skip_generation": [],
        "skip_hooks": False,
        "skip_if_file_exists": True,
        "template": str(source),
        "rendered_name": "fake-project-template",
    }
    rendered_layer = RenderedLayer(
        layer=LayerConfig(
            template=Template(
                repo=TemplateRepo(
                    source=str(fixtures_path.joinpath("template1")),
                    cached_source=source,
                    locality=Locality.LOCAL,
                    format=TemplateFormat.PLAIN,
                ),
                directory="",
            ),
            initial_context=layer_info["context"],
            no_input=layer_info["no_input"],
            overwrite=layer_info["overwrite"],
            overwrite_exclude=layer_info["overwrite_exclude"],
            skip_generation=layer_info["skip_generation"],
            skip_hooks=layer_info["skip_hooks"],
            skip_if_file_exists=layer_info["skip_if_file_exists"],
        ),
        rendered_name=layer_info["rendered_name"],
        rendered_context=layer_info["context"],
        rendered_commit=layer_info["commit"],
        location=fixtures_path,
    )
    return layer_info, rendered_layer


def test_deserialize_rendered_layer(rendered_layer_info: Tuple[dict, RenderedLayer], fixtures_path: Path):
    """A rendered layer dict should be serialized into a RenderedLayer."""
    layer_info = rendered_layer_info[0]
    expected_layer = rendered_layer_info[1]
    rendered_layer = io.deserialize_rendered_layer(layer_info, fixtures_path)
    assert rendered_layer == expected_layer


def test_serialize_rendered_layer(rendered_layer_info: Tuple[dict, RenderedLayer]):
    """A rendered layer should be serialized into a dict."""
    layer_info = rendered_layer_info[0]
    rendered_layer = rendered_layer_info[1]
    assert io.serialize_rendered_layer(rendered_layer) == layer_info
