"""Tests for the utils module."""
import pytest
from pytest import param

from cookie_composer import utils
from cookie_composer.composition import read_rendered_composition


def test_get_context_for_layer(fixtures_path):
    """Return a context for a given layer."""
    rendered_comp = read_rendered_composition(fixtures_path / "rendered_composition.yaml")

    result1 = utils.get_context_for_layer(rendered_comp, 0)
    assert result1 == rendered_comp.layers[0].new_context

    result2 = utils.get_context_for_layer(rendered_comp, 1)
    assert "project_slug" in result2
    assert len(result2) == len(result1) + 1

    result3 = utils.get_context_for_layer(rendered_comp, 2)
    assert "_docs_requirements" in result3
    assert len(result3) == len(result2) + 1

    result4 = utils.get_context_for_layer(rendered_comp)
    assert result4 == result3


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("/path/to/template/", "template", id="local directory"),
        param("/path/to/composition.yaml", "composition", id="local composition"),
        param("https://example.com/path/to/template", "template", id="remote directory"),
        param("https://example.com/path/to/composition.yaml", "composition", id="remote composition"),
    ],
)
def test_get_template_name(value, expected):
    """The template name should be the base name of the path."""
    assert utils.get_template_name(value) == expected


@pytest.mark.parametrize(
    ["bad_value"],
    [
        ("https://example.com",),
        ("",),
    ],
)
def test_get_template_name_errors(bad_value):
    """It should raise errors"""
    with pytest.raises(ValueError):
        utils.get_template_name(bad_value)
