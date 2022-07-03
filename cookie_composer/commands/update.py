"""The implementation of the update command."""
from typing import List, Optional

from pathlib import Path

from cookiecutter.config import get_user_config
from cookiecutter.repository import determine_repo_dir

from cookie_composer.composition import (
    Composition,
    RenderedComposition,
    RenderedLayer,
    read_rendered_composition,
    write_rendered_composition,
)
from cookie_composer.exceptions import GitError
from cookie_composer.git_commands import (
    branch_exists,
    branch_from_first_commit,
    checkout_branch,
    get_repo,
    remote_branch_exists,
)
from cookie_composer.layers import render_layers
from cookie_composer.utils import echo, get_context_for_layer


def update_cmd(destination_dir: Optional[Path] = None, no_input: bool = False):
    """
    Update the project with the latest versions of each layer.

    Args:
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

    # Get the merged context for all layers
    initial_context = get_context_for_layer(proj_composition)

    update_composition = Composition(layers=[])
    for rendered_layer in proj_composition.layers:
        if not layer_needs_rendering(rendered_layer):
            echo(f"{rendered_layer.layer.layer_name} is already up-to-date.")
            continue
        update_composition.layers.append(rendered_layer.layer)

    if not update_composition.layers:
        echo("Done.")
        return

    repo = get_repo(destination_dir)
    branch_name = "update_composition"
    if branch_exists(repo, branch_name) or remote_branch_exists(repo, branch_name):
        checkout_branch(repo, branch_name)
    else:
        branch_from_first_commit(repo, branch_name)

    rendered_layers = render_layers(
        update_composition.layers, output_dir, initial_context=initial_context, no_input=no_input, accept_hooks=False
    )
    new_composition = update_rendered_composition_layers(proj_composition, rendered_layers)
    write_rendered_composition(new_composition)
    echo("Done.")


def layer_needs_rendering(rendered_layer: RenderedLayer) -> bool:
    """
    Determine if a rendered layer is out of date or otherwise should be rendered.

    If the template is not a git repository, it will always return ``True``.

    Args:
        rendered_layer: The rendered layer configuration

    Returns:
        ``True`` if the rendered layer requires rendering
    """
    user_config = get_user_config(config_file=None, default_config=False)
    repo_dir, _ = determine_repo_dir(
        template=rendered_layer.layer.template,
        abbreviations=user_config["abbreviations"],
        clone_to_dir=user_config["cookiecutters_dir"],
        checkout=rendered_layer.layer.commit or rendered_layer.layer.checkout,
        no_input=rendered_layer.layer.no_input,
        password=rendered_layer.layer.password,
        directory=rendered_layer.layer.directory,
    )
    try:
        template_repo = get_repo(repo_dir, search_parent_directories=True)
        return rendered_layer.latest_commit != template_repo.head.object.hexsha
    except GitError:
        # It probably isn't a git repository
        return True


def update_rendered_composition_layers(
    base: RenderedComposition, updated_layers: List[RenderedLayer]
) -> RenderedComposition:
    """
    Update ``base.layers`` with ``updated_layers`` where layer names match.

    If for some reason a layer exists in ``updated_layers`` but not in ``base``, it is discarded.

    Args:
        base: The base composition whose layers are to be updated
        updated_layers: The new rendered layers

    Raises:
        RuntimeError: If a layer's location  ``render_dir`` properties don't match
        RuntimeError: If the compositions' ``rendered_name`` properties don't match

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

            if base.render_dir != updated_layer.location:
                raise RuntimeError(
                    f"The base rendered location is {base.render_dir}, but the update rendered location is "
                    f"{updated_layer.location}. Something very strange happened and the update failed."
                )

            new_layers.append(updated_layer)
        else:
            new_layers.append(rendered_layer)

    return RenderedComposition(layers=new_layers, render_dir=base.render_dir, rendered_name=base.rendered_name)
