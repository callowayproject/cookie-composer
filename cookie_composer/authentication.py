"""OAuth2 authentication to access protected resources."""
from typing import Optional

import json
from pathlib import Path


def get_hosts_file() -> Path:
    """Return the path to the hosts file."""
    config_dir = Path("~/.config/cookiecomposer").expanduser().resolve()
    config_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
    return config_dir / "hosts.json"


def login_to_svc(
    service: Optional[str] = None,
    protocol: Optional[str] = None,
    scopes: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    """
    Log in and cache token.

    Args:
        service: The name of the service to authenticate with
        protocol: The protocol to use for git operations
        scopes: Additional authentication scopes to request
        token: A specific token to use instead of logging in

    Returns:
        The token for the service
    """
    import questionary

    hosts_file = get_hosts_file()
    hosts = json.loads(hosts_file.read_text()) if hosts_file.exists() else {}

    if not service:  # pragma: no cover
        title = "What account do you want to log into?"
        options = [
            "github.com",
        ]
        service = questionary.select(title, options).ask()

    protocol = protocol or hosts.get(service, {}).get("git_protocol")
    if not protocol:  # pragma: no cover
        title = "What is your preferred protocol for Git operations?"
        options = ["ssh", "https"]
        protocol = questionary.select(title, options).ask()

    token = token or hosts.get(service, {}).get("oauth_token")
    if not token:  # pragma: no cover
        token = github_auth_device() if service == "github.com" else ""

    hosts[service] = {"git_protocol": protocol, "oauth_token": token}
    hosts_file.write_text(json.dumps(hosts))

    return token


def get_cached_token(account_name: str) -> Optional[str]:
    """Return the cached token for the account."""
    hosts_file = get_hosts_file()
    hosts = json.loads(hosts_file.read_text()) if hosts_file.exists() else {}
    return hosts.get(account_name, {}).get("oauth_token")


def add_auth_to_url(url: str) -> str:
    """
    Add authentication information to a URL.

    Args:
        url: The URL to add authentication information to.

    Returns:
        The URL with authentication information added, or the original URL if no token is cached
    """
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(url)
    token = get_cached_token(parsed.netloc)

    if token:
        parsed = parsed._replace(netloc=f"cookiecomposer:{token}@{parsed.netloc}")

    return urlunparse(parsed)


def github_auth_device(n_polls=9999):  # pragma: no cover
    """
    Authenticate with GitHub, polling up to ``n_polls`` times to wait for completion.
    """
    from ghapi.auth import GhDeviceAuth

    auth = GhDeviceAuth(client_id="de4e3ca9028661a80b50")
    print(f"First copy your one-time code: \x1b[33m{auth.user_code}\x1b[m")
    print(f"Then visit {auth.verification_uri} in your browser, and paste the code when prompted.")
    input("Press Enter to open github.com in your browser...")
    auth.open_browser()

    print("Waiting for authorization...", end="")
    token = auth.wait(lambda: print(".", end=""), n_polls=n_polls)
    if not token:
        return print("Authentication not complete!")
    print("Authenticated to GitHub")
    return token
