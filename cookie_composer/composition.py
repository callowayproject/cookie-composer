"""Project configuration and options."""

import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, DirectoryPath

from cookie_composer.data_merge import comprehensive_merge
from cookie_composer.layers import LayerConfig, RenderedLayer

logger = logging.getLogger(__name__)


class Composition(BaseModel):
    """Composition of templates for a project."""

    layers: List[LayerConfig]


class RenderedComposition(BaseModel):
    """A rendered composition of templates for a project."""

    layers: List[RenderedLayer]
    """Rendered layers."""

    render_dir: DirectoryPath
    """The directory in which the layers were rendered.

    The `render_dir` + `rendered_name` is the location of the project."""

    rendered_name: str
    """The name of the rendered project."""

    @property
    def layer_names(self) -> List[str]:
        """Return a list of the names of all the layers."""
        return [x.layer.layer_name for x in self.layers]


def get_context_for_layer(composition: RenderedComposition, index: Optional[int] = None) -> dict:
    """
    Merge the contexts for all layers up to index.

    An `index` of `None` does all the layers.

    Args:
        composition: The rendered composition
        index: Merge the contexts of the layers up to this 0-based index. `None` to do all layers.

    Returns:
        The comprehensively merged context
    """
    full_context: Dict[str, Any] = {}
    if index is None:
        layers = composition.layers
    else:
        layers = composition.layers[: index + 1]

    for layer in layers:
        full_context = comprehensive_merge(full_context, layer.rendered_context)

    return full_context
