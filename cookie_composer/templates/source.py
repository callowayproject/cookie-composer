"""Entry point for cookiecutter templates."""
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from cookie_composer.templates.git_repo import template_repo_from_git
from cookie_composer.templates.types import Locality, TemplateFormat, TemplateRepo
from cookie_composer.templates.zipfile_repo import template_repo_from_zipfile


def identify_repo(url: str) -> Tuple[TemplateFormat, Locality]:
    """Identify the repo format and locality from the URL."""
    parsed_url = urlparse(url)
    locality = Locality.LOCAL if parsed_url.scheme in {"", "file"} else Locality.REMOTE

    if url.endswith(".zip"):
        return TemplateFormat.ZIP, locality

    if locality == Locality.LOCAL:
        git_path = Path(parsed_url.path).joinpath(".git")
        is_git = git_path.exists() and git_path.is_dir()

        return TemplateFormat.GIT if is_git else TemplateFormat.PLAIN, locality

    if url.endswith(".git") or url.startswith("git+") or "git" in parsed_url.netloc:
        return TemplateFormat.GIT, locality

    raise ValueError(f"Unknown template format for URL: {url}")


def get_template_repo(
    url: str, cache_dir: Path, checkout: Optional[str] = None, password: Optional[str] = None
) -> TemplateRepo:
    """Get the template repo for a URL."""
    tmpl_format, locality = identify_repo(url)

    if tmpl_format == TemplateFormat.ZIP:
        return template_repo_from_zipfile(url, locality, cache_dir, password=password)
    elif tmpl_format == TemplateFormat.GIT:
        return template_repo_from_git(url, locality, cache_dir, checkout=checkout)
    else:
        dir_path = Path(url).expanduser().resolve()
        return TemplateRepo(
            source=url,
            cached_source=Path(dir_path),
            format=TemplateFormat.PLAIN,
            locality=Locality.LOCAL,
            checkout=None,
            password=None,
        )
