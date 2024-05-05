"""The implementation of the update command."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

from cookie_composer.composition import RenderedComposition, get_context_for_layer
from cookie_composer.diff import get_diff
from cookie_composer.git_commands import apply_patch, checkout_branch, get_repo
from cookie_composer.io import read_rendered_composition, write_rendered_composition
from cookie_composer.layers import RenderedLayer, render_layers
from cookie_composer.utils import (
    echo,
    get_deleted_files,
    remove_paths,
)


def update_cmd(project_dir: Optional[Path] = None, no_input: bool = False) -> None:
    """
    Update the project with the latest versions of each layer.

    Args:
        project_dir: The project directory to update. Defaults to current directory.
        no_input: If `True` force each layer's `no_input` attribute to `True`

    Raises:
        GitError: If the destination_dir is not a git repository
        ValueError: If there is not a .composition.yaml file in the destination directory
    """
    project_dir = Path(project_dir).resolve() or Path().cwd().resolve()
    repo = get_repo(project_dir)
    previously_untracked_files = set(repo.untracked_files)

    # Read the project composition file
    proj_composition_path = project_dir / ".composition.yaml"
    if not proj_composition_path.exists():
        raise ValueError(f"There is no .composition.yaml file in {project_dir}")

    proj_composition = read_rendered_composition(proj_composition_path)

    # Get the merged context for all layers
    initial_context = get_context_for_layer(proj_composition)

    update_layers = []
    requires_updating = False
    for rendered_layer in proj_composition.layers:
        latest_template_sha = rendered_layer.layer.template.repo.latest_sha
        if latest_template_sha is None or latest_template_sha != rendered_layer.rendered_commit:
            requires_updating = True
        new_layer = rendered_layer.layer.model_copy(deep=True, update={"_commit": latest_template_sha})
        update_layers.append(new_layer)

    if not requires_updating:
        echo("All layers are up-to-date.")
        return

    with TemporaryDirectory() as tempdir:
        current_state_dir = Path(tempdir) / "current_state"
        current_state_dir.mkdir(exist_ok=True)

        current_layers = []
        for layer in proj_composition.layers:
            layer_config = layer.layer
            layer_config._commit = layer.rendered_commit
            layer_config.initial_context = layer.rendered_context
            current_layers.append(layer_config)

        current_rendered_layers = render_layers(
            current_layers,
            current_state_dir,
            initial_context=initial_context,
            no_input=no_input,
            accept_hooks="none",
        )
        remove_paths(current_state_dir, {Path(".git")})  # don't want the .git dir, if it exists
        current_composition = update_rendered_composition_layers(proj_composition, current_rendered_layers)

        deleted_paths = get_deleted_files(current_state_dir, project_dir.parent)
        deleted_paths.add(Path(".git"))  # don't want the .git dir, if it exists

        updated_state_dir = Path(tempdir) / "update_state"
        updated_state_dir.mkdir(exist_ok=True)
        updated_rendered_layers = render_layers(
            update_layers,
            updated_state_dir,
            initial_context=initial_context,
            no_input=no_input,
            accept_hooks="none",
        )
        remove_paths(updated_state_dir, deleted_paths)
        updated_composition = update_rendered_composition_layers(proj_composition, updated_rendered_layers)

        # Generate diff
        current_project_dir = current_state_dir / current_composition.rendered_name
        updated_project_dir = updated_state_dir / updated_composition.rendered_name
        diff = get_diff(current_project_dir, updated_project_dir)

        # Create new or checkout branch "update_composition"
        checkout_branch(repo, "update_composition")
        # Apply patch to branch
        apply_patch(repo, diff)
        write_rendered_composition(updated_composition)

        # Commit changed files and newly created files
        changed_files = [item.a_path for item in repo.index.diff(None)]
        untracked_files = set(repo.untracked_files)
        new_untracked_files = untracked_files - previously_untracked_files
        changed_files.extend(list(new_untracked_files))

        if changed_files:
            repo.index.add(changed_files)
            repo.index.commit(message="Updating composition layers")


def update_rendered_composition_layers(
    base: RenderedComposition, updated_layers: List[RenderedLayer]
) -> RenderedComposition:
    """
    Update `base.layers` with `updated_layers` where layer names match.

    If, for some reason, a layer exists in `updated_layers` but not in `base`, it is discarded.

    Args:
        base: The base composition whose layers are to be updated
        updated_layers: The new rendered layers

    Raises:
        RuntimeError: If a layer's location `render_dir` properties don't match
        RuntimeError: If the compositions' `rendered_name` properties don't match

    Returns:
        A new composition with updated layers
    """
    updated_layer_names = [x.layer.layer_name for x in updated_layers]

    new_layers = []
    for rendered_layer in base.layers:
        if rendered_layer.layer.layer_name in updated_layer_names:
            index = updated_layer_names.index(rendered_layer.layer.layer_name)
            updated_layer = updated_layers[index]
            if base.rendered_name != updated_layer.rendered_name:
                raise RuntimeError(
                    f"The rendered name of the project has changed from {base.rendered_name} to "
                    f"{updated_layer.rendered_name} when updating layer {updated_layer.layer.layer_name}.\n\n"
                    "You will have to change your project's .composition.yaml "
                    f"file for layer {updated_layer.layer.layer_name}."
                )

            new_layers.append(updated_layer)
        else:
            new_layers.append(rendered_layer)

    return RenderedComposition(layers=new_layers, render_dir=base.render_dir, rendered_name=base.rendered_name)
