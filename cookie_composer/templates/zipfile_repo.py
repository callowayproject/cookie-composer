"""Utility functions for handling and fetching repo archives in zip format."""
import os
import tempfile
from pathlib import Path
from typing import Optional
from zipfile import BadZipFile, ZipFile

import requests
from cookiecutter.prompt import read_repo_password
from cookiecutter.utils import make_sure_path_exists, prompt_and_delete

from cookie_composer.exceptions import (
    EmptyZipRepositoryError,
    InvalidZipPasswordError,
    InvalidZipRepositoryError,
    NoZipDirectoryError,
)
from cookie_composer.templates.types import Locality, TemplateFormat, TemplateRepo


def template_repo_from_zipfile(
    zip_uri: str, locality: Locality, cache_dir: Path, no_input: bool = False, password: Optional[str] = None
) -> TemplateRepo:
    """Return a template repo from a zipfile URI."""
    cached_source = unzip(zip_uri, locality == Locality.REMOTE, cache_dir, no_input, password)
    return TemplateRepo(
        source=zip_uri,
        cached_source=cached_source,
        format=TemplateFormat.ZIP,
        locality=locality,
        checkout=None,
        password=password,
    )


def download_zipfile(url: str, cache_dir: Path, no_input: bool = False) -> Path:
    """Download a zipfile from a URL into the cache_dir."""
    filename = url.rsplit("/", 1)[1]
    zip_path = cache_dir.joinpath(filename)

    if zip_path.exists():
        download = prompt_and_delete(zip_path, no_input=no_input)
    else:
        download = True

    if download:
        # (Re) download the zipfile
        r = requests.get(url, stream=True, timeout=100)
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    return zip_path


def unzip(
    zip_uri: str,
    is_remote: bool,
    cache_dir: Path,
    no_input: bool = False,
    password: Optional[str] = None,
) -> Path:
    """
    Download and unpack a zipfile at a given URI.

    This will download the zipfile to the cookiecutter repository,
    and unpack into a temporary directory.

    Args:
        zip_uri: The URI for the zipfile.
        is_remote: Is the zip URI a URL or a file?
        cache_dir: The cookiecutter repository directory to put the archive into.
        no_input: Do not prompt for user input and eventually force a refresh of cached resources.
        password: The password to use when unpacking the repository.

    Returns:
        The path to the unpacked zipfile.
    """
    cache_dir = Path(cache_dir).expanduser().resolve()
    make_sure_path_exists(cache_dir)

    if is_remote:
        zip_path = download_zipfile(zip_uri, cache_dir, no_input=no_input)
    else:
        # Just use the local zipfile as-is.
        zip_path = Path(zip_uri).expanduser().resolve()

    # Now unpack the repository into a temporary directory
    validate_zipfile(zip_path, zip_uri)
    return extract_zipfile(zip_path, no_input, password)


def validate_zipfile(zip_path: Path, zip_uri: str) -> None:
    """
    Validate that a zipfile exists and is not empty.

    Args:
        zip_path: The path to the zipfile.
        zip_uri: The origin URI of the zipfile.

    Raises:
        EmptyZipRepositoryError: If the zipfile is empty.
        NoZipDirectoryError: If the zipfile does not contain a top-level directory.
    """
    try:
        zip_file = ZipFile(zip_path)

        if len(zip_file.namelist()) == 0:
            raise EmptyZipRepositoryError(zip_uri)

        # The first record in the zipfile should be the directory entry for
        # the archive. If it isn't a directory, there's a problem.
        first_filename = zip_file.namelist()[0]
        if not first_filename.endswith("/"):
            raise NoZipDirectoryError(zip_uri)
    except BadZipFile as e:
        raise InvalidZipRepositoryError(zip_uri) from e


def extract_zipfile(zip_path: Path, no_input: bool, password: Optional[str] = None) -> Path:
    """
    Extract a zipfile into a temporary directory.

    Args:
        zip_path: The path to the zipfile.
        no_input: Don't prompt for user input.
        password: The password for a password-protected zipfile.

    Raises:
        InvalidZipPasswordError: If the zipfile is password-protected and the user provides an incorrect password.

    Returns:
        The temporary directory containing the unpacked zipfile.
    """
    zip_file = ZipFile(zip_path)
    password_bytes = password.encode("utf-8") if password else None

    # The first record in the zipfile should be the directory entry for the archive, with a trailing slash.
    project_name = zip_file.namelist()[0][:-1]

    # Construct the final target directory
    unzip_base = tempfile.mkdtemp()
    unzip_path = os.path.join(unzip_base, project_name)

    # Extract the zip file into the temporary directory
    try:
        zip_file.extractall(path=unzip_base, pwd=password_bytes)
    except RuntimeError as e:
        if no_input:
            raise InvalidZipPasswordError() from e
        retry = 0
        while retry is not None:
            try:
                password = read_repo_password("Repo password")
                zip_file.extractall(path=unzip_base, pwd=password.encode("utf-8"))
                retry = None
            except RuntimeError as e2:
                retry += 1
                if retry == 3:
                    raise InvalidZipPasswordError() from e2

    return Path(unzip_path)
