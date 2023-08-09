from pathlib import Path

import pytest

from cookie_composer import composition, layers
from cookie_composer.composition import LayerConfig
from cookie_composer.exceptions import MissingCompositionFileError


def test_multiple_templates(fixtures_path):
    filepath = fixtures_path / "multi-template.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 2
    assert comp.layers[0].template == str(fixtures_path / "template1")
    assert comp.layers[1].template == str(fixtures_path / "template2")


def test_relative_templates(fixtures_path):
    filepath = fixtures_path / "relative-multi-template.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 2
    assert comp.layers[0].template == f"{fixtures_path!s}/"
    assert comp.layers[1].template == f"{fixtures_path!s}/"


def test_single_template(fixtures_path):
    filepath = fixtures_path / "single-template.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 1
    assert comp.layers[0].template == str(fixtures_path / "tests/fixtures/template1")


def test_is_composition_file():
    assert composition.is_composition_file("single-template.yaml")
    assert composition.is_composition_file("single-template.yml")
    assert not composition.is_composition_file("single-template.txt")


def test_missing_composition():
    with pytest.raises(MissingCompositionFileError):
        composition.read_composition("/does/not/exist")


def test_empty_composition(fixtures_path):
    filepath = fixtures_path / "empty.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 0


def test_write_composition(tmp_path):
    """Test writing out layers."""
    layers = [
        LayerConfig(template=str(tmp_path / "tests/fixtures/template1")),
        LayerConfig(template=str(tmp_path / "tests/fixtures/template2")),
    ]
    filepath = tmp_path / "composition.yaml"
    composition.write_composition(layers, filepath)
    comp = composition.read_composition(filepath)
    assert comp.layers[0] == layers[0]
    assert comp.layers[1] == layers[1]


def test_get_composition_from_path_or_url_composition(fixtures_path: Path):
    """The paths should generate the correct Composition."""
    filepath = fixtures_path / "single-template.yaml"
    expected = composition.Composition(layers=[LayerConfig(template=str(fixtures_path / "tests/fixtures/template1"))])
    assert composition.get_composition_from_path_or_url(str(filepath), skip_if_file_exists=True) == expected


def test_get_composition_from_path_or_url_path(fixtures_path: Path):
    """The paths should generate the correct Composition."""
    filepath = fixtures_path / "template1"
    expected = composition.Composition(layers=[LayerConfig(template=str(filepath), skip_if_file_exists=False)])
    assert composition.get_composition_from_path_or_url(str(filepath)) == expected


def test_layer_contexts_are_not_overwritten(fixtures_path: Path, tmp_path: Path):
    """Test that layer contexts are not overwritten when reading a composition."""
    filepath = fixtures_path / "overwritten-context-comp.yaml"
    comp = composition.read_composition(filepath)
    rendered_layers = layers.render_layers(comp.layers, tmp_path, None, no_input=True)
    # rendered_project = tmp_path / rendered_layers[0].rendered_name
    rendered_composition = composition.RenderedComposition(
        layers=rendered_layers,
        render_dir=tmp_path,
        rendered_name=rendered_layers[0].rendered_name,
    )
    assert rendered_composition.layers[0].new_context["service_name"] == "frontend"
    assert rendered_composition.layers[1].new_context["service_name"] == "backend"
    assert rendered_composition.layer_names == ["template1", "template2"]
