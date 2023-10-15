"""Tests of the cc_overrides module."""
import platform
from collections import OrderedDict

import pytest
from click.testing import CliRunner

from cookie_composer import cc_overrides, data_merge
from cookie_composer.data_merge import Context


@pytest.fixture(autouse=True)
def patch_readline_on_win(monkeypatch):
    """Fixture. Overwrite windows end of line to linux standard."""
    if "windows" in platform.platform().lower():
        monkeypatch.setattr("sys.stdin.readline", lambda: "\n")


def test_jsonify_context():
    """Contexts return a dict."""
    context = data_merge.Context(
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "project_slug": "fake-project-template-two",
            "_requirements": OrderedDict([("bar", ">=5.0.0"), ("baz", "")]),
            "lower_project_name": "fake project template2",
        },
        {
            "project_name": "Fake Project Template2",
            "repo_name": "fake-project-template2",
            "repo_slug": "fake-project-template-two",
            "_requirements": {"foo": "", "bar": ">=5.0.0"},
        },
    )
    expected = {
        "project_name": "Fake Project Template2",
        "repo_name": "fake-project-template2",
        "project_slug": "fake-project-template-two",
        "repo_slug": "fake-project-template-two",
        "_requirements": OrderedDict(
            [
                ("bar", ">=5.0.0"),
                ("baz", ""),
                ("foo", ""),
            ]
        ),
        "lower_project_name": "fake project template2",
    }
    assert cc_overrides.jsonify_context(context) == expected


def test_jsonify_context_non_context():
    """Passing a non-context raises a ValueError."""
    with pytest.raises(TypeError):
        cc_overrides.jsonify_context({"a": 1})


@pytest.mark.parametrize(
    "context",
    [
        {"full_name": "Your Name"},
        {"full_name": "Řekni či napiš své jméno"},
    ],
    ids=["ASCII default prompt/input", "Unicode default prompt/input"],
)
def test_prompt_for_config(mocker, context):
    """Verify `prompt_for_config` call `read_user_variable` on text request."""
    m = mocker.patch("cookie_composer.cc_overrides.read_user_variable")
    m.return_value = context["full_name"]

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)
    assert cookiecutter_dict == context


@pytest.mark.parametrize(
    "context",
    [
        {
            "cookiecutter": {
                "full_name": "Your Name",
                "check": ["yes", "no"],
                "nothing": "ok",
                "__prompts__": {
                    "full_name": "Name please",
                    "check": "Checking",
                },
            }
        },
    ],
    ids=["ASCII default prompt/input"],
)
def test_prompt_for_config_with_human_prompts(monkeypatch, context):
    """Verify call `read_user_variable` on request when human-readable prompts."""
    monkeypatch.setattr(
        "cookie_composer.cc_overrides.read_user_variable",
        lambda var, default, prompts, prefix: default,
    )
    monkeypatch.setattr(
        "cookie_composer.cc_overrides.read_user_yes_no",
        lambda var, default, prompts, prefix: default,
    )
    monkeypatch.setattr(
        "cookiecutter.prompt.read_user_choice",  # This is called by `prompt_choice_for_config`
        lambda var, default, prompts, prefix: default,
    )

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context(), None)
    assert cookiecutter_dict == context["cookiecutter"]


@pytest.mark.parametrize(
    "context",
    [
        {
            "cookiecutter": {
                "full_name": "Your Name",
                "check": ["yes", "no"],
                "__prompts__": {
                    "check": "Checking",
                },
            }
        },
        {
            "cookiecutter": {
                "full_name": "Your Name",
                "check": ["yes", "no"],
                "__prompts__": {
                    "full_name": "Name please",
                    "check": {"__prompt__": "Checking", "yes": "Yes", "no": "No"},
                },
            }
        },
        {
            "cookiecutter": {
                "full_name": "Your Name",
                "check": ["yes", "no"],
                "__prompts__": {
                    "full_name": "Name please",
                    "check": {"no": "No"},
                },
            }
        },
    ],
)
def test_prompt_for_config_with_human_choices(monkeypatch, context):
    """Test prompts when human-readable labels for user choices."""
    runner = CliRunner()
    with runner.isolation(input="\n\n\n"):
        cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)

    assert dict(cookiecutter_dict) == {"full_name": "Your Name", "check": "yes"}


def test_prompt_for_config_dict(monkeypatch):
    """Verify `prompt_for_config` call `read_user_variable` on dict request."""
    monkeypatch.setattr(
        "cookie_composer.cc_overrides.read_user_dict",
        lambda var, default, prompts, prefix: {"key": "value", "integer": 37},
    )
    context = {"details": {}}

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)
    assert cookiecutter_dict == {"details": {"key": "value", "integer": 37}}


def test_should_render_dict():
    """Verify template inside dictionary variable rendered."""
    context = {
        "project_name": "Slartibartfast",
        "details": {"{{cookiecutter.project_name}}": "{{cookiecutter.project_name}}"},
    }

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)
    assert cookiecutter_dict == {
        "project_name": "Slartibartfast",
        "details": {"Slartibartfast": "Slartibartfast"},
    }


def test_should_render_deep_dict():
    """Verify nested structures like dict in dict, rendered correctly."""
    context = {
        "project_name": "Slartibartfast",
        "details": {
            "key": "value",
            "integer_key": 37,
            "other_name": "{{cookiecutter.project_name}}",
            "dict_key": {
                "deep_key": "deep_value",
                "deep_integer": 42,
                "deep_other_name": "{{cookiecutter.project_name}}",
                "deep_list": [
                    "deep value 1",
                    "{{cookiecutter.project_name}}",
                    "deep value 3",
                ],
            },
            "list_key": [
                "value 1",
                "{{cookiecutter.project_name}}",
                "value 3",
            ],
        },
    }

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)
    assert cookiecutter_dict == {
        "project_name": "Slartibartfast",
        "details": {
            "key": "value",
            "integer_key": "37",
            "other_name": "Slartibartfast",
            "dict_key": {
                "deep_key": "deep_value",
                "deep_integer": "42",
                "deep_other_name": "Slartibartfast",
                "deep_list": ["deep value 1", "Slartibartfast", "deep value 3"],
            },
            "list_key": ["value 1", "Slartibartfast", "value 3"],
        },
    }


def test_prompt_for_templated_config(monkeypatch):
    """Verify Jinja2 templating works in unicode prompts."""
    monkeypatch.setattr(
        "cookie_composer.cc_overrides.read_user_variable", lambda var, default, prompts, prefix: default
    )
    context = OrderedDict(
        [
            ("project_name", "A New Project"),
            (
                "pkg_name",
                '{{ cookiecutter.project_name|lower|replace(" ", "") }}',
            ),
        ]
    )

    exp_cookiecutter_dict = {
        "project_name": "A New Project",
        "pkg_name": "anewproject",
    }
    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)
    assert cookiecutter_dict == exp_cookiecutter_dict


def test_dont_prompt_for_private_context_var(monkeypatch):
    """Verify `read_user_variable` not called for private context variables."""
    monkeypatch.setattr(
        "cookie_composer.cc_overrides.read_user_variable",
        lambda var, default: pytest.fail("Should not try to read a response for private context var"),
    )
    context = {"_copy_without_render": ["*.html"]}
    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)
    assert cookiecutter_dict == {"_copy_without_render": ["*.html"]}


def test_should_render_private_variables_with_two_underscores():
    """Test rendering of private variables with two underscores.

    There are three cases:
    1. Variables beginning with a single underscore are private and not rendered.
    2. Variables beginning with a double underscore are private and are rendered.
    3. Variables beginning with anything other than underscores are not private and
       are rendered.
    """
    context = OrderedDict(
        [
            ("foo", "Hello world"),
            ("bar", 123),
            ("rendered_foo", "{{ cookiecutter.foo|lower }}"),
            ("rendered_bar", 123),
            ("_hidden_foo", "{{ cookiecutter.foo|lower }}"),
            ("_hidden_bar", 123),
            ("__rendered_hidden_foo", "{{ cookiecutter.foo|lower }}"),
            ("__rendered_hidden_bar", 123),
        ]
    )

    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)
    assert cookiecutter_dict == OrderedDict(
        [
            ("foo", "Hello world"),
            ("bar", "123"),
            ("rendered_foo", "hello world"),
            ("rendered_bar", "123"),
            ("_hidden_foo", "{{ cookiecutter.foo|lower }}"),
            ("_hidden_bar", 123),
            ("__rendered_hidden_foo", "hello world"),
            ("__rendered_hidden_bar", "123"),
        ]
    )


def test_should_not_render_private_variables():
    """Verify private(underscored) variables not rendered by `prompt_for_config`.

    Private variables designed to be raw, same as context input.
    """
    context = {
        "project_name": "Skip render",
        "_skip_jinja_template": "{{cookiecutter.project_name}}",
        "_skip_float": 123.25,
        "_skip_integer": 123,
        "_skip_boolean": True,
        "_skip_nested": True,
    }
    cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)
    assert cookiecutter_dict == context


def test_raises_exception_on_missing_variable():
    """A missing variable raises an error."""
    from cookiecutter.exceptions import UndefinedVariableInTemplate

    context = {"project_name": "{{ cookiecutter.i_dont_exist }}"}
    with pytest.raises(UndefinedVariableInTemplate):
        cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)


def test_raises_exception_on_missing_variable_dict():
    """A missing variable raises an error."""
    from cookiecutter.exceptions import UndefinedVariableInTemplate

    context = {"key_a": {"key_b": "{{ cookiecutter.i_dont_exist }}"}}
    with pytest.raises(UndefinedVariableInTemplate):
        cc_overrides.prompt_for_config(context, Context({}), None, no_input=True)


class TestReadUserChoice:
    """Class to unite choices prompt related tests."""

    def test_should_invoke_read_user_choice(self, mocker):
        """Verify the correct function is called for select(list) variables."""
        prompt_choice = mocker.patch(
            "cookie_composer.cc_overrides.prompt_choice_for_config",
            wraps=cc_overrides.prompt_choice_for_config,
        )

        read_user_choice = mocker.patch("cookiecutter.prompt.read_user_choice")
        read_user_choice.return_value = "all"

        read_user_variable = mocker.patch("cookiecutter.prompt.read_user_variable")

        choices = ["landscape", "portrait", "all"]
        context = {"orientation": choices}

        cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)

        assert not read_user_variable.called
        assert prompt_choice.called
        read_user_choice.assert_called_once_with("orientation", choices, {}, "  [dim][1/1][/] ")
        assert cookiecutter_dict == {"orientation": "all"}

    def test_should_invoke_read_user_variable(self, mocker):
        """Verify correct function called for string input variables."""
        read_user_variable = mocker.patch("cookie_composer.cc_overrides.read_user_variable")
        read_user_variable.return_value = "Audrey Roy"

        prompt_choice = mocker.patch("cookie_composer.cc_overrides.prompt_choice_for_config")

        read_user_choice = mocker.patch("cookiecutter.prompt.read_user_choice")

        context = {"full_name": "Your Name"}

        cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)

        assert not prompt_choice.called
        assert not read_user_choice.called
        read_user_variable.assert_called_once_with("full_name", "Your Name", {}, "  [dim][1/1][/] ")
        assert cookiecutter_dict == {"full_name": "Audrey Roy"}

    def test_should_render_choices(self, mocker):
        """Verify Jinja2 templating engine works inside choices variables."""
        read_user_choice = mocker.patch("cookiecutter.prompt.read_user_choice")
        read_user_choice.return_value = "anewproject"

        read_user_variable = mocker.patch("cookie_composer.cc_overrides.read_user_variable")
        read_user_variable.return_value = "A New Project"

        rendered_choices = ["foo", "anewproject", "bar"]

        context = OrderedDict(
            [
                ("project_name", "A New Project"),
                (
                    "pkg_name",
                    [
                        "foo",
                        '{{ cookiecutter.project_name|lower|replace(" ", "") }}',
                        "bar",
                    ],
                ),
            ]
        )

        expected = {
            "project_name": "A New Project",
            "pkg_name": "anewproject",
        }
        cookiecutter_dict = cc_overrides.prompt_for_config(context, Context({}), None)

        read_user_variable.assert_called_once_with("project_name", "A New Project", {}, "  [dim][1/2][/] ")
        read_user_choice.assert_called_once_with("pkg_name", rendered_choices, {}, "  [dim][2/2][/] ")
        assert cookiecutter_dict == expected
