from click.testing import CliRunner
import pytest

from cookie_composer import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_helps(runner):
    result = runner.invoke(cli.create, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.add, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.update, "--help")
    assert result.exit_code == 0
    result = runner.invoke(cli.link, "--help")
    assert result.exit_code == 0
