"""Exceptions raised when bad things happen."""
from typing import Optional


class MissingCompositionFileError(Exception):
    """The composition is missing or inaccessible."""

    def __init__(self, path_or_url: str):
        msg = f"The composition is missing or inaccessible at {path_or_url}"
        super().__init__(msg)


class MergeError(Exception):
    """There was a problem merging a file."""

    def __init__(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        strategy: Optional[str] = None,
        error_message: Optional[str] = "",
    ):
        if origin and destination and strategy:
            msg = f"There was a problem merging {origin} and {destination} using {strategy}: {error_message}"
            super().__init__(msg)
        super().__init__(error_message)
