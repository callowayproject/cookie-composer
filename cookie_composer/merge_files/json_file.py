"""Merge two json files into one."""
import json
from pathlib import Path

from cookie_composer import data_merge
from cookie_composer.composition import MergeStrategy
from cookie_composer.exceptions import MergeError


def merge_json_files(new_file: Path, existing_file: Path, merge_strategy: MergeStrategy):
    """
    Merge two json files into one.

    Args:
        new_file: The path to the data file to merge
        existing_file: The path to the data file to merge into and write out.
        merge_strategy: How to do the merge

    Raises:
        MergeError: If something goes wrong
    """
    if merge_strategy == MergeStrategy.DO_NOT_MERGE:
        raise MergeError(
            str(new_file),
            str(existing_file),
            str(merge_strategy),
            "Can not merge with do-not-merge strategy.",
        )

    try:
        new_data = json.loads(new_file.read_text())
        existing_data = json.loads(existing_file.read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise MergeError(str(new_file), str(existing_file), str(merge_strategy), str(e))

    if merge_strategy == MergeStrategy.OVERWRITE:
        existing_data.update(new_data)
    elif merge_strategy == MergeStrategy.NESTED_OVERWRITE:
        existing_data = data_merge.deep_merge(existing_data, new_data)
    elif merge_strategy == MergeStrategy.COMPREHENSIVE:
        existing_data = data_merge.comprehensive_merge(existing_data, new_data)
    else:
        raise MergeError(error_message=f"Unrecognized merge strategy {merge_strategy}")

    existing_file.write_text(json.dumps(existing_data))
