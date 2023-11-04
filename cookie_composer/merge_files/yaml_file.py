"""Merge two json files into one."""

from pathlib import Path

from immutabledict import ImmutableOrderedDict, immutabledict

from cookie_composer import data_merge
from cookie_composer.data_merge import COMPREHENSIVE, DO_NOT_MERGE, NESTED_OVERWRITE, OVERWRITE
from cookie_composer.exceptions import MergeError


def merge_yaml_files(new_file: Path, existing_file: Path, merge_strategy: str) -> None:
    """
    Merge two json files into one.

    Args:
        new_file: The path to the data file to merge
        existing_file: The path to the data file to merge into and write out.
        merge_strategy: How to do the merge

    Raises:
        MergeError: If something goes wrong
    """
    from ruamel.yaml import YAML, SafeRepresenter, YAMLError

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.Representer.add_representer(immutabledict, SafeRepresenter.represent_dict)
    yaml.Representer.add_representer(ImmutableOrderedDict, SafeRepresenter.represent_dict)

    if merge_strategy == DO_NOT_MERGE:
        raise MergeError(
            str(new_file),
            str(existing_file),
            merge_strategy,
            "Can not merge with do-not-merge strategy.",
        )

    try:
        new_data = yaml.load(new_file)
        existing_data = yaml.load(existing_file)
    except (YAMLError, FileNotFoundError) as e:
        raise MergeError(str(new_file), str(existing_file), merge_strategy, str(e)) from e

    if merge_strategy == OVERWRITE:
        existing_file.write_text(new_file.read_text())
        return
    elif merge_strategy == NESTED_OVERWRITE:
        existing_data = data_merge.deep_merge(existing_data, new_data)
    elif merge_strategy == COMPREHENSIVE:
        existing_data = data_merge.comprehensive_merge(existing_data, new_data)
    else:
        raise MergeError(error_message=f"Unrecognized merge strategy {merge_strategy}")

    yaml.dump(existing_data, existing_file)
