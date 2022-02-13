"""Test merging YAML files."""
import shutil

import pytest
from ruyaml import YAML

from cookie_composer.composition import MergeStrategy
from cookie_composer.exceptions import MergeError
from cookie_composer.merge_files import yaml_file

yaml = YAML(typ="safe")


def test_do_not_merge(fixtures_path):
    """This should raise an exception."""
    with pytest.raises(MergeError):
        existing_file = fixtures_path / "existing.yaml"
        new_file = fixtures_path / "new.yaml"
        yaml_file.merge_yaml_files(new_file, existing_file, MergeStrategy.DO_NOT_MERGE)


def test_overwrite_merge(tmp_path, fixtures_path):
    """the new overwrites the old."""
    initial_file = fixtures_path / "existing.yaml"
    existing_file = tmp_path / "existing.yaml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.yaml"

    yaml_file.merge_yaml_files(new_file, existing_file, MergeStrategy.OVERWRITE)
    rendered = yaml.load(existing_file)
    assert rendered == {
        "number": 2,
        "string": "def",
        "list": ["a", 2],
        "dictionary": {"b": [3, 2]},
    }


def test_overwrite_nested_merge(tmp_path, fixtures_path):
    """Test using the nested overwrite merge strategy."""
    initial_file = fixtures_path / "existing.yaml"
    existing_file = tmp_path / "existing.yaml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.yaml"
    yaml_file.merge_yaml_files(new_file, existing_file, MergeStrategy.NESTED_OVERWRITE)
    rendered = yaml.load(existing_file)
    assert rendered == {
        "number": 2,
        "string": "def",
        "list": ["a", 2],
        "dictionary": {"a": 1, "b": [3, 2]},
    }


def test_comprehensive_merge(tmp_path, fixtures_path):
    """Merge using the comprehensive_merge strategy."""
    initial_file = fixtures_path / "existing.yaml"
    existing_file = tmp_path / "existing.yaml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.yaml"
    yaml_file.merge_yaml_files(new_file, existing_file, MergeStrategy.COMPREHENSIVE)
    rendered = yaml.load(existing_file)
    assert rendered["number"] == 2
    assert rendered["string"] == "def"
    assert set(rendered["list"]) == {"a", 1, 2, "c"}
    assert rendered["dictionary"]["a"] == 1
    assert set(rendered["dictionary"]["b"]) == {1, 2, 3}


def test_bad_files(tmp_path, fixtures_path):
    """Missing files should raise an error."""
    with pytest.raises(MergeError):
        yaml_file.merge_yaml_files(
            fixtures_path / "missing.yaml",
            fixtures_path / "new.yaml",
            MergeStrategy.OVERWRITE,
        )

    with pytest.raises(MergeError):
        yaml_file.merge_yaml_files(
            fixtures_path / "existing.yaml",
            fixtures_path / "missing.yaml",
            MergeStrategy.OVERWRITE,
        )

    with pytest.raises(MergeError):
        yaml_file.merge_yaml_files(
            fixtures_path / "gibberish.txt",
            fixtures_path / "new.json",
            MergeStrategy.OVERWRITE,
        )


def test_bad_strategy(tmp_path, fixtures_path):
    """A bad strategy should raise an error."""
    initial_file = fixtures_path / "existing.yaml"
    existing_file = tmp_path / "existing.yaml"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.yaml"

    with pytest.raises(MergeError):
        print(f"{new_file=}")
        print(f"{existing_file=}")
        yaml_file.merge_yaml_files(new_file, existing_file, "not-a-stragegy")
