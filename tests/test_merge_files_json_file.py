"""Test merging JSON files."""

import json
import shutil

import pytest

from cookie_composer.data_merge import DO_NOT_MERGE, NESTED_OVERWRITE, OVERWRITE, COMPREHENSIVE
from cookie_composer.exceptions import MergeError
from cookie_composer.merge_files import json_file


def test_do_not_merge(fixtures_path):
    """This should raise an exception."""
    with pytest.raises(MergeError):
        existing_file = fixtures_path / "existing.json"
        new_file = fixtures_path / "new.json"
        json_file.merge_json_files(new_file, existing_file, DO_NOT_MERGE)


def test_overwrite_merge(tmp_path, fixtures_path):
    initial_file = fixtures_path / "existing.json"
    existing_file = tmp_path / "existing.json"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.json"
    json_file.merge_json_files(new_file, existing_file, OVERWRITE)
    rendered = json.loads(existing_file.read_text())
    assert rendered == {
        "number": 2,
        "string": "def",
        "list": ["a", 2],
        "dictionary": {"b": [3, 2]},
        "list_of_dicts": [{"e": 1}, {"f": 3}],
    }


def test_overwrite_nested_merge(tmp_path, fixtures_path):
    """Test using the nested overwrite merge strategy."""
    initial_file = fixtures_path / "existing.json"
    existing_file = tmp_path / "existing.json"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.json"
    json_file.merge_json_files(new_file, existing_file, NESTED_OVERWRITE)
    rendered = json.loads(existing_file.read_text())
    assert rendered == {
        "number": 2,
        "string": "def",
        "list": ["a", 2],
        "dictionary": {"a": 1, "b": [3, 2]},
        "list_of_dicts": [{"e": 1}, {"f": 3}],
    }


def test_comprehensive_merge(tmp_path, fixtures_path):
    """Merge using the comprehensive_merge strategy."""
    initial_file = fixtures_path / "existing.json"
    existing_file = tmp_path / "existing.json"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.json"
    json_file.merge_json_files(new_file, existing_file, COMPREHENSIVE)
    rendered = json.loads(existing_file.read_text())
    assert rendered["number"] == 2
    assert rendered["string"] == "def"
    assert set(rendered["list"]) == {"a", 1, 2, "c"}
    assert rendered["dictionary"]["a"] == 1
    assert set(rendered["dictionary"]["b"]) == {1, 2, 3}


def test_bad_files(fixtures_path):
    """Missing files should raise an error."""
    with pytest.raises(MergeError):
        json_file.merge_json_files(
            fixtures_path / "missing.json",
            fixtures_path / "new.json",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        json_file.merge_json_files(
            fixtures_path / "existing.json",
            fixtures_path / "missing.json",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        json_file.merge_json_files(
            fixtures_path / "gibberish.txt",
            fixtures_path / "new.json",
            OVERWRITE,
        )


def test_bad_strategy(tmp_path, fixtures_path):
    """A bad strategy should raise an error."""
    existing_file = fixtures_path / "existing.json"
    new_file = fixtures_path / "new.json"
    with pytest.raises(MergeError):
        json_file.merge_json_files(new_file, existing_file, "not-a-stragegy")
