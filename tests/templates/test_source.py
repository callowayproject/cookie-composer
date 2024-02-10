"""Tests for the templates.source module."""

from typing import Tuple

from cookiecutter.config import get_user_config

from cookie_composer.templates.types import TemplateFormat, Locality, TemplateRepo
from cookie_composer.templates.source import identify_repo, get_template_repo

import pytest
from pathlib import Path


@pytest.mark.parametrize(
    "url, local_path, expected",
    [
        ("https://example.com/repo.zip", None, (TemplateFormat.ZIP, Locality.REMOTE)),
        ("file:///path/to/repo.zip", None, (TemplateFormat.ZIP, Locality.LOCAL)),
        ("/path/to/repo.zip", None, (TemplateFormat.ZIP, Locality.LOCAL)),
        ("https://github.com/user/repo.git", None, (TemplateFormat.GIT, Locality.REMOTE)),
        ("git+https://github.com/user/repo.git", None, (TemplateFormat.GIT, Locality.REMOTE)),
        ("https://git.example.com/user/repo", None, (TemplateFormat.GIT, Locality.REMOTE)),
        (".", Path("/path/to/local/"), (TemplateFormat.PLAIN, Locality.LOCAL)),
        ("../template", Path("/path/to/template"), (TemplateFormat.PLAIN, Locality.LOCAL)),
    ],
)
def test_identify_repo(url, local_path, expected):
    """Test that the repo format and locality are identified correctly."""
    result = identify_repo(url, local_path)
    assert result == expected


def test_local_git_repo(mocker):
    """Test that a local git repo is identified correctly."""
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    result = identify_repo("/path/to/local/git/repo")
    assert result == (TemplateFormat.GIT, Locality.LOCAL)


def test_local_plain_repo(mocker):
    """Test that a local plain repo is identified correctly."""
    mocker.patch.object(Path, "exists", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=False)

    result = identify_repo("/path/to/local/plain/repo")
    assert result == (TemplateFormat.PLAIN, Locality.LOCAL)


@pytest.mark.parametrize(
    "url, local_path, cache_dir, tmpl_format, locality, expected_args",
    [
        (
            "https://example.com/repo.zip",
            None,
            None,
            TemplateFormat.ZIP,
            Locality.REMOTE,
            {"password": None},
        ),
        (
            "/path/to/local/repo.zip",
            None,
            Path("/path/to/local/repo.zip"),
            TemplateFormat.ZIP,
            Locality.LOCAL,
            {"password": None},
        ),
        (
            "repo.zip",
            Path("/path/to/local/"),
            Path("/path/to/local/repo.zip"),
            TemplateFormat.ZIP,
            Locality.LOCAL,
            {"password": None},
        ),
    ],
)
def test_get_template_repo(mocker, url, local_path, cache_dir, tmpl_format, locality, expected_args):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    # Mock the relevant return function to just return a dummy TemplateRepo
    mocked_func = mocker.patch(
        "cookie_composer.templates.source.template_repo_from_zipfile", return_value=mocker.Mock(spec=TemplateRepo)
    )

    result = get_template_repo(url, local_path=local_path)

    # Check which function was called and with which arguments
    cache_dir = cache_dir or Path(get_user_config()["cookiecutters_dir"])
    mocked_func.assert_called_once_with(url, locality, cache_dir, **expected_args)


@pytest.mark.parametrize(
    "url, local_path, cache_dir, tmpl_format, locality, expected_args",
    [
        (
            "https://github.com/user/repo.git",
            None,
            None,
            TemplateFormat.GIT,
            Locality.REMOTE,
            {"checkout": None},
        ),
        (
            "/path/to/local/git/repo",
            None,
            Path("/path/to/local/git/repo"),
            TemplateFormat.GIT,
            Locality.LOCAL,
            {"checkout": None},
        ),
        (
            "repo",
            Path("/path/to/local/git/"),
            Path("/path/to/local/git/repo"),
            TemplateFormat.GIT,
            Locality.LOCAL,
            {"checkout": None},
        ),
    ],
)
def test_get_template_repo_git(mocker, url, local_path, cache_dir, tmpl_format, locality, expected_args):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    # Mock the relevant return function to just return a dummy TemplateRepo
    mocked_func = mocker.patch(
        "cookie_composer.templates.source.template_repo_from_git", return_value=mocker.Mock(spec=TemplateRepo)
    )

    # Call the function
    result = get_template_repo(url, local_path=local_path)
    cache_dir = cache_dir or Path(get_user_config()["cookiecutters_dir"])
    mocked_func.assert_called_once_with(url, locality, cache_dir, **expected_args)


@pytest.mark.parametrize(
    "url, local_path, tmpl_format, locality",
    [
        ("/path/to/local/plain/repo", None, TemplateFormat.PLAIN, Locality.LOCAL),
        ("repo", Path("/path/to/local/plain/"), TemplateFormat.PLAIN, Locality.LOCAL),
    ],
)
def test_get_template_repo_plain(mocker, url, local_path, tmpl_format, locality):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    result = get_template_repo(url, local_path=local_path)

    assert isinstance(result, TemplateRepo)
    assert result.source == url
    if local_path is None:
        assert result.cached_source == Path(url).expanduser().resolve()
    else:
        assert result.cached_source == local_path.joinpath(url).expanduser().resolve()
    assert result.format == TemplateFormat.PLAIN
    assert result.locality == Locality.LOCAL
    assert result.checkout is None
    assert result.password is None
