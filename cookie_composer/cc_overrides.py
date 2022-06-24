"""This overrides the default cookie cutter environment."""
from typing import Any

import json

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UndefinedVariableInTemplate
from cookiecutter.prompt import (
    prompt_choice_for_config,
    read_user_dict,
    read_user_variable,
    render_variable,
)
from jinja2 import UndefinedError
from jinja2.ext import Extension

from cookie_composer.data_merge import Context


def jsonify_context(value: Any) -> dict:
    """Convert a ``Context`` to a dict."""
    if isinstance(value, Context):
        return value.flatten()

    raise TypeError()


class JsonifyContextExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def jsonify(obj):
            return json.dumps(obj, sort_keys=True, indent=4, default=jsonify_context)

        environment.filters["jsonify"] = jsonify


class CustomStrictEnvironment(StrictEnvironment):
    """
    Create strict Jinja2 environment.

    Jinja2 environment will raise error on undefined variable in template-rendering context.

    Does not expect all the context to be under the `cookiecutter` key.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "cookiecutter.extensions.JsonifyExtension" in self.extensions:
            del self.extensions["cookiecutter.extensions.JsonifyExtension"]
        self.add_extension("cookie_composer.cc_overrides.JsonifyContextExtension")

    def _read_extensions(self, context) -> list[str]:
        """
        Return list of extensions as str to be passed on to the Jinja2 env.

        If context does not contain the relevant info, return an empty
        list instead.

        Args:
            context: A ``dict`` possibly containing the ``_extensions`` key

        Returns:
            List of extensions as str to be passed on to the Jinja2 env
        """
        return [str(ext) for ext in context.get("_extensions", [])]


def prompt_for_config(prompts: dict, existing_config: Context, no_input=False) -> Context:
    """
    Prompt user to enter a new config using an existing config as a basis.

    Will not prompt for configurations already in the existing configuration.

    Prompts can refer to items in the existing config.

    Args:
        prompts: A dictionary of configuration prompts and default values
        existing_config: An existing configuration to use as a basis
        no_input: If ``True`` Don't prompt the user at command line for manual configuration

    Raises:
        UndefinedVariableInTemplate: If a variable in a prompt defaults is not in the context

    Returns:
        A new configuration context
    """
    import copy

    # Make sure we have a fresh layer to populate
    if existing_config.is_empty:
        context = existing_config
    else:
        context = existing_config.new_child()

    env = CustomStrictEnvironment(context=existing_config)

    # First pass: Handle simple and raw variables, plus choices.
    # These must be done first because the dictionaries keys and
    # values might refer to them.
    for key, raw in prompts.items():
        if key.startswith("_") and not key.startswith("__"):
            context[key] = raw
            continue
        elif key.startswith("__"):
            context[key] = render_variable(env, raw, context)
            continue
        elif key in context:
            context[key] = copy.deepcopy(context.parents[key])
            continue

        try:
            if isinstance(raw, list):
                # We are dealing with a choice variable
                val = prompt_choice_for_config(context, env, key, raw, no_input)
                context[key] = val
            elif not isinstance(raw, dict):
                # We are dealing with a regular variable
                val = render_variable(env, raw, context)

                if not no_input:
                    val = read_user_variable(key, val)

                context[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context) from err

    # Second pass; handle the dictionaries.
    for key, raw in prompts.items():
        # Skip private type dicts not ot be rendered.
        if key.startswith("_") and not key.startswith("__"):
            continue

        try:
            if isinstance(raw, dict):
                # We are dealing with a dict variable
                val = render_variable(env, raw, context)

                if not no_input and not key.startswith("__"):
                    val = read_user_dict(key, val)

                context[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context)

    return context
