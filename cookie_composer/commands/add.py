"""The implementation of the add command."""
from typing import Optional

import logging
from pathlib import Path

from cookie_composer.composition import (
    Composition,
    LayerConfig,
    is_composition_file,
    read_composition,
    read_rendered_composition,
    write_rendered_composition,
)
from cookie_composer.git_commands import (
    branch_exists,
    branch_from_first_commit,
    checkout_branch,
    get_repo,
    remote_branch_exists,
)
from cookie_composer.layers import render_layers
from cookie_composer.utils import get_context_for_layer, get_template_name

logger = logging.getLogger(__name__)


def add_cmd(
    path_or_url: str,
    destination_dir: Optional[Path] = None,
    no_input: bool = False,
):
    """
    Add a template or configuration to an existing project.

    Args:
        path_or_url: A URL or string to add the template or configuration
        destination_dir: The project directory to add the layer to
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``


    Raises:
        GitError: If the destination_dir is not a git repository
        ValueError: If there is not a .composition.yaml file in the destination directory
    """
    destination_dir = Path(destination_dir).resolve() or Path().cwd().resolve()
    output_dir = destination_dir.parent

    # Read the project composition file
    proj_composition_path = destination_dir / ".composition.yaml"
    if not proj_composition_path.exists():
        raise ValueError(f"There is no .composition.yaml file in {destination_dir}")

    proj_composition = read_rendered_composition(proj_composition_path)

    # Read the additional composition
    if is_composition_file(path_or_url):
        addl_composition = read_composition(path_or_url)
        logger.info(f"Adding composition {path_or_url} to {output_dir}.")
    else:
        tmpl = LayerConfig(template=path_or_url)
        addl_composition = Composition(layers=[tmpl])
        logger.info(f"Adding template {path_or_url} to {output_dir}.")

    # Get the merged context for all layers
    initial_context = get_context_for_layer(proj_composition)

    # Make sure the destination directory is a git repository
    repo = get_repo(destination_dir)

    # Create and check out a new branch
    tmpl_name = get_template_name(path_or_url)
    branch_name = f"add_layer_{tmpl_name}"
    if branch_exists(repo, branch_name) or remote_branch_exists(repo, branch_name):
        checkout_branch(repo, branch_name)
    else:
        branch_from_first_commit(repo, branch_name)

    # Render and merge the additional layers
    rendered_layers = render_layers(
        addl_composition.layers, output_dir, initial_context=initial_context, no_input=no_input, accept_hooks=False
    )
    proj_composition.layers.extend(rendered_layers)
    write_rendered_composition(proj_composition)
