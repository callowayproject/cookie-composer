"""This overrides the default cookie cutter environment."""
import json
from typing import Any, List, MutableMapping

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UndefinedVariableInTemplate
from cookiecutter.prompt import (
    prompt_choice_for_config,
    read_user_dict,
    read_user_variable,
    read_user_yes_no,
    render_variable,
)
from jinja2 import Environment, UndefinedError
from jinja2.ext import Extension

from cookie_composer.data_merge import Context


def jsonify_context(value: Any) -> dict:
    """Convert a ``Context`` to a dict."""
    if isinstance(value, Context):
        return value.flatten()

    raise TypeError()


class JsonifyContextExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment: Environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def jsonify(obj: Any) -> str:  # pragma: no cover
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
        if "cookiecutter.extensions.JsonifyExtension" in self.extensions:  # pragma: no cover
            del self.extensions["cookiecutter.extensions.JsonifyExtension"]
        self.add_extension("cookie_composer.cc_overrides.JsonifyContextExtension")

    def _read_extensions(self, context: MutableMapping[str, Any]) -> List[str]:
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


def update_extensions(existing_config: Context, prompts: MutableMapping[str, Any]) -> List[str]:
    """Merge extensions from prompts into existing config."""
    extensions = existing_config.get("_extensions", [])
    if "_extensions" in prompts:
        extensions.extend(prompts["_extensions"])

    return extensions


def prompt_for_config(prompts: dict, existing_config: Context, no_input: bool = False) -> Context:
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
    if "cookiecutter" in prompts:
        prompts = prompts["cookiecutter"]

    # Make sure we have a fresh layer to populate
    if existing_config.is_empty:
        context = existing_config
    else:
        context = existing_config.new_child()

    extensions = update_extensions(existing_config, prompts)
    if extensions:
        context["_extensions"] = extensions
    env = CustomStrictEnvironment(context=existing_config)

    context_prompts = {}
    if "__prompts__" in prompts:
        context_prompts = prompts["__prompts__"]
        del prompts["__prompts__"]

    _render_simple(context, context_prompts, env, no_input, prompts)

    _render_dicts(context, env, no_input, prompts)

    return context


def _render_dicts(context: Context, env: Environment, no_input: bool, prompts: dict) -> None:
    """
    Render dictionaries.

    This is the second pass of rendering. It must be done after the first pass because that renders
    the values that might be used as keys or values in the dictionaries.

    I hate that this uses a side effect to modify the context, but I don't see a better way.

    Args:
        context: The current context
        env: The current environment for rendering
        no_input: Should we prompt the user for input?
        prompts: The default prompts for the context

    Raises:
        UndefinedVariableInTemplate: If a variable in a prompt defaults is not in the context
    """
    # Second pass; handle the dictionaries.
    for key, raw in prompts.items():
        # Skip private type dicts not ot be rendered.
        if key.startswith("_") and not key.startswith("__"):
            continue

        try:
            if isinstance(raw, dict):
                # We are dealing with a dict variable
                val = render_variable(env, raw, context.flatten())

                if not no_input and not key.startswith("__"):
                    val = read_user_dict(key, val, prompts)

                context[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context) from err


def _render_simple(context: Context, context_prompts: dict, env: Environment, no_input: bool, prompts: dict) -> None:
    """
    Render simple variables, raw variables, and choices.

    This is the first pass. It must be done first because the dictionary's keys and
    values might refer to them.

    I hate that this uses a side effect to modify the context, but I don't see a better way.

    Args:
        context: The current context
        context_prompts: The human prompts for the context
        env: The current environment for rendering
        no_input: Should we prompt the user for input?
        prompts: The default prompts for the context

    Raises:
        UndefinedVariableInTemplate: If a variable in a prompt defaults is not in the context
    """
    import copy

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
                val = prompt_choice_for_config(context, env, key, raw, no_input, context_prompts)
                context[key] = val
            elif isinstance(raw, bool):
                # We are dealing with a boolean variable
                if no_input:
                    context[key] = render_variable(env, raw, context)
                else:
                    context[key] = read_user_yes_no(key, raw, context_prompts)
            elif not isinstance(raw, dict):
                # We are dealing with a regular variable
                val = render_variable(env, raw, context)

                if not no_input:
                    val = read_user_variable(key, val, context_prompts)

                context[key] = val
        except UndefinedError as err:
            msg = f"Unable to render variable '{key}'"
            raise UndefinedVariableInTemplate(msg, err, context) from err
