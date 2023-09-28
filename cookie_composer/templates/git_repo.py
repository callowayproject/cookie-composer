"""Utility functions for handling and fetching repo archives in git format."""
from pathlib import Path
from typing import Optional

from cookiecutter.utils import make_sure_path_exists

from cookie_composer.git_commands import checkout_ref, clone, get_repo
from cookie_composer.templates.types import Locality, TemplateFormat, TemplateRepo


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
        repo = get_repo(git_uri, search_parent_directories=True, ensure_clean=ensure_clean)
    else:
        cache_dir = Path(cache_dir).expanduser().resolve()
        make_sure_path_exists(cache_dir)
        repo_name = get_repo_name(git_uri, checkout)
        repo_dir = cache_dir.joinpath(repo_name)
        repo = clone(git_uri, repo_dir)

    if len(repo.remotes) > 0:
        repo.remotes[0].pull()

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
