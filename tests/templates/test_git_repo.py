"""Test for git_repo template."""
from pathlib import Path

from git import Repo

from cookie_composer.templates.git_repo import get_repo_name, template_repo_from_git
import pytest
from pytest import param

from cookie_composer.templates.types import Locality, TemplateFormat


@pytest.mark.parametrize(
    ["repo_url", "checkout", "expected"],
    [
        param("https://github.com/callowayproject/cookie-composer", None, "cookie-composer", id="no_checkout"),
        param(
            "https://github.com/callowayproject/cookie-composer", "main", "cookie-composer_main", id="with_checkout"
        ),
        param(
            "https://github.com/callowayproject/cookie-composer.git",
            None,
            "cookie-composer",
            id="no_checkout_git_suffix",
        ),
        param(
            "https://github.com/callowayproject/cookie-composer.git",
            "main",
            "cookie-composer_main",
            id="with_checkout_git_suffix",
        ),
        param("https://github.com/callowayproject/cookie-composer/", None, "cookie-composer", id="no_checkout_slash"),
        param(
            "https://github.com/callowayproject/cookie-composer/",
            "main",
            "cookie-composer_main",
            id="with_checkout_slash",
        ),
        param(
            "https://github.com/callowayproject/cookie-composer.git/",
            None,
            "cookie-composer",
            id="no_checkout_git_suffix_slash",
        ),
        param(
            "https://github.com/callowayproject/cookie-composer.git/",
            "main",
            "cookie-composer_main",
            id="with_checkout_git_suffix_slash",
        ),
    ],
)
def test_get_repo_name(repo_url: str, checkout: str, expected: str):
    """Test get_repo_name properly parses url paths and checkouts."""
    assert get_repo_name(repo_url, checkout) == expected


def test_template_repo_from_git_local_no_checkout(default_repo: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - local repo no checkout
    """
    template_repo = template_repo_from_git(default_repo.working_tree_dir, Locality.LOCAL, tmp_path, checkout=None)
    assert template_repo.source == default_repo.working_tree_dir
    assert template_repo.cached_source == Path(default_repo.working_tree_dir)
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.LOCAL
    assert template_repo.checkout is None


def test_template_repo_from_git_local_with_checkout(default_repo: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - local repo with checkout
    """
    template_repo = template_repo_from_git(
        default_repo.working_tree_dir, Locality.LOCAL, tmp_path, checkout="remote-branch"
    )
    assert template_repo.source == default_repo.working_tree_dir
    assert template_repo.cached_source == Path(default_repo.working_tree_dir)
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.LOCAL
    assert template_repo.checkout == "remote-branch"


def test_template_repo_from_git_remote_no_checkout(default_origin: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - remote repo no checkout
    """
    origin_path = Path(default_origin.working_dir)
    template_repo = template_repo_from_git(str(origin_path), Locality.REMOTE, tmp_path, checkout=None)
    assert template_repo.source == str(origin_path)
    assert template_repo.cached_source == origin_path.parent.joinpath("origin")
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.REMOTE
    assert template_repo.checkout is None


def test_template_repo_from_git_remote_with_checkout(default_origin: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - remote repo with checkout
    """
    origin_path = Path(default_origin.working_dir)
    template_repo = template_repo_from_git(str(origin_path), Locality.REMOTE, tmp_path, checkout="remote-branch")
    assert template_repo.source == str(origin_path)
    assert template_repo.cached_source == origin_path.parent.joinpath("origin_remote-branch")
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.REMOTE
    assert template_repo.checkout == "remote-branch"


def test_template_repo_from_git_existing_remote_no_checkout(default_origin: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - remote repo previously cloned no checkout
    """
    origin_path = Path(default_origin.working_dir)
    repo_path = tmp_path.joinpath("origin")
    repo = default_origin.clone(repo_path)
    repo.heads.master.checkout()
    repo.remotes.origin.pull()
    template_repo = template_repo_from_git(str(origin_path), Locality.REMOTE, tmp_path, checkout=None)
    assert template_repo.source == default_origin.working_dir
    assert template_repo.cached_source == repo_path
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.REMOTE
    assert template_repo.checkout is None


def test_template_repo_from_git_existing_remote_with_checkout(default_origin: Repo, tmp_path: Path):
    """
    Test template_repo_from_git.

    - remote repo previously cloned with checkout
    """
    branch = "remote-branch"
    origin_path = Path(default_origin.working_dir)
    repo_path = tmp_path.joinpath(f"origin_{branch}")
    repo = default_origin.clone(repo_path)
    repo.remotes.origin.pull()
    repo.create_head(branch, f"origin/{branch}")
    repo.heads[branch].checkout()
    repo.heads[branch].set_tracking_branch(repo.remotes.origin.refs[branch])

    template_repo = template_repo_from_git(str(origin_path), Locality.REMOTE, tmp_path, checkout="remote-branch")
    assert template_repo.source == default_origin.working_dir
    assert template_repo.cached_source == repo_path
    assert template_repo.format == TemplateFormat.GIT
    assert template_repo.locality == Locality.REMOTE
    assert template_repo.checkout == "remote-branch"
