"""Merge two toml files into one."""
from pathlib import Path

import toml

from cookie_composer import data_merge
from cookie_composer.composition import (
    COMPREHENSIVE,
    DO_NOT_MERGE,
    NESTED_OVERWRITE,
    OVERWRITE,
)
from cookie_composer.exceptions import MergeError


def merge_toml_files(new_file: Path, existing_file: Path, merge_strategy: str):
    """
    Merge two toml files into one.

    Args:
        new_file: The path to the data file to merge
        existing_file: The path to the data file to merge into and write out.
        merge_strategy: How to do the merge

    Raises:
        MergeError: If something goes wrong
    """
    if merge_strategy == DO_NOT_MERGE:
        raise MergeError(
            str(new_file),
            str(existing_file),
            merge_strategy,
            "Can not merge with do-not-merge strategy.",
        )

    try:
        new_data = toml.loads(new_file.read_text())
        existing_data = toml.loads(existing_file.read_text())
    except (toml.TomlDecodeError, FileNotFoundError, TypeError) as e:
        raise MergeError(str(new_file), str(existing_file), merge_strategy, str(e)) from e

    if merge_strategy == OVERWRITE:
        existing_data.update(new_data)
    elif merge_strategy == NESTED_OVERWRITE:
        existing_data = data_merge.deep_merge(existing_data, new_data)
    elif merge_strategy == COMPREHENSIVE:
        existing_data = data_merge.comprehensive_merge(existing_data, new_data)
    else:
        raise MergeError(error_message=f"Unrecognized merge strategy {merge_strategy}")

    existing_file.write_text(toml.dumps(existing_data))
