from pathlib import Path

import pytest

from cookie_composer import composition
from cookie_composer.composition import LayerConfig
from cookie_composer.exceptions import MissingCompositionFileError


def test_multiple_templates(fixtures_path):
    filepath = fixtures_path / "multi-template.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 2
    assert comp.layers[0].template == "tests/fixtures/template1"
    assert comp.layers[1].template == "tests/fixtures/template2"


def test_single_template(fixtures_path):
    filepath = fixtures_path / "single-template.yaml"
    comp = composition.read_composition(filepath)
    assert len(comp.layers) == 1
    assert comp.layers[0].template == "tests/fixtures/template1"


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
        LayerConfig(template="tests/fixtures/template1"),
        LayerConfig(template="tests/fixtures/template2"),
    ]
    filepath = tmp_path / "composition.yaml"
    composition.write_composition(layers, filepath)
    comp = composition.read_composition(filepath)
    assert comp.layers[0] == layers[0]
    assert comp.layers[1] == layers[1]
