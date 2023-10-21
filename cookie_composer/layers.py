"""Layer management."""

import copy
import logging
import os
import shutil
import tempfile
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, MutableMapping, Optional

import click
from cookiecutter.config import get_user_config
from cookiecutter.generate import apply_overwrites_to_context, generate_files
from cookiecutter.main import _patch_import_path_for_repo
from pydantic import BaseModel, DirectoryPath, Field, model_validator

from cookie_composer.cc_overrides import CustomStrictEnvironment, prompt_for_config
from cookie_composer.data_merge import DO_NOT_MERGE, Context, comprehensive_merge, get_merge_strategy
from cookie_composer.matching import matches_any_glob
from cookie_composer.merge_files import MERGE_FUNCTIONS

from .templates.types import Template
from .utils import echo

logger = logging.getLogger(__name__)


class WriteStrategy(Enum):
    """How to deal with a file."""

    WRITE = 1
    """Write or overwrite the file."""

    SKIP = 2
    """Skip the file."""

    MERGE = 3
    """Merge the file with an existing file, or write a new file."""


class LayerConfig(BaseModel):
    """Configuration for a layer of a composition."""

    #
    # Template specification
    #
    template: Template
    """Information about the template."""

    #
    # Input specification
    #
    no_input: bool = False
    """Do not prompt for parameters and only use cookiecutter.json file content.

    This is only used for initial generation. After initial generation, the results
    are stored in the context."""

    initial_context: MutableMapping[str, Any] = Field(default_factory=dict)
    """Dictionary that will provide values for input."""

    #
    # File generation
    #
    skip_hooks: bool = False
    """Skip the template hooks."""

    skip_if_file_exists: bool = True
    """Skip the files in the corresponding directories if they already exist."""

    skip_generation: List[str] = Field(default_factory=list)
    """Paths or glob patterns to skip attempting to generate."""

    overwrite: List[str] = Field(default_factory=list)
    """Paths or glob patterns to always overwrite."""

    overwrite_exclude: List[str] = Field(default_factory=list)
    """Paths or glob patterns to exclude from overwriting."""

    merge_strategies: Dict[str, str] = Field(default_factory=lambda: {"*": DO_NOT_MERGE})
    """The method to merge specific paths or glob patterns."""

    _commit: Optional[str] = None
    """Used when updating layers."""

    @property
    def layer_name(self) -> str:
        """The name of the template layer."""
        return self.template.name

    def generate_context(
        self,
        default_context: MutableMapping[str, Any],
    ) -> OrderedDict:
        """
        Get the context for prompting the user for values.

        The order of precedence is:
        1. `initial_context` from the composition or command-line
        2. `default_context` from the user_config
        3. `raw context` from the template

        Equivalent to `cookiecutter.generate.generate_context` but with the following differences:
        1. Reading the raw context file is handled by the layer's template
        2. The layer's initial context is treated as the `extra_context`
        3. Does not namespace the context with `{"cookiecutter": ...}`

        Args:
            default_context: The default context from the user_config

        Returns:
            A dict containing the context for prompting the user
        """
        raw_context = self.template.context or {}
        user_context = copy.deepcopy(default_context)
        layer_initial_context = copy.deepcopy(self.initial_context)

        # _copy_without_render is template-specific and fails if overridden,
        # So we are going to remove it from the "defaults" when generating the context
        user_context.pop("_copy_without_render", None)
        layer_initial_context.pop("_copy_without_render", None)

        # This pulls in the template context and overrides the values with the user config defaults
        #   and the defaults specified in the layer.
        if default_context:
            try:
                apply_overwrites_to_context(raw_context, default_context)
            except ValueError as error:
                echo(f"Invalid user default received: {error}")
        if layer_initial_context:
            apply_overwrites_to_context(raw_context, layer_initial_context)

        return OrderedDict(raw_context)


class RenderedLayer(BaseModel):
    """Information about a rendered layer."""

    layer: LayerConfig
    """The original layer configuration that was rendered."""

    location: DirectoryPath
    """The directory where the layer was rendered."""

    rendered_context: MutableMapping[str, Any]
    """The context based on questions asked."""

    rendered_commit: Optional[str] = None
    """If a git template, this is the commit of the template that was rendered."""

    rendered_name: Optional[str] = None
    """The name of the rendered template directory."""

    @property
    def latest_commit(self) -> Optional[str]:
        """The latest commit checked out if the layer source was a git repo."""
        return self.layer.template.repo.latest_sha

    @model_validator(mode="before")
    @classmethod
    def set_rendered_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Set the :attr:`~.RenderedLayer.layer_name`` to the name of the rendered template directory."""
        if "rendered_name" in values:
            return values

        dirs = list(os.scandir(values["location"]))
        if len(dirs) > 1:
            raise ValueError("More than one item in render location.")
        elif not dirs:
            raise ValueError("There are no items in render location.")
        if not dirs[0].is_dir():
            raise ValueError("The rendered template is not a directory.")
        values["rendered_name"] = dirs[0].name
        return values


def get_write_strategy(origin: Path, destination: Path, rendered_layer: RenderedLayer) -> WriteStrategy:
    """
    Based on the layer_config rules, determine if we should overwrite an existing path.

    Args:
        origin: Path within the rendered layer that we are evaluating.
        destination: Path to which we would write this file (may not actually exist)
        rendered_layer: Rendered layer configuration.

    Returns:
        The appropriate way to handle writing this file.
    """
    if matches_any_glob(origin, rendered_layer.layer.skip_generation):
        logger.debug(f"{origin} matches a skip_generation pattern. Skipping.")
        return WriteStrategy.SKIP

    if not destination.exists():
        logger.debug(f"{destination} does not exist. Writing.")
        return WriteStrategy.WRITE

    merge_strat = get_merge_strategy(origin, rendered_layer.layer.merge_strategies)
    if merge_strat != DO_NOT_MERGE:
        logger.debug("Strategy is not do-not-merge. Merging.")
        return WriteStrategy.MERGE
    logger.debug("Strategy is do-not-merge. Continuing evaluation.")

    if matches_any_glob(origin, rendered_layer.layer.overwrite_exclude):
        logger.debug(f"{origin} matches an overwrite_exclude pattern. Skipping.")
        return WriteStrategy.SKIP

    if matches_any_glob(origin, rendered_layer.layer.overwrite):
        logger.debug(f"{origin} matches an overwrite pattern. Writing.")
        return WriteStrategy.WRITE

    if rendered_layer.layer.skip_if_file_exists:
        logger.debug("skip_if_file_exists is True. Skipping.")
        return WriteStrategy.SKIP
    else:
        logger.debug("skip_if_file_exists is False. Writing.")
        return WriteStrategy.WRITE


def get_template_rendered_name(template: Template, context: MutableMapping) -> str:
    """Find and render the template's root directory's name."""
    from cookiecutter.find import find_template

    template_dir = find_template(template.cached_path)
    envvars = context.get("cookiecutter", {}).get("_jinja2_env_vars", {})
    env = CustomStrictEnvironment(context=context, keep_trailing_newline=True, **envvars)
    name_tmpl = env.from_string(template_dir.name)
    return name_tmpl.render(**context)


def render_layer(
    layer_config: LayerConfig,
    render_dir: Path,
    full_context: Optional[Context] = None,
    commit: Optional[str] = None,
    accept_hooks: str = "yes",
) -> RenderedLayer:
    """
    Process one layer of the template composition.

    Renders the template using cookiecutter.

    Args:
        layer_config: The configuration of the layer to render
        render_dir: Where to render the template
        full_context: The extra context from all layers in the composition
        commit: The commit to checkout if the template is a git repo
        accept_hooks: Accept pre- and post-hooks if set to ``True``

    Returns:
        The rendered layer information
    """
    full_context = full_context or Context()
    user_config = get_user_config(config_file=None, default_config=False)
    repo_dir = layer_config.template.cached_path

    default_context = user_config.get("default_context", {})
    context = layer_config.generate_context(
        default_context=default_context,
    )
    context_for_prompting = {k: v for k, v in context.items() if (k not in full_context or k.startswith("_"))}
    layer_context = get_layer_context(
        template_repo_dir=repo_dir,
        context_for_prompting=context_for_prompting,
        initial_context=layer_config.initial_context or {},
        full_context=full_context,
        no_input=layer_config.no_input,
    )
    cookiecutter_context = {"cookiecutter": layer_context}

    if accept_hooks == "ask":
        _accept_hooks = click.confirm("Do you want to execute hooks?")
    else:
        _accept_hooks = accept_hooks == "yes"

    rendered_name = get_template_rendered_name(layer_config.template, cookiecutter_context)

    # call cookiecutter's generate files function
    with layer_config.template.repo.render_source(commit=commit) as repo_dir:
        if layer_config.template.directory:
            repo_dir = repo_dir / layer_config.template.directory  # NOQA: PLW2901
        generate_files(
            repo_dir=repo_dir,
            context=cookiecutter_context,
            overwrite_if_exists=False,
            output_dir=str(render_dir),
            accept_hooks=_accept_hooks,
        )

    rendered_layer = RenderedLayer(
        layer=layer_config,
        location=render_dir,
        rendered_context=copy.deepcopy(layer_context),
        rendered_commit=commit or layer_config.template.repo.latest_sha,
        rendered_name=rendered_name,
    )

    layer_config.template.cleanup()

    return rendered_layer


def get_layer_context(
    template_repo_dir: Path,
    context_for_prompting: dict,
    initial_context: MutableMapping[str, Any],
    full_context: Context,
    no_input: bool = False,
) -> dict:
    """
    Get the context for a layer pre-rendering values using previous layers contexts as defaults.

    The layer context is the combination of several things:

    - raw layer context (contents of the cookiecutter.json file)
    - The user's default context (from the user's cookiecutter config file)
    - initial context set in the template composition (or {} if not a composition or not set)
    - initial context passed in by user (as set from the command line.
        This is merged into the layer's inital context when the layer is deserialized. See
        :func:`cookie_composer.io.get_composition_from_path_or_url`)
    - context from previous layers


    Args:
        template_repo_dir: The location of the template repo to use for rendering
        context_for_prompting: The raw context from the cookiecutter.json file with user defaults applied
        initial_context: The initial context from the layer configuration
        full_context: A full context from previous layers.
        no_input: If ``False`` do not prompt for missing values and use defaults instead.

    Returns:
        A dict containing the context for rendering the layer
    """
    import_patch = _patch_import_path_for_repo(template_repo_dir)
    with import_patch:
        prompted_context = prompt_for_config(context_for_prompting, full_context, initial_context, no_input)
        context_for_prompting.update(prompted_context)
    return context_for_prompting


def render_layers(
    layers: List[LayerConfig],
    destination: Path,
    initial_context: Optional[dict] = None,
    no_input: bool = False,
    accept_hooks: str = "all",
) -> List[RenderedLayer]:
    """
    Render layers to a destination.

    Args:
        layers: A list of ``LayerConfig`` to render
        destination: The location to merge the rendered layers to
        initial_context: An initial context to pass to the rendering
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        accept_hooks: How to process pre/post hooks.

    Returns:
        A list of the rendered layer information
    """
    full_context = Context(initial_context) if initial_context else Context()
    rendered_layers = []
    num_layers = len(layers)
    accept_hooks_layers = get_accept_hooks_per_layer(accept_hooks, num_layers)

    for layer_config, accept_hook in zip(layers, accept_hooks_layers):
        layer_config.no_input = True if no_input else layer_config.no_input
        with tempfile.TemporaryDirectory() as render_dir:
            rendered_layer = render_layer(
                layer_config, Path(render_dir), full_context, layer_config._commit, accept_hook
            )
            merge_layers(destination, rendered_layer)
            full_context.update(rendered_layer.rendered_context)
        rendered_layer.location = destination
        merged_context = comprehensive_merge(rendered_layer.rendered_context, rendered_layer.layer.initial_context)
        rendered_layer.layer.initial_context = merged_context  # type: ignore[assignment]
        rendered_layers.append(rendered_layer)
        full_context = full_context.new_child(merged_context)

    return rendered_layers


def get_accept_hooks_per_layer(accept_hooks: str, num_layers: int) -> list:
    """Convert a single accept_hooks value into a value for every layer based on num_layers."""
    if accept_hooks in {"yes", "all"}:
        accept_hooks_layers = ["yes"] * num_layers
    elif accept_hooks in {"no", "none"}:
        accept_hooks_layers = ["no"] * num_layers
    elif accept_hooks == "first":
        accept_hooks_layers = ["no"] * num_layers
        accept_hooks_layers[0] = "yes"
    elif accept_hooks == "last":
        accept_hooks_layers = ["no"] * num_layers
        accept_hooks_layers[-1] = "yes"
    else:
        accept_hooks_layers = ["ask"] * num_layers
    return accept_hooks_layers


def merge_layers(destination: Path, rendered_layer: RenderedLayer) -> None:
    """
    Merge a layer into another layer using the rules specified in the layer_config.

    Args:
        destination: The root path to merge into.
        rendered_layer: The information about the rendered layer.
    """
    for root, dirs, files in os.walk(rendered_layer.location):
        rel_root = Path(root).relative_to(rendered_layer.location)

        for f in files:
            dest_path = destination / rel_root / f
            origin_path = Path(f"{root}/{f}")
            write_strat = get_write_strategy(origin_path, dest_path, rendered_layer)
            if write_strat == WriteStrategy.MERGE:
                merge_strategy = get_merge_strategy(origin_path, rendered_layer.layer.merge_strategies)
                MERGE_FUNCTIONS[dest_path.suffix](origin_path, dest_path, merge_strategy)
            elif write_strat == WriteStrategy.WRITE:
                shutil.copy(origin_path, dest_path)

        for d in dirs:
            dest_path = destination / rel_root / d
            origin_path = Path(f"{root}/{d}")
            write_strat = get_write_strategy(origin_path, dest_path, rendered_layer)
            if write_strat in {WriteStrategy.WRITE, WriteStrategy.MERGE}:
                dest_path.mkdir(parents=True, exist_ok=True)
