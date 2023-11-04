"""Merge two .ini files into one."""
import configparser
from collections import defaultdict
from pathlib import Path
from typing import Dict

from cookie_composer import data_merge
from cookie_composer.data_merge import COMPREHENSIVE, DO_NOT_MERGE, NESTED_OVERWRITE, OVERWRITE
from cookie_composer.exceptions import MergeError


def merge_ini_files(new_file: Path, existing_file: Path, merge_strategy: str) -> None:
    """
    Merge two INI files into one.

    Raises:
        MergeError: If something goes wrong

    Args:
        new_file: The path to the data file to merge
        existing_file: The path to the data file to merge into and write out.
        merge_strategy: How to do the merge
    """
    if merge_strategy == DO_NOT_MERGE:
        raise MergeError(
            str(new_file),
            str(existing_file),
            merge_strategy,
            "Can not merge with do-not-merge strategy.",
        )
    try:
        existing_config = configparser.ConfigParser()
        existing_config.read_file(existing_file.open())

        if merge_strategy == OVERWRITE:
            new_config = configparser.ConfigParser()
            new_config.read_file(new_file.open())
            existing_config.update(new_config)
        elif merge_strategy == NESTED_OVERWRITE:
            existing_config.read(new_file)
        elif merge_strategy == COMPREHENSIVE:
            new_config = configparser.ConfigParser()
            new_config.read_file(new_file.open())
            new_config_dict = config_to_dict(new_config)
            existing_config_dict = config_to_dict(existing_config)
            existing_config_dict = data_merge.comprehensive_merge(existing_config_dict, new_config_dict)
            existing_config = dict_to_config(existing_config_dict)
        else:
            raise MergeError(error_message=f"Unrecognized merge strategy {merge_strategy}")
    except (configparser.Error, FileNotFoundError) as e:
        raise MergeError(str(new_file), str(existing_file), merge_strategy, str(e)) from e

    existing_config.write(existing_file.open("w"))


def config_to_dict(config: configparser.ConfigParser) -> dict:
    """Convert a configparser object to a dictionary."""
    result: Dict[str, dict] = defaultdict(dict)

    for section in config.sections():
        for k, v in config.items(section):
            result[section][k] = v.strip().split("\n") if "\n" in v else v

    return result


def dict_to_config(dictionary: dict) -> configparser.ConfigParser:
    """Convert a dict to a configparser object."""
    result = configparser.ConfigParser()

    for section, items in dictionary.items():
        result.add_section(section)
        for k, v in items.items():
            result.set(section, k, "\n" + "\n".join(v) if isinstance(v, list) else v)

    return result
