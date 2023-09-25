"""Tests for the templates.source module."""
from typing import Tuple

from cookie_composer.templates.types import TemplateFormat, Locality, TemplateRepo
from cookie_composer.templates.source import identify_repo, get_template_repo

import pytest
from pathlib import Path


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://example.com/repo.zip", (TemplateFormat.ZIP, Locality.REMOTE)),
        ("file:///path/to/repo.zip", (TemplateFormat.ZIP, Locality.LOCAL)),
        ("/path/to/repo.zip", (TemplateFormat.ZIP, Locality.LOCAL)),
        ("https://github.com/user/repo.git", (TemplateFormat.GIT, Locality.REMOTE)),
        ("git+https://github.com/user/repo.git", (TemplateFormat.GIT, Locality.REMOTE)),
        ("https://git.example.com/user/repo", (TemplateFormat.GIT, Locality.REMOTE)),
    ],
)
def test_identify_repo(url, expected):
    """Test that the repo format and locality are identified correctly."""
    result = identify_repo(url)
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
    "url, tmpl_format, locality, expected_args",
    [
        (
            "https://example.com/repo.zip",
            TemplateFormat.ZIP,
            Locality.REMOTE,
            {"password": None},
        ),
        (
            "/path/to/local/repo.zip",
            TemplateFormat.ZIP,
            Locality.LOCAL,
            {"password": None},
        ),
    ],
)
def test_get_template_repo(mocker, url, tmpl_format, locality, expected_args):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    # Mock the relevant return function to just return a dummy TemplateRepo
    mocked_func = mocker.patch(
        "cookie_composer.templates.source.template_repo_from_zipfile", return_value=mocker.Mock(spec=TemplateRepo)
    )

    # Call the function
    cache_dir = Path("/cache")
    result = get_template_repo(url, cache_dir)

    # Check which function was called and with which arguments
    mocked_func.assert_called_once_with(url, locality, cache_dir, **expected_args)


@pytest.mark.parametrize(
    "url, tmpl_format, locality, expected_args",
    [
        (
            "https://github.com/user/repo.git",
            TemplateFormat.GIT,
            Locality.REMOTE,
            {"checkout": None},
        ),
        ("/path/to/local/git/repo", TemplateFormat.GIT, Locality.LOCAL, {"checkout": None}),
    ],
)
def test_get_template_repo_git(mocker, url, tmpl_format, locality, expected_args):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    # Mock the relevant return function to just return a dummy TemplateRepo
    mocked_func = mocker.patch(
        "cookie_composer.templates.source.template_repo_from_git", return_value=mocker.Mock(spec=TemplateRepo)
    )

    # Call the function
    cache_dir = Path("/cache")
    result = get_template_repo(url, cache_dir)
    mocked_func.assert_called_once_with(url, locality, cache_dir, **expected_args)


@pytest.mark.parametrize(
    "url, tmpl_format, locality",
    [
        ("/path/to/local/plain/repo", TemplateFormat.PLAIN, Locality.LOCAL),
    ],
)
def test_get_template_repo_plain(mocker, url, tmpl_format, locality):
    # Mock identify_repo to return tmpl_format and locality
    mocker.patch("cookie_composer.templates.source.identify_repo", return_value=(tmpl_format, locality))

    # Mock the relevant return function to just return a dummy TemplateRepo
    # Call the function
    cache_dir = Path("/cache")
    result = get_template_repo(url, cache_dir)

    assert isinstance(result, TemplateRepo)
    assert result.source == url
    assert result.format == TemplateFormat.PLAIN
    assert result.locality == Locality.LOCAL
    assert result.checkout is None
    assert result.password is None
