"""Test merging INI files."""
import configparser
import shutil
from io import StringIO

import pytest

from cookie_composer.composition import (
    COMPREHENSIVE,
    DO_NOT_MERGE,
    NESTED_OVERWRITE,
    OVERWRITE,
)
from cookie_composer.exceptions import MergeError
from cookie_composer.merge_files import ini_file


def test_do_not_merge(fixtures_path):
    """This should raise an exception."""
    with pytest.raises(MergeError):
        existing_file = fixtures_path / "existing.ini"
        new_file = fixtures_path / "new.ini"
        ini_file.merge_ini_files(new_file, existing_file, DO_NOT_MERGE)


def test_overwrite_merge(tmp_path, fixtures_path):
    """The new overwrites the old."""
    initial_file = fixtures_path / "existing.ini"
    existing_file = tmp_path / "existing.ini"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.ini"

    ini_file.merge_ini_files(new_file, existing_file, OVERWRITE)

    rendered = existing_file.read_text()
    expected_config = configparser.ConfigParser()
    expected_config.read_dict(
        {
            "Section1": {
                "number": 2,
                "string": "def",
                "list": "\n".join(["", "a", "2"]),
            },
            "Section2.dictionary": {"b": "\n".join(["", "3", "2"])},
        }
    )
    expected = StringIO()
    expected_config.write(expected)
    assert rendered == expected.getvalue()


def test_overwrite_nested_merge(tmp_path, fixtures_path):
    """Test using the nested overwrite merge strategy."""
    initial_file = fixtures_path / "existing.ini"
    existing_file = tmp_path / "existing.ini"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.ini"
    ini_file.merge_ini_files(new_file, existing_file, NESTED_OVERWRITE)

    rendered = existing_file.read_text()
    expected_config = configparser.ConfigParser()
    expected_config.read_dict(
        {
            "Section1": {
                "number": 2,
                "string": "def",
                "list": "\n".join(["", "a", "2"]),
            },
            "Section2.dictionary": {"a": 1, "b": "\n".join(["", "3", "2"])},
        }
    )
    expected = StringIO()
    expected_config.write(expected)
    assert rendered == expected.getvalue()


def test_comprehensive_merge(tmp_path, fixtures_path):
    """Merge using the comprehensive_merge strategy."""
    initial_file = fixtures_path / "existing.ini"
    existing_file = tmp_path / "existing.ini"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.ini"
    ini_file.merge_ini_files(new_file, existing_file, COMPREHENSIVE)

    rendered = configparser.ConfigParser()
    rendered.read_file(existing_file.open())
    rendered_data = ini_file.config_to_dict(rendered)

    assert rendered_data["Section1"]["number"] == "2"
    assert rendered_data["Section1"]["string"] == "def"
    assert set(rendered_data["Section1"]["list"]) == {"a", "1", "2", "c"}
    assert rendered_data["Section2.dictionary"]["a"] == "1"
    assert set(rendered_data["Section2.dictionary"]["b"]) == {"1", "2", "3"}


def test_bad_files(tmp_path, fixtures_path):
    """Missing files should raise an error."""
    with pytest.raises(MergeError):
        ini_file.merge_ini_files(
            fixtures_path / "missing.ini",
            fixtures_path / "new.ini",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        ini_file.merge_ini_files(
            fixtures_path / "existing.ini",
            fixtures_path / "missing.ini",
            OVERWRITE,
        )

    with pytest.raises(MergeError):
        ini_file.merge_ini_files(
            fixtures_path / "gibberish.txt",
            fixtures_path / "new.json",
            OVERWRITE,
        )


def test_bad_strategy(tmp_path, fixtures_path):
    """A bad strategy should raise an error."""
    initial_file = fixtures_path / "existing.ini"
    existing_file = tmp_path / "existing.ini"
    shutil.copy(initial_file, existing_file)

    new_file = fixtures_path / "new.ini"

    with pytest.raises(MergeError):
        ini_file.merge_ini_files(new_file, existing_file, "not-a-stragegy")
