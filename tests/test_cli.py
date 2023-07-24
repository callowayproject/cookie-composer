from pathlib import Path

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


def test_local_extension(tmpdir, runner, fixtures_path):
    """Test to verify correct work of extension, included in template."""
    output_dir = str(tmpdir.mkdir("output"))
    template_path = fixtures_path / "local_extension_template"

    result = runner.invoke(
        cli.create,
        [
            "--no-input",
            "--default-config",
            "--output-dir",
            output_dir,
            str(template_path),
        ],
    )
    if result.exit_code != 0:
        print(result.exception)
        print(result.output)
    assert result.exit_code == 0
    content = Path(output_dir, "Foobar", "HISTORY.rst").read_text()
    assert "FoobarFoobar" in content
    assert "FOOBAR" in content
