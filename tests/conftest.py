"""Testing configuration."""
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_path() -> Path:
    """Return the path to the testing fixtures."""

    return Path(__file__).parent / "fixtures"
