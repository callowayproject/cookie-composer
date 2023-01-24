"""Authentication tests."""
from typing import Optional

import functools
import json
import os

from cookie_composer import authentication


class MockPath:
    """A mocked Path class."""

    def __init__(self, path: Optional[str] = None, contents: str = ""):
        self.path = path or os.getcwd()
        self.contents = contents
        self._exists = True

    def expanduser(self) -> "MockPath":
        """Return a new MockPath with the path expanded."""
        path = self.path.replace("~/", "/user/test/")
        return MockPath(path, self.contents)

    def resolve(self) -> "MockPath":
        """Return a new MockPath with the path resolved."""
        return MockPath(self.path, self.contents)

    def mkdir(self, *args, **kwargs):
        pass

    def exists(self):
        return self._exists

    def __truediv__(self, other) -> "MockPath":
        import os.path

        if isinstance(other, str):
            return MockPath(os.path.join(self.path, other), self.contents)
        elif isinstance(other, MockPath):
            return MockPath(os.path.join(self.path, other.path), self.contents)
        else:
            raise ValueError("MockPath can only be divided by a string or a MockPath")

    def __call__(self, path: str, contents: Optional[str] = None) -> "MockPath":
        contents = contents or self.contents
        return MockPath(path, contents)

    def __str__(self) -> str:
        return self.path

    def read_text(self) -> str:
        return self.contents

    def write_text(self, text: str):
        self.contents = text


def create_mock_path(contents: str = "") -> MockPath:
    """Create a mock path."""
    return MockPath(contents=contents)


def test_get_hosts_file(mocker):
    """Getting the host file should return the correct path."""
    mocker.patch(
        "cookie_composer.authentication.Path", new_callable=create_mock_path, contents='{"hosts": ["127.0.0.1"]}'
    )
    path = authentication.get_hosts_file()
    assert path.path == "/user/test/.config/cookiecomposer/hosts.json"
    assert path.read_text() == '{"hosts": ["127.0.0.1"]}'
    path.write_text("{}")
    assert path.read_text() == "{}"


def test_login_to_svc_with_no_hosts_file(mocker):
    """Login to the service with no hosts file."""
    mocked_path = create_mock_path("")
    mocker.patch("cookie_composer.authentication.get_hosts_file", return_value=mocked_path)
    mocked_path._exists = False
    mocked_token = "thisisatesttoken"
    mocker.patch("cookie_composer.authentication.github_auth_device", return_value=mocked_token)

    result_token = authentication.login_to_svc(protocol="https", service="github.com")
    assert result_token == mocked_token
    assert json.loads(mocked_path.contents) == {
        "github.com": {"git_protocol": "https", "oauth_token": "thisisatesttoken"}
    }

    mocked_path._exists = True
    result_token = authentication.login_to_svc(protocol="https", service="foobar.com")
    assert result_token == ""
    assert json.loads(mocked_path.contents) == {
        "github.com": {"git_protocol": "https", "oauth_token": "thisisatesttoken"},
        "foobar.com": {"git_protocol": "https", "oauth_token": ""},
    }


def test_get_cached_token(mocker):
    """When the cached token exists, it gets returned."""
    mocked_path = create_mock_path(
        json.dumps({"github.com": {"git_protocol": "https", "oauth_token": "thisisatesttoken"}})
    )
    mocker.patch("cookie_composer.authentication.get_hosts_file", return_value=mocked_path)
    assert authentication.get_cached_token("github.com") == "thisisatesttoken"
    assert authentication.get_cached_token("idon'texist") is None


def test_add_auth_to_url(mocker):
    """A host with a cached token returns a new URL."""
    mocked_path = create_mock_path(
        json.dumps({"github.com": {"git_protocol": "https", "oauth_token": "thisisatesttoken"}})
    )
    mocker.patch("cookie_composer.authentication.get_hosts_file", return_value=mocked_path)
    new_url = authentication.add_auth_to_url("https://github.com/test/test")
    assert new_url == "https://cookiecomposer:thisisatesttoken@github.com/test/test"

    new_url = authentication.add_auth_to_url("https://foobar.com/test/test")
    assert new_url == "https://foobar.com/test/test"
