"""Project configuration and options."""
import logging
from typing import List

from pydantic import BaseModel, DirectoryPath

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

    The ``render_dir`` + ``rendered_name`` is the location of the project."""

    rendered_name: str
    """The name of the rendered project."""

    @property
    def layer_names(self) -> List[str]:
        """Return a list of the names of all the layers."""
        return [x.layer.layer_name for x in self.layers]
