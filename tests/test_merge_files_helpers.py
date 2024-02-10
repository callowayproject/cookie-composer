"""Test the merge_files.helpers functions."""

from collections import OrderedDict
from typing import Any

import pytest
from immutabledict import immutabledict
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
    Make sure the deep merge is doing the right thing.
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
        param(
            [{"a": [1]}, {"a": [2]}],
            {"a": [1, 2]},
            id="dict 2 iterable merges with dict 1 iterable",
        ),
        param([1, 2], 2, id="scalar 2 overwrites scalar 1"),
        param(
            [OrderedDict({"first": 1, "second": 2}), {"second": "two", "third": 3}],
            OrderedDict({"first": 1, "second": "two", "third": 3}),
            id="dict into ordered dict",
        ),
        param(
            [{"first": 1, "second": 2}, OrderedDict({"third": 3})],
            OrderedDict({"first": 1, "second": 2, "third": 3}),
            id="ordered dict into dict",
        ),
    ],
)
def test_comprehensive_merge(args: list, expected: Any):
    """
    Make sure the deep merge is doing the right thing.
    """
    assert data_merge.comprehensive_merge(*args) == expected


def test_comprehensive_merge_list_of_dicts():
    """A list of dicts should resolve into a list of immutabledicts in random order."""
    result = data_merge.comprehensive_merge([{"a": 1}, {"b": 2}], [{"c": 3}, {"d": 4}])
    expected = [
        immutabledict({"d": 4}),
        immutabledict({"c": 3}),
        immutabledict({"b": 2}),
        immutabledict({"a": 1}),
    ]
    assert isinstance(result, list)
    assert set(result) == set(expected)


def test_context_flatten():
    """Should return a merged dict."""
    context = data_merge.Context(
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "project_slug": "fake-project-template-two",
            "_requirements": OrderedDict([("bar", ">=5.0.0"), ("baz", "")]),
            "lower_project_name": "fake project template2",
        },
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "repo_slug": "fake-project-template-two",
            "_requirements": {"foo": "", "bar": ">=5.0.0"},
        },
    )
    expected = {
        "project_name": "Fake Project Template2",
        "repo_name": "fake-project-template2",
        "project_slug": "fake-project-template-two",
        "repo_slug": "fake-project-template-two",
        "_requirements": OrderedDict(
            [
                ("bar", ">=5.0.0"),
                ("baz", ""),
                ("foo", ""),
            ]
        ),
        "lower_project_name": "fake project template2",
    }
    assert context.flatten() == expected
