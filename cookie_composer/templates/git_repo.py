"""Utility functions for handling and fetching repo archives in git format."""

import logging
from pathlib import Path
from typing import Optional

from cookiecutter.utils import make_sure_path_exists
from git import Repo

from cookie_composer.git_commands import checkout_ref, clone, get_repo
from cookie_composer.templates.types import Locality, TemplateFormat, TemplateRepo
from cookie_composer.utils import remove_single_path

logger = logging.getLogger(__name__)


def get_repo_name(repo_url: str, checkout: Optional[str] = None) -> str:
    """Construct the destination repo name from the repo URL and checkout."""
    repo_name = repo_url.rstrip("/").rsplit("/", 1)[-1]  # Get the last part of the URL path
    repo_name = repo_name.rsplit(".git")[0]  # Strip off any .git suffix
    if checkout is not None:
        repo_name = f"{repo_name}_{checkout}"
    return repo_name


def template_repo_from_git(
    git_uri: str, locality: Locality, cache_dir: Path, checkout: Optional[str] = None
) -> TemplateRepo:
    """
    Return a template repo from a git URI.

    - If the repo is remote, it will be cloned to the cache_dir and named after the repo and checkout value,
    for example `mytemplate_main`. This allows for multiple versions of the same repo to be cached without
    a conflict.
    - If the repo is already cloned, it will not be cloned again.
    - If the repo is local, it is not cloned but will check out `checkout`, and the local path is returned.

    """
    if locality == Locality.LOCAL:
        ensure_clean = checkout is not None
        local_path = cache_dir.joinpath(git_uri).expanduser().resolve()
        logger.debug("Getting local repo %s", local_path)
        repo = get_repo(local_path, search_parent_directories=True, ensure_clean=ensure_clean)
    else:
        repo = get_cached_remote(git_uri, cache_dir, checkout)

    if checkout:
        checkout_ref(repo, checkout)

    return TemplateRepo(
        source=git_uri,
        cached_source=Path(repo.working_dir),
        format=TemplateFormat.GIT,
        locality=locality,
        checkout=checkout,
        password=None,
    )


def get_cached_remote(git_uri: str, cache_dir: Path, checkout: Optional[str] = None) -> Repo:
    """
    Return a cached remote repo.

    This provides some error-checking for the cached repo, and will re-clone if the
    cached repo is in a detached head state.

    Args:
        git_uri: The remote git URI
        cache_dir: The directory to cache the repo in
        checkout: The optional checkout ref to use

    Returns:
        The cached repo
    """
    logger.debug("Getting cached remote repo %s", git_uri)
    cache_dir = cache_dir.expanduser().resolve()
    make_sure_path_exists(cache_dir)
    repo_name = get_repo_name(git_uri, checkout)
    repo_dir = cache_dir.joinpath(repo_name)
    repo = clone(git_uri, repo_dir)
    if repo.head.is_detached and repo.head.object.hexsha != checkout:
        logger.info("The cached repo is not on the expected checkout, deleting and re-cloning.")
        remove_single_path(repo_dir)
        repo = clone(git_uri, repo_dir)
    return repo
