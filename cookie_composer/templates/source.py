"""Entry point for cookiecutter templates."""
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from cookiecutter.config import get_user_config

from cookie_composer.templates.git_repo import template_repo_from_git
from cookie_composer.templates.types import Locality, TemplateFormat, TemplateRepo
from cookie_composer.templates.zipfile_repo import template_repo_from_zipfile


def identify_repo(url: str, local_path: Optional[Path] = None) -> Tuple[TemplateFormat, Locality]:
    """Identify the repo format and locality from the URL."""
    parsed_url = urlparse(url)
    locality = Locality.LOCAL if parsed_url.scheme in {"", "file"} else Locality.REMOTE

    if url.endswith(".zip"):
        return TemplateFormat.ZIP, locality

    if locality == Locality.LOCAL:
        git_path = resolve_local_path(parsed_url.path, local_path).joinpath(".git")
        is_git = git_path.exists() and git_path.is_dir()

        return TemplateFormat.GIT if is_git else TemplateFormat.PLAIN, locality

    if url.endswith(".git") or url.startswith("git+") or "git" in parsed_url.netloc:
        return TemplateFormat.GIT, locality

    raise ValueError(f"Unknown template format for URL: {url}")


def get_template_repo(
    url: str, local_path: Optional[Path] = None, checkout: Optional[str] = None, password: Optional[str] = None
) -> TemplateRepo:
    """
    Get a template repository from a URL.

    Args:
        url: The string from the template field in the composition file.
        local_path: Used to resolve local paths.
        checkout: The branch, tag or commit to check out after git clone
        password: The password to use if template is a password-protected Zip archive.

    Returns:
        A :class:`TemplateRepo` object.
    """
    user_config = get_user_config()
    tmpl_format, locality = identify_repo(url, local_path)

    if locality == Locality.LOCAL:
        cache_dir = resolve_local_path(url, local_path)
    else:
        cache_dir = Path(user_config["cookiecutters_dir"])

    if tmpl_format == TemplateFormat.ZIP:
        return template_repo_from_zipfile(url, locality, cache_dir, password=password)
    elif tmpl_format == TemplateFormat.GIT:
        return template_repo_from_git(url, locality, cache_dir, checkout=checkout)
    else:
        return TemplateRepo(
            source=url,
            cached_source=cache_dir,
            format=TemplateFormat.PLAIN,
            locality=Locality.LOCAL,
            checkout=None,
            password=None,
        )


def resolve_local_path(url: str, local_path: Optional[Path] = None) -> Path:
    """
    Resolve a local path.

    Args:
        url: The string from the template field in the composition file.
        local_path: An optional path to resolve the URL against.

    Returns:
        The resolved path.
    """
    if local_path is None:
        return Path(url).expanduser().resolve()
    return local_path.joinpath(url).expanduser().resolve()
