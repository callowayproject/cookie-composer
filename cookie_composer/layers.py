"""Layer management."""

from typing import List, Optional

import contextlib
import logging
import os
import shutil
import tempfile
from enum import Enum
from pathlib import Path

from cookiecutter.config import get_user_config
from cookiecutter.generate import generate_context, generate_files
from cookiecutter.repository import determine_repo_dir
from cookiecutter.utils import rmtree

from cookie_composer.cc_overrides import prompt_for_config
from cookie_composer.composition import (
    DO_NOT_MERGE,
    LayerConfig,
    RenderedLayer,
    get_merge_strategy,
)
from cookie_composer.data_merge import Context
from cookie_composer.matching import matches_any_glob
from cookie_composer.merge_files import MERGE_FUNCTIONS

from .exceptions import GitError
from .git_commands import get_latest_template_commit, get_repo

logger = logging.getLogger(__name__)


class WriteStrategy(Enum):
    """How to deal with a file."""

    WRITE = 1
    """Write or overwrite the file."""

    SKIP = 2
    """Skip the file."""

    MERGE = 3
    """Merge the file with an existing file, or write a new file."""


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


def render_layer(
    layer_config: LayerConfig, render_dir: Path, full_context: Optional[Context] = None, accept_hooks: bool = True
) -> RenderedLayer:
    """
    Process one layer of the template composition.

    Renders the template using cookiecutter.

    Args:
        layer_config: The configuration of the layer to render
        render_dir: Where to render the template
        full_context: The extra context from all layers in the composition
        accept_hooks: Accept pre- and post-hooks if set to ``True``

    Returns:
        The rendered layer information
    """
    full_context = full_context or Context()
    user_config = get_user_config(config_file=None, default_config=False)
    repo_dir, cleanup = determine_repo_dir(
        template=layer_config.template,
        abbreviations=user_config["abbreviations"],
        clone_to_dir=user_config["cookiecutters_dir"],
        checkout=layer_config.commit or layer_config.checkout,
        no_input=layer_config.no_input,
        password=layer_config.password,
        directory=layer_config.directory,
    )
    # If it is a local git directory (not a URL) we need to make sure the correct
    # rev is checked out.
    with contextlib.suppress(GitError):
        repo = get_repo(repo_dir)
        repo.git.checkout(layer_config.commit)

    context = get_layer_context(layer_config, repo_dir, user_config, full_context)

    # call cookiecutter's generate files function
    generate_files(
        repo_dir=repo_dir,
        context={"cookiecutter": context.flatten()},
        overwrite_if_exists=False,
        output_dir=str(render_dir),
        accept_hooks=accept_hooks,
    )
    if layer_config.commit is None:
        layer_config.commit = get_latest_template_commit(repo_dir)

    rendered_layer = RenderedLayer(
        layer=layer_config,
        location=render_dir,
        new_context=context.maps[0],
        latest_commit=layer_config.commit,
    )

    if cleanup:
        rmtree(repo_dir)

    return rendered_layer


def get_layer_context(
    layer_config: LayerConfig, repo_dir: str, user_config: dict, full_context: Optional[Context] = None
) -> Context:
    """
    Get the context for a layer pre-rendering values using previous layers contexts as defaults.

    Args:
        layer_config: The configuration for this layer
        repo_dir: The directory containing the template's ``cookiecutter.json`` file
        user_config: The user's cookiecutter configuration
        full_context: A full context from previous layers.

    Returns:
        The context for rendering the layer
    """
    full_context = full_context or Context()

    # _copy_without_render is template-specific and fails if overridden
    # So we are going to remove it from the "defaults" when generating the context
    user_config["default_context"].pop("_copy_without_render", None)
    # if full_context and "_copy_without_render" in full_context:
    #     del full_context["_copy_without_render"]

    # This pulls in the template context and overrides the values with the user config defaults
    #   and the defaults specified in the layer.
    prompts = generate_context(
        context_file=Path(repo_dir) / "cookiecutter.json",
        default_context=user_config["default_context"],
        extra_context=layer_config.context or {},
    )
    return prompt_for_config(prompts["cookiecutter"], full_context, layer_config.no_input)


def render_layers(
    layers: List[LayerConfig],
    destination: Path,
    initial_context: Optional[dict] = None,
    no_input: bool = False,
    accept_hooks: bool = True,
) -> List[RenderedLayer]:
    """
    Render layers to a destination.

    Args:
        layers: A list of ``LayerConfig`` to render
        destination: The location to merge the rendered layers to
        initial_context: An initial context to pass to the rendering
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        accept_hooks: Accept pre- and post-hooks if set to ``True``

    Returns:
        A list of the rendered layer information
    """
    full_context = Context(initial_context) if initial_context else Context()
    rendered_layers = []

    for layer_config in layers:
        layer_config.no_input = True if no_input else layer_config.no_input
        with tempfile.TemporaryDirectory() as render_dir:
            rendered_layer = render_layer(layer_config, render_dir, full_context, accept_hooks)
            merge_layers(destination, rendered_layer)
        rendered_layer.location = destination
        rendered_layer.layer.commit = rendered_layer.latest_commit
        rendered_layer.layer.context = rendered_layer.new_context
        rendered_layers.append(rendered_layer)
        full_context = full_context.new_child(rendered_layer.new_context)

    return rendered_layers


def merge_layers(destination: Path, rendered_layer: RenderedLayer):
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
