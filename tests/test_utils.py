"""Tests for the utils module."""
from pathlib import Path

import pytest
from pytest import param

from cookie_composer.composition import get_context_for_layer
from cookie_composer import utils
from cookie_composer.io import read_rendered_composition


def test_get_context_for_layer(fixtures_path: Path):
    """Return a context for a given layer."""
    rendered_comp = read_rendered_composition(fixtures_path / "rendered_composition.yaml")

    result1 = get_context_for_layer(rendered_comp, 0)
    assert result1 == rendered_comp.layers[0].rendered_context

    result2 = get_context_for_layer(rendered_comp, 1)
    assert "project_slug" in result2
    assert len(result2) == len(result1) + 1

    result3 = get_context_for_layer(rendered_comp, 2)
    assert "_docs_requirements" in result3
    assert len(result3) == len(result2) + 1

    result4 = get_context_for_layer(rendered_comp)
    assert result4 == result3


def test_remove_single_path(tmp_path: Path):
    """It should remove a single path."""
    path = tmp_path / "file.txt"
    path.touch()
    utils.remove_single_path(path)
    assert not path.exists()

    path = tmp_path / "dir"
    path.mkdir()
    utils.remove_single_path(path)
    assert not path.exists()

    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    file_path = dir_path / "file.txt"
    file_path.touch()
    utils.remove_single_path(dir_path)
    assert not dir_path.exists()
