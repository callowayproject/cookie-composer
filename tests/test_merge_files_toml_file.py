"""Test merging TOML files."""
import shutil

import pytest
import toml

from cookie_composer.data_merge import DO_NOT_MERGE, NESTED_OVERWRITE, OVERWRITE, COMPREHENSIVE
from cookie_composer.exceptions import MergeError
from cookie_composer.merge_files import toml_file


def test_do_not_merge(fixtures_path):
    """This should raise an exception."""
    with pytest.raises(MergeError):
        existing_file = fixtures_path / "existing.toml"
        new_file = fixtures_path / "new.toml"
        toml_file.merge_toml_files(new_file, existing_file, DO_NOT_MERGE)


def test_overwrite_merge(tmp_path, fixtures_path):
    """The new overwrites the old."""
    initial_file = fixtures_path / "existing.toml"
    existing_file = tmp_path / "existing.toml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.toml"

    toml_file.merge_toml_files(new_file, existing_file, OVERWRITE)
    rendered = toml.load(existing_file)
    assert rendered == {
        "section1": {
            "number": 2,
            "string": "def",
            "list": ["a", "2"],
            "dictionary": {"b": [3, 2]},
            "list_of_dicts": [{"e": 1}, {"f": 3}],
        }
    }


def test_overwrite_nested_merge(tmp_path, fixtures_path):
    """Test using the nested overwrite merge strategy."""
    initial_file = fixtures_path / "existing.toml"
    existing_file = tmp_path / "existing.toml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.toml"
    toml_file.merge_toml_files(new_file, existing_file, NESTED_OVERWRITE)
    rendered = toml.load(existing_file)
    assert rendered == {
        "section1": {
            "number": 2,
            "string": "def",
            "list": ["a", "2"],
            "dictionary": {"a": 1, "b": [3, 2]},
            "list_of_dicts": [{"e": 1}, {"f": 3}],
        }
    }


def test_comprehensive_merge(tmp_path, fixtures_path):
    """Merge using the comprehensive_merge strategy."""
    initial_file = fixtures_path / "existing.toml"
    existing_file = tmp_path / "existing.toml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.toml"
    toml_file.merge_toml_files(new_file, existing_file, COMPREHENSIVE)
    rendered = toml.load(existing_file)
    assert rendered["section1"]["number"] == 2
    assert rendered["section1"]["string"] == "def"
    assert set(rendered["section1"]["list"]) == {"a", "1", "2", "c"}
    assert rendered["section1"]["dictionary"]["a"] == 1
    assert set(rendered["section1"]["dictionary"]["b"]) == {1, 2, 3}


def test_bad_files(tmp_path, fixtures_path):
    """Missing files should raise an error."""
    with pytest.raises(MergeError):
        toml_file.merge_toml_files(
            fixtures_path / "missing.toml",
            fixtures_path / "new.toml",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        toml_file.merge_toml_files(
            fixtures_path / "existing.toml",
            fixtures_path / "missing.toml",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        toml_file.merge_toml_files(
            fixtures_path / "gibberish.txt",
            fixtures_path / "new.json",
            OVERWRITE,
        )


def test_bad_strategy(tmp_path, fixtures_path):
    """A bad strategy should raise an error."""
    initial_file = fixtures_path / "existing.toml"
    existing_file = tmp_path / "existing.toml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.toml"

    with pytest.raises(MergeError):
        toml_file.merge_toml_files(new_file, existing_file, "not-a-stragegy")
