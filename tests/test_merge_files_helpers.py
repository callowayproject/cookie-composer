"""Test the merge_files.helpers functions."""
from typing import Any

import pytest
from pytest import param
from cookie_composer import data_merge


@pytest.mark.parametrize(
    ["dict_list", "expected"],
    [
        param([{"a": 1}, {"a": 2}], {"a": 2}, id="dict 2 overwrites dict 1"),
        param([{"a": 1}, {"b": 2}], {"a": 1, "b": 2}, id="simple dict merge"),
        param(
            [{"a": {"b": 2}}, {"a": {"b": 3}}],
            {"a": {"b": 3}},
            id="nested dict 2 overwrites nested dict 1",
        ),
        param(
            [{"a": {"b": 1}}, {"a": {"c": 2}}],
            {"a": {"b": 1, "c": 2}},
            id="merge nested dicts",
        ),
    ],
)
def test_deepmerge(dict_list: list, expected: dict):
    """
    Make sure the deep merge is doing the right thing
    """
    assert data_merge.deep_merge(*dict_list) == expected


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        param([{"a": 1}, {"a": 2}], {"a": 2}, id="dict 2 scalars overwrites dict 1"),
        param([{"a": 1}, {"b": 2}], {"a": 1, "b": 2}, id="simple dict merge"),
        param(
            [{"a": {"b": 2}}, {"a": {"b": 3}}],
            {"a": {"b": 3}},
            id="nested dict 2 scalars overwrites nested dict 1 scalars",
        ),
        param(
            [{"a": {"b": 1}}, {"a": {"c": 2}}],
            {"a": {"b": 1, "c": 2}},
            id="merge nested dicts",
        ),
        param([[1, 2], [2, 3]], [1, 2, 3], id="merge lists"),
        param([(1, 2), (2, 3)], (1, 2, 3), id="merge tuples"),
        param([{1, 2}, {2, 3}], {1, 2, 3}, id="merge sets"),
        param([{"a": [1]}, {"a": [2]}], {"a": [1, 2]}, id="dict 2 iterable merges with dict 1 iterable"),
        param([1, 2], 2, id="scalar 2 overwrites scalar 1"),
    ],
)
def test_comprehensive_merge(args: list, expected: Any):
    """
    Make sure the deep merge is doing the right thing
    """
    assert data_merge.comprehensive_merge(*args) == expected


def test_comprehensive_merge_bad_types():
    """
    Make sure it raises an error if the types are not the same.
    """
    with pytest.raises(ValueError):
        data_merge.comprehensive_merge([1, 2], (2, 3))
