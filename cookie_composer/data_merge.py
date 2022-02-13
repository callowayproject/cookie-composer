"""Tools for merging data."""
from typing import Any, Iterable

import copy
from functools import reduce


def deep_merge(*dicts) -> dict:
    """
    Merges dicts deeply.

    Args:
        dicts: List of dicts to merge with the first one the base

    Returns:
        dict: The merged dict
    """

    def merge_into(d1, d2):
        for key in d2:
            if key not in d1 or not isinstance(d1[key], dict):
                d1[key] = copy.deepcopy(d2[key])
            else:
                d1[key] = merge_into(d1[key], d2[key])
        return d1

    return reduce(merge_into, dicts, {})


def merge_iterables(iter1: Iterable, iter2: Iterable) -> set:
    """
    Merge and de-duplicate a bunch of lists into a single list.

    Order is not guaranteed.

    Args:
        iter1: An Iterable
        iter2: An Iterable

    Returns:
        The merged, de-duplicated sequence as a set
    """
    from itertools import chain

    return set(chain(iter1, iter2))


def comprehensive_merge(*args) -> Any:
    """
    Merges data comprehensively.

    All arguments must be of the same type.

    - Scalars are overwritten by the new values
    - lists are merged and de-duplicated
    - dicts are recursively merged

    Args:
        args: List of dicts to merge with the first one the base

    Returns:
        The merged data

    Raises:
        ValueError: If the values are not of the same type
    """

    def merge_into(d1, d2):
        if type(d1) != type(d2):
            raise ValueError(f"Cannot merge {type(d2)} into {type(d1)}.")

        if isinstance(d1, list):
            return list(merge_iterables(d1, d2))
        elif isinstance(d1, set):
            return merge_iterables(d1, d2)
        elif isinstance(d1, tuple):
            return tuple(merge_iterables(d1, d2))
        elif isinstance(d1, dict):
            for key in d2:
                if key in d1:
                    d1[key] = merge_into(d1[key], d2[key])
                else:
                    d1[key] = copy.deepcopy(d2[key])
            return d1
        else:
            return copy.deepcopy(d2)

    if isinstance(args[0], list):
        return reduce(merge_into, args, [])
    elif isinstance(args[0], tuple):
        return reduce(merge_into, args, tuple())
    elif isinstance(args[0], set):
        return reduce(merge_into, args, set())
    elif isinstance(args[0], dict):
        return reduce(merge_into, args, {})
    else:
        return reduce(merge_into, args)
