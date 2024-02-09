"""Tests for the template types module."""

import pytest
from pytest import param

from cookie_composer.templates.types import get_template_name


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("/path/to/template/", "template", id="local directory"),
        param("/path/to/composition.yaml", "composition", id="local composition"),
        param("https://example.com/path/to/template", "template", id="remote directory"),
        param("https://example.com/path/to/composition.yaml", "composition", id="remote composition"),
    ],
)
def test_get_template_name(value: str, expected: str):
    """The template name should be the base name of the path."""
    assert get_template_name(value) == expected


@pytest.mark.parametrize(
    ["bad_value"],
    [
        ("https://example.com",),
        ("",),
    ],
)
def test_get_template_name_errors(bad_value):
    """It should raise errors."""
    with pytest.raises(ValueError):
        get_template_name(bad_value)
