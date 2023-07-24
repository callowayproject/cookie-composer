import pytest
from click import BadParameter
from click.testing import CliRunner

from cookie_composer import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_validate_context_params():
    """Make sure the context params are validated."""
    with pytest.raises(BadParameter):
        cli.validate_context_params(None, None, ("iaminvalid", "key=value"))

    assert cli.validate_context_params(None, None, ("key1=value1", "key=value")) == {"key1": "value1", "key": "value"}


def test_helps(runner):
    result = runner.invoke(cli.create, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.add, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.update, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.link, "--help")
    assert result.exit_code == 0
