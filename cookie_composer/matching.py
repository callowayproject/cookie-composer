"""Matching files and patterns."""
from typing import List, Union

from fnmatch import fnmatch
from pathlib import Path


def rel_fnmatch(name: str, pat: str) -> bool:
    """Force a relative match of the pattern by prefixing a ``*``."""
    if pat.startswith("*"):
        return fnmatch(name, pat)
    else:
        return fnmatch(name, f"*{pat}")


def matches_any_glob(path: Union[str, Path], patterns: List[str]) -> bool:
    """
    Does the path match any of the glob patterns?

    Args:
        path: Path to test
        patterns: A list of glob patterns

    Returns:
        ``True`` if it matches any of the patterns
    """
    return any(rel_fnmatch(str(path), pat) for pat in patterns)
