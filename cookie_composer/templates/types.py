"""
Datatypes for templates.

Templates are a representation of source templates used to generate projects.
"""
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class Locality(str, Enum):
    """The locality of a template."""

    LOCAL = "local"
    REMOTE = "remote"


class TemplateFormat(str, Enum):
    """The format of a template."""

    ZIP = "zip"
    GIT = "git"
    HG = "hg"
    PLAIN = "plain"
    """A plain directory that isn't under version control."""


@dataclass
class TemplateRepo:
    """
    A template repository is a source of one or more templates.
    """

    source: str
    """The original path or URL to the template."""

    cached_source: Path
    """The path to the locally cached template."""

    format: TemplateFormat
    """The format of the template."""

    locality: Locality
    """Is the template local or remote?"""

    checkout: Optional[str] = None
    """The branch, tag or commit to tell Cookie Cutter to use."""

    password: Optional[str] = None
    """The password to use if template is a password-protected Zip archive."""


@dataclass
class Template:
    """A template is the combination of a template repository and a directory containing a cookiecutter.json file."""

    repo: TemplateRepo
    """The source of the template."""

    directory: str = ""
    """The directory within the repository that contains the cookiecutter.json file."""

    def cleanup(self) -> None:
        """Remove the cached template if it is a Zipfile."""
        if self.repo.format == TemplateFormat.ZIP and self.repo.cached_source.exists():
            shutil.rmtree(self.repo.cached_source)
