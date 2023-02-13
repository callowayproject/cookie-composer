"""The implementation of the link command."""
from typing import Any, Dict, Optional

from pathlib import Path

from cookie_composer.commands.create import create_cmd
from cookie_composer.git_commands import checkout_branch, get_repo


def link_cmd(
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
    Link a template or configuration to an existing project.

    Args:
        path_or_url: A URL or string to add the template or configuration
        destination_dir: The project directory to add the layer to
        no_input: If ``True`` force each layer's ``no_input`` attribute to ``True``
        checkout: The branch, tag or commit to check out after git clone
        directory: Directory within repo that holds cookiecutter.json file
        overwrite_if_exists: Overwrite the contents of the output directory if it already exists
        skip_if_file_exists: Skip the files in the corresponding directories if they already exist
        default_config: Do not load a config file. Use the defaults instead
        initial_context: The initial context for the composition

    Raises:
        GitError: If the destination_dir is not a git repository
        GitError: If the destination_dir git repository is dirty
        ValueError: If there is a .composition.yaml file in the destination directory
    """
    destination_dir = Path(destination_dir).resolve() or Path().cwd().resolve()
    output_dir = destination_dir.parent

    # Make sure the destination directory is a git repository and not dirty
    repo = get_repo(destination_dir, ensure_clean=True)

    # Check for the project composition file
    proj_composition_path = destination_dir / ".composition.yaml"
    if proj_composition_path.exists():
        raise ValueError(f"There is already a .composition.yaml file in {destination_dir}")

    branch_name = "link_composition"
    checkout_branch(repo, branch_name)

    previously_untracked_files = set(repo.untracked_files)

    create_cmd(
        path_or_url,
        output_dir,
        no_input,
        checkout,
        directory,
        overwrite_if_exists,
        skip_if_file_exists,
        default_config,
        initial_context=initial_context or {},
    )

    changed_files = [item.a_path for item in repo.index.diff(None)]
    untracked_files = set(repo.untracked_files)
    new_untracked_files = untracked_files - previously_untracked_files
    changed_files.extend(list(new_untracked_files))

    if changed_files:
        repo.index.add(changed_files)
        repo.index.commit(message="Adding composition layers")
