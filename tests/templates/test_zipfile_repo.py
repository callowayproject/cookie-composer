"""Tests for zipfile_repo.py module."""

import shutil
import tempfile
from pathlib import Path

import pytest

from cookie_composer.exceptions import (
    InvalidZipRepositoryError,
    InvalidZipPasswordError,
    EmptyZipRepositoryError,
    NoZipDirectoryError,
)
from cookie_composer.templates import zipfile_repo
from cookie_composer.templates.types import Locality


def mock_download(fixture_path: Path):
    """Fake download function."""
    with fixture_path.joinpath("fake-repo-tmpl.zip").open("rb") as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def mock_download_with_empty_chunks(fixture_path: Path):
    """Fake download function."""
    yield
    with fixture_path.joinpath("fake-repo-tmpl.zip").open("rb") as zf:
        chunk = zf.read(1024)
        while chunk:
            yield chunk
            chunk = zf.read(1024)


def test_unzip_local_file(mocker, fixtures_path: Path, tmp_path: Path):
    """Local file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.prompt_and_delete", return_value=True, autospec=True
    )
    zipfile_path = fixtures_path.joinpath("fake-repo-tmpl.zip")
    output_dir = zipfile_repo.unzip(str(zipfile_path), is_remote=False, cache_dir=tmp_path)

    assert str(output_dir).startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_unzip_local_protected_file(mocker, fixtures_path: Path, tmp_path: Path):
    """Local protected file reference can be unzipped."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.prompt_and_delete", return_value=True, autospec=True
    )
    zipfile_path = fixtures_path.joinpath("protected-fake-repo-tmpl.zip")
    output_dir = zipfile_repo.unzip(str(zipfile_path), is_remote=False, cache_dir=tmp_path, password="sekrit")

    assert str(output_dir).startswith(tempfile.gettempdir())
    assert not mock_prompt_and_delete.called


def test_extract_protected_local_file_environment_password(fixtures_path: Path):
    """In `extract_zipfile()`, the environment can be used to provide a repo password."""
    zipfile_path = fixtures_path.joinpath("protected-fake-repo-tmpl.zip")
    output_dir = zipfile_repo.extract_zipfile(zipfile_path, no_input=True, password="sekrit")

    assert str(output_dir).startswith(tempfile.gettempdir())


def test_extract_protected_local_file_bad_environment_password(mocker, fixtures_path: Path):
    """In `extract_zipfile()`, an error occurs if the environment has a bad password."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.read_repo_password", return_value="still-wrong"
    )
    zipfile_path = fixtures_path.joinpath("protected-fake-repo-tmpl.zip")
    with pytest.raises(InvalidZipPasswordError):
        zipfile_repo.extract_zipfile(
            zipfile_path,
            no_input=False,
            password="not-the-right-password",
        )


def test_extract_protected_local_file_user_password_with_noinput(fixtures_path: Path):
    """Can't unpack a password-protected repo in no_input mode."""

    zipfile_path = fixtures_path.joinpath("protected-fake-repo-tmpl.zip")
    with pytest.raises(InvalidZipPasswordError):
        zipfile_repo.extract_zipfile(
            zipfile_path,
            no_input=True,
            password=None,
        )


def test_extract_protected_local_file_user_password(mocker, fixtures_path: Path):
    """A password-protected local file reference can be unzipped."""
    mock_read_repo_password = mocker.patch(
        "cookie_composer.templates.zipfile_repo.read_repo_password", return_value="sekrit"
    )
    zipfile_path = fixtures_path.joinpath("protected-fake-repo-tmpl.zip")
    output_dir = zipfile_repo.extract_zipfile(
        zipfile_path,
        no_input=False,
        password=None,
    )

    assert str(output_dir).startswith(tempfile.gettempdir())
    assert mock_read_repo_password.called


def test_validate_empty_zip_file(fixtures_path: Path):
    """In `validate_zipfile()`, an empty file raises an error."""
    zipfile_path = fixtures_path.joinpath("empty.zip")
    with pytest.raises(EmptyZipRepositoryError):
        zipfile_repo.validate_zipfile(zipfile_path, str(zipfile_path))


def test_non_repo_zip_file(fixtures_path: Path):
    """In `validate_zipfile()`, a repository must have a top level directory."""
    zipfile_path = fixtures_path.joinpath("not-a-repo.zip")
    with pytest.raises(NoZipDirectoryError):
        zipfile_repo.validate_zipfile(zipfile_path, str(zipfile_path))


def test_bad_zip_file(fixtures_path: Path):
    """In `validate_zipfile()`, a corrupted zip file raises an error."""
    zipfile_path = fixtures_path.joinpath("bad-zip-file.zip")
    with pytest.raises(InvalidZipRepositoryError):
        zipfile_repo.validate_zipfile(zipfile_path, str(zipfile_path))


def test_download_zipfile_url(mocker, tmp_path: Path, fixtures_path: Path):
    """In `download_zipfile()`, a url will be downloaded."""
    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download(fixtures_path)

    mocker.patch(
        "cookie_composer.templates.zipfile_repo.requests.get",
        return_value=request,
        autospec=True,
    )

    output_path = zipfile_repo.download_zipfile(
        "https://example.com/path/to/fake-repo-tmpl.zip",
        cache_dir=tmp_path,
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.name == "fake-repo-tmpl.zip"


def test_download_url_with_empty_chunks(mocker, tmp_path: Path, fixtures_path: Path):
    """In `download_zipfile()` empty chunk must be ignored."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.prompt_and_delete", return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download_with_empty_chunks(fixtures_path)

    mocker.patch(
        "cookie_composer.templates.zipfile_repo.requests.get",
        return_value=request,
        autospec=True,
    )

    output_path = zipfile_repo.download_zipfile(
        "https://example.com/path/to/fake-repo-tmpl.zip",
        cache_dir=tmp_path,
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.name == "fake-repo-tmpl.zip"


def test_download_url_existing_cache(mocker, tmp_path: Path, fixtures_path: Path):
    """Url should be downloaded and unzipped, old zip file will be removed."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.prompt_and_delete", return_value=True, autospec=True
    )

    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download(fixtures_path)

    mocker.patch(
        "cookie_composer.templates.zipfile_repo.requests.get",
        return_value=request,
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = tmp_path.joinpath("fake-repo-tmpl.zip")
    existing_zip.write_text("This is an existing zipfile")

    output_path = zipfile_repo.download_zipfile(
        "https://example.com/path/to/fake-repo-tmpl.zip",
        cache_dir=tmp_path,
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.name == "fake-repo-tmpl.zip"
    assert mock_prompt_and_delete.call_count == 1


def test_download_url_existing_cache_no_input(mocker, tmp_path: Path, fixtures_path: Path):
    """If no_input is provided, the existing file should be removed."""
    request = mocker.MagicMock()
    request.iter_content.return_value = mock_download(fixtures_path)

    mock_requests_get = mocker.patch(
        "cookie_composer.templates.zipfile_repo.requests.get",
        return_value=request,
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = tmp_path.joinpath("fake-repo-tmpl.zip")
    existing_zip.write_text("This is an existing zipfile")

    output_path = zipfile_repo.download_zipfile(
        "https://example.com/path/to/fake-repo-tmpl.zip",
        cache_dir=tmp_path,
        no_input=True,
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.name == "fake-repo-tmpl.zip"
    assert mock_requests_get.call_count == 1


def test_download_should_abort_if_no_redownload(mocker, tmp_path: Path):
    """Should exit without cloning anything If no re-download."""
    mocker.patch("cookie_composer.templates.zipfile_repo.prompt_and_delete", side_effect=SystemExit, autospec=True)

    mock_requests_get = mocker.patch(
        "cookie_composer.templates.zipfile_repo.requests.get",
        autospec=True,
    )

    # Create an existing cache of the zipfile
    existing_zip = tmp_path.joinpath("fake-repo-tmpl.zip")
    existing_zip.write_text("This is an existing zipfile")

    zipfile_url = "https://example.com/path/to/fake-repo-tmpl.zip"

    with pytest.raises(SystemExit):
        zipfile_repo.download_zipfile(zipfile_url, cache_dir=tmp_path)

    assert not mock_requests_get.called


def test_download_is_ok_to_reuse(mocker, tmp_path: Path, fixtures_path: Path):
    """Already downloaded zip should not be downloaded again."""
    mock_prompt_and_delete = mocker.patch(
        "cookie_composer.templates.zipfile_repo.prompt_and_delete", return_value=False, autospec=True
    )

    request = mocker.MagicMock()

    existing_zip = tmp_path.joinpath("fake-repo-tmpl.zip")
    shutil.copy(fixtures_path.joinpath("fake-repo-tmpl.zip"), existing_zip)

    output_path = zipfile_repo.download_zipfile(
        "https://example.com/path/to/fake-repo-tmpl.zip",
        cache_dir=tmp_path,
    )

    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.name == "fake-repo-tmpl.zip"
    assert mock_prompt_and_delete.call_count == 1
    assert request.iter_content.call_count == 0


def test_template_repo_from_zipfile(fixtures_path: Path, tmp_path: Path):
    """Test template_repo_from_zipfile."""
    zipfile_path = fixtures_path.joinpath("fake-repo-tmpl.zip")
    template_repo = zipfile_repo.template_repo_from_zipfile(
        str(zipfile_path), locality=Locality.LOCAL, cache_dir=tmp_path
    )

    assert template_repo.source == str(zipfile_path)
    assert template_repo.cached_source.exists()
    assert template_repo.cached_source.is_dir()
    assert template_repo.cached_source.name == "fake-repo-tmpl"
    assert template_repo.format == "zip"
    assert template_repo.locality == Locality.LOCAL
    assert template_repo.checkout is None
    assert template_repo.password is None
