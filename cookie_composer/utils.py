"""Utilities not easily categorized."""
from typing import Optional

from pathlib import Path

from cookie_composer.composition import RenderedComposition
from cookie_composer.data_merge import comprehensive_merge


def get_context_for_layer(composition: RenderedComposition, index: Optional[int] = None) -> dict:
    """
    Merge the contexts for all layers up to index.

    An ``index`` of ``None`` does all the layers.

    Args:
        composition: The rendered composition
        index: Merge the contexts of the layers up to this 0-based index. ``None`` to do all layers.

    Returns:
        The comprehensively merged context
    """
    full_context = {}
    if index is None:
        layers = composition.layers
    else:
        layers = composition.layers[: index + 1]

    for layer in layers:
        full_context = comprehensive_merge(full_context, layer.new_context)

    return full_context


def get_template_name(path_or_url: str) -> str:
    """
    Get the name of the template using the path or URL.

    Args:
        path_or_url: The URL or path to the template

    Raises:
        ValueError: If the path_or_url is not parsable

    Returns:
        The name of the template without extensions
    """
    from urllib.parse import urlparse

    path = urlparse(path_or_url).path
    if not path:
        raise ValueError("There is no path.")

    return Path(path).stem
