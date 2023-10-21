"""
Datatypes for templates.

Templates are a representation of source templates used to generate projects.
"""
import json
import shutil
import tempfile
from collections import OrderedDict
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterator, Optional


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
    """The branch, tag or commit for the template to track."""

    password: Optional[str] = None
    """The password to use if template is a password-protected Zip archive."""

    @property
    def current_sha(self) -> Optional[str]:
        """If the template is a git repository, return the current commit hash."""
        from cookie_composer.git_commands import get_repo

        if self.format != TemplateFormat.GIT:
            return None

        template_repo = get_repo(self.cached_source, search_parent_directories=True)
        return template_repo.head.object.hexsha

    @property
    def latest_sha(self) -> Optional[str]:
        """
        Return the latest SHA of this template's repo.

        If the template is not a git repository, it will always return ``None``.

        Returns:
            The latest hexsha of the template or ``None`` if the template isn't a git repo
        """
        from cookie_composer.git_commands import get_repo

        if self.format != TemplateFormat.GIT:
            return None

        template_repo = get_repo(self.cached_source, search_parent_directories=True)
        if len(template_repo.remotes) > 0:
            template_repo.remotes[0].fetch()
            return template_repo.remotes[0].refs[0].commit.hexsha
        return template_repo.head.object.hexsha

    @contextmanager
    def render_source(self, output_dir: Optional[Path] = None, commit: Optional[str] = None) -> Iterator[Path]:
        """
        A context manager that provides the source from which to render the template.

        For git repositories, this will create a temporary working tree of the repository and yield the path
        to the working tree.

        For Zip archives, this will extract the archive to a temporary directory and yield the path

        For plain repos, it will yield the path to the directory.

        Args:
            output_dir: The directory to extract the template to. If not provided, a temporary directory will be used.
            commit: The commit to checkout if the template is a git repository.

        Yields:
            The path to the rendered template
        """
        output_dir = output_dir or Path(tempfile.mkdtemp())

        if self.format == TemplateFormat.GIT:
            from cookie_composer.git_commands import temp_git_worktree_dir

            with temp_git_worktree_dir(
                self.cached_source, output_dir, branch=self.checkout, commit=commit
            ) as worktree_dir:
                yield worktree_dir
        elif self.format == TemplateFormat.ZIP:
            from cookie_composer.templates.zipfile_repo import extract_zipfile

            zip_dir = extract_zipfile(self.cached_source, output_dir=output_dir, password=self.password)
            yield zip_dir
            shutil.rmtree(zip_dir)
        elif self.format == TemplateFormat.PLAIN:
            from cookie_composer.utils import temporary_copy

            with temporary_copy(self.cached_source) as temp_dir:
                yield temp_dir


@dataclass
class Template:
    """A template is the combination of a template repository and a directory containing a cookiecutter.json file."""

    repo: TemplateRepo
    """The source of the template."""

    directory: str = ""
    """The directory within the repository that contains the cookiecutter.json file."""

    _context: Optional[OrderedDict] = None

    def cleanup(self) -> None:
        """Remove the cached template if it is a Zipfile."""
        if self.repo.format == TemplateFormat.ZIP and self.repo.cached_source.exists():
            shutil.rmtree(self.repo.cached_source)

    @property
    def name(self) -> str:
        """The name of the template."""
        return get_template_name(
            path_or_url=self.repo.source,
            directory=self.directory,
            checkout=self.repo.checkout,
        )

    @property
    def cached_path(self) -> Path:
        """The path to the cached template."""
        if self.directory:
            return self.repo.cached_source / self.directory
        else:
            return self.repo.cached_source

    @property
    def context_file_path(self) -> Path:
        """The path to the template's context file."""
        if self.directory:
            return self.repo.cached_source / self.directory / "cookiecutter.json"
        else:
            return self.repo.cached_source / "cookiecutter.json"

    @property
    def context(self) -> dict:
        """The context of the template."""
        if self._context is None:
            self._context = json.loads(self.context_file_path.read_text(), object_pairs_hook=OrderedDict)
        return self._context


def get_template_name(path_or_url: str, directory: Optional[str] = None, checkout: Optional[str] = None) -> str:
    """
    Get the name of the template using the path or URL.

    Args:
        path_or_url: The URL or path to the template
        directory: Directory within a git repository template that holds the cookiecutter.json file.
        checkout: The branch, tag or commit to use if template is a git repository.

    Raises:
        ValueError: If the path_or_url is not parsable

    Returns:
        The name of the template without extensions
    """
    from urllib.parse import urlparse

    path = urlparse(path_or_url).path
    if not path:
        raise ValueError("There is no path.")

    base_path = Path(path).stem
    dir_name = Path(directory).name if directory else None
    parts = [base_path, dir_name, checkout]
    return "-".join([x for x in parts if x])
