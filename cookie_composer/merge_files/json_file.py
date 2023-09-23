"""Merge two json files into one."""
from pathlib import Path
from typing import Any

import orjson

from cookie_composer import data_merge
from cookie_composer.data_merge import COMPREHENSIVE, DO_NOT_MERGE, NESTED_OVERWRITE, OVERWRITE
from cookie_composer.exceptions import MergeError


def default(obj: Any) -> dict:
    """Default JSON encoder."""
    from immutabledict import immutabledict

    if isinstance(obj, immutabledict):
        return dict(obj)
    raise TypeError


def merge_json_files(new_file: Path, existing_file: Path, merge_strategy: str) -> None:
    """
    Merge two json files into one.

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
        new_data = orjson.loads(new_file.read_text())
        existing_data = orjson.loads(existing_file.read_text())
    except (orjson.JSONDecodeError, FileNotFoundError) as e:
        raise MergeError(str(new_file), str(existing_file), merge_strategy, str(e)) from e

    if merge_strategy == OVERWRITE:
        existing_data.update(new_data)
    elif merge_strategy == NESTED_OVERWRITE:
        existing_data = data_merge.deep_merge(existing_data, new_data)
    elif merge_strategy == COMPREHENSIVE:
        existing_data = data_merge.comprehensive_merge(existing_data, new_data)
    else:
        raise MergeError(error_message=f"Unrecognized merge strategy {merge_strategy}")

    existing_file.write_text(orjson.dumps(existing_data, default=default).decode("utf-8"))
