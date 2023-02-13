"""The implementation of the add command."""
from typing import Any, Dict, Optional

import logging
from pathlib import Path

from cookie_composer.composition import (
    get_composition_from_path_or_url,
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
    checkout: Optional[str] = None,
    directory: Optional[str] = None,
    overwrite_if_exists: bool = False,
    skip_if_file_exists: bool = False,
    default_config: bool = False,
    initial_context: Optional[Dict[str, Any]] = None,
):
    """
    Add a template or configuration to an existing project.

    Args:
        path_or_url: A URL or string to add the template or configuration
        destination_dir: The project directory to add the layer to
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        checkout: The branch, tag or commit to check out after git clone
        directory: Directory within repo that holds cookiecutter.json file
        overwrite_if_exists: Overwrite the contents of the output directory if it already exists
        skip_if_file_exists: Skip the files in the corresponding directories if they already exist
        default_config: Do not load a config file. Use the defaults instead
        initial_context: The initial context for the composition layer

    Raises:
        GitError: If the destination_dir is not a git repository
        ValueError: If there is not a .composition.yaml file in the destination directory
    """
    destination_dir = Path(destination_dir).resolve() or Path().cwd().resolve()
    output_dir = destination_dir.parent

    # Read the project composition file
    proj_composition_path = destination_dir / ".composition.yaml"
    if not proj_composition_path.exists():  # pragma: no cover
        raise ValueError(f"There is no .composition.yaml file in {destination_dir}")

    proj_composition = read_rendered_composition(proj_composition_path)

    # Read the additional composition
    addl_composition = get_composition_from_path_or_url(
        path_or_url,
        checkout,
        default_config,
        directory,
        no_input,
        output_dir,
        overwrite_if_exists,
        skip_if_file_exists,
        initial_context=initial_context or {},
    )

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
