"""Tools for merging data."""

import copy
import logging
from collections import ChainMap, OrderedDict
from functools import reduce
from pathlib import Path
from typing import Any, Dict, Iterable, MutableMapping

from immutabledict import immutabledict

from cookie_composer.matching import rel_fnmatch

logger = logging.getLogger(__name__)


def deep_merge(*dicts: dict) -> dict:
    """
    Merges dicts deeply.

    Args:
        *dicts: List of dicts to merge with the first one as the base

    Returns:
        dict: The merged dict
    """

    def merge_into(d1: dict, d2: dict) -> dict:
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

    return set(chain(freeze_data(iter1), freeze_data(iter2)))


def comprehensive_merge(*args: MutableMapping) -> Any:  # noqa: C901
    """
    Merges data comprehensively.

    All arguments must be of the same type.

    - Scalars are overwritten by the new values
    - lists are merged and de-duplicated
    - dicts are recursively merged

    Args:
        *args: List of dicts to merge with the first one the base

    Returns:
        The merged data
    """
    dict_types = (dict, OrderedDict, immutabledict)
    iterable_types = (list, set, tuple)

    def merge_into(d1: Any, d2: Any) -> Any:
        if isinstance(d1, dict_types) and isinstance(d2, dict_types):
            if isinstance(d1, OrderedDict) or isinstance(d2, OrderedDict):
                od1: MutableMapping[Any, Any] = OrderedDict(d1)
                od2: MutableMapping[Any, Any] = OrderedDict(d2)
            else:
                od1 = dict(d1)
                od2 = dict(d2)

            for key in od2:
                od1[key] = merge_into(od1[key], od2[key]) if key in od1 else copy.deepcopy(od2[key])
            return od1  # type: ignore[return-value]
        elif isinstance(d1, list) and isinstance(d2, iterable_types):
            return list(merge_iterables(d1, d2))
        elif isinstance(d1, set) and isinstance(d2, iterable_types):
            return merge_iterables(d1, d2)
        elif isinstance(d1, tuple) and isinstance(d2, iterable_types):
            return tuple(merge_iterables(d1, d2))
        else:
            return copy.deepcopy(d2)

    if isinstance(args[0], list):
        return reduce(merge_into, args, [])
    elif isinstance(args[0], tuple):
        return reduce(merge_into, args, ())
    elif isinstance(args[0], set):
        return reduce(merge_into, args, set())
    elif isinstance(args[0], dict_types):
        return reduce(merge_into, args, {})
    else:
        return reduce(merge_into, args)


class Context(ChainMap):
    """Provides merging and convenience functions for managing contexts."""

    @property
    def is_empty(self) -> bool:
        """The context has only one mapping and it is empty."""
        return len(self.maps) == 1 and len(self.maps[0]) == 0

    def flatten(self) -> MutableMapping:
        """Comprehensively merge all the maps into a single mapping."""
        return reduce(comprehensive_merge, self.maps, {})


def freeze_data(obj: Any) -> Any:
    """Check type and recursively return a new read-only object."""
    if isinstance(obj, (str, int, float, bytes, type(None), bool)):
        return obj
    elif isinstance(obj, tuple) and type(obj) != tuple:  # assumed namedtuple
        return type(obj)(*(freeze_data(i) for i in obj))
    elif isinstance(obj, (tuple, list)):
        return tuple(freeze_data(i) for i in obj)
    elif isinstance(obj, (dict, OrderedDict, immutabledict)):
        return immutabledict({k: freeze_data(v) for k, v in obj.items()})
    elif isinstance(obj, (set, frozenset)):
        return frozenset(freeze_data(i) for i in obj)
    raise ValueError(obj)


# Strategies merging files and data.
DO_NOT_MERGE = "do-not-merge"
"""Do not merge the data, use the file path to determine what to do."""

NESTED_OVERWRITE = "nested-overwrite"
"""Merge deeply nested structures and overwrite at the lowest level; A deep ``dict.update()``."""

OVERWRITE = "overwrite"
"""Overwrite at the top level like ``dict.update()``."""

COMPREHENSIVE = "comprehensive"
"""Comprehensively merge the two data structures.

- Scalars are overwritten by the new values
- lists are merged and de-duplicated
- dicts are recursively merged
"""


def get_merge_strategy(path: Path, merge_strategies: Dict[str, str]) -> str:
    """
    Return the merge strategy of the path based on the layer configured rules.

    Files that are not mergable return :attr:`~cookie_composer.composition.DO_NOT_MERGE`

    Args:
        path: The file path to evaluate.
        merge_strategies: The glob pattern->strategy mapping

    Returns:
        The appropriate merge strategy.
    """
    from cookie_composer.merge_files import MERGE_FUNCTIONS

    strategy = DO_NOT_MERGE  # The default

    if path.suffix not in MERGE_FUNCTIONS:
        return DO_NOT_MERGE

    for pattern, strat in merge_strategies.items():
        if rel_fnmatch(str(path), pattern):
            logger.debug(f"{path} matches merge strategy pattern {pattern} for {strat}")
            strategy = strat
            break

    return strategy
