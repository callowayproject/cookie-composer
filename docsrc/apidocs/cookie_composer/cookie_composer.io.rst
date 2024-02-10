:py:mod:`cookie_composer.io`
============================

.. py:module:: cookie_composer.io

.. autodoc2-docstring:: cookie_composer.io
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`serialize_layer <cookie_composer.io.serialize_layer>`
     - .. autodoc2-docstring:: cookie_composer.io.serialize_layer
          :summary:
   * - :py:obj:`deserialize_layer <cookie_composer.io.deserialize_layer>`
     - .. autodoc2-docstring:: cookie_composer.io.deserialize_layer
          :summary:
   * - :py:obj:`serialize_rendered_layer <cookie_composer.io.serialize_rendered_layer>`
     - .. autodoc2-docstring:: cookie_composer.io.serialize_rendered_layer
          :summary:
   * - :py:obj:`deserialize_rendered_layer <cookie_composer.io.deserialize_rendered_layer>`
     - .. autodoc2-docstring:: cookie_composer.io.deserialize_rendered_layer
          :summary:
   * - :py:obj:`serialize_composition <cookie_composer.io.serialize_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.serialize_composition
          :summary:
   * - :py:obj:`deserialize_composition <cookie_composer.io.deserialize_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.deserialize_composition
          :summary:
   * - :py:obj:`serialize_rendered_composition <cookie_composer.io.serialize_rendered_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.serialize_rendered_composition
          :summary:
   * - :py:obj:`deserialize_rendered_composition <cookie_composer.io.deserialize_rendered_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.deserialize_rendered_composition
          :summary:
   * - :py:obj:`read_yaml <cookie_composer.io.read_yaml>`
     - .. autodoc2-docstring:: cookie_composer.io.read_yaml
          :summary:
   * - :py:obj:`write_yaml <cookie_composer.io.write_yaml>`
     - .. autodoc2-docstring:: cookie_composer.io.write_yaml
          :summary:
   * - :py:obj:`is_composition_file <cookie_composer.io.is_composition_file>`
     - .. autodoc2-docstring:: cookie_composer.io.is_composition_file
          :summary:
   * - :py:obj:`read_composition <cookie_composer.io.read_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.read_composition
          :summary:
   * - :py:obj:`read_rendered_composition <cookie_composer.io.read_rendered_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.read_rendered_composition
          :summary:
   * - :py:obj:`write_rendered_composition <cookie_composer.io.write_rendered_composition>`
     - .. autodoc2-docstring:: cookie_composer.io.write_rendered_composition
          :summary:
   * - :py:obj:`get_composition_from_path_or_url <cookie_composer.io.get_composition_from_path_or_url>`
     - .. autodoc2-docstring:: cookie_composer.io.get_composition_from_path_or_url
          :summary:

API
~~~

.. py:function:: serialize_layer(layer: cookie_composer.layers.LayerConfig) -> dict
   :canonical: cookie_composer.io.serialize_layer

   .. autodoc2-docstring:: cookie_composer.io.serialize_layer

.. py:function:: deserialize_layer(layer_info: dict, local_path: typing.Optional[pathlib.Path] = None, **kwargs) -> cookie_composer.layers.LayerConfig
   :canonical: cookie_composer.io.deserialize_layer

   .. autodoc2-docstring:: cookie_composer.io.deserialize_layer

.. py:function:: serialize_rendered_layer(rendered_layer: cookie_composer.layers.RenderedLayer) -> dict
   :canonical: cookie_composer.io.serialize_rendered_layer

   .. autodoc2-docstring:: cookie_composer.io.serialize_rendered_layer

.. py:function:: deserialize_rendered_layer(rendered_layer_info: dict, location: pathlib.Path) -> cookie_composer.layers.RenderedLayer
   :canonical: cookie_composer.io.deserialize_rendered_layer

   .. autodoc2-docstring:: cookie_composer.io.deserialize_rendered_layer

.. py:function:: serialize_composition(layers: typing.List[cookie_composer.layers.LayerConfig]) -> typing.List[dict]
   :canonical: cookie_composer.io.serialize_composition

   .. autodoc2-docstring:: cookie_composer.io.serialize_composition

.. py:function:: deserialize_composition(composition_info: typing.List[dict], local_path: typing.Optional[pathlib.Path] = None, **kwargs) -> cookie_composer.composition.Composition
   :canonical: cookie_composer.io.deserialize_composition

   .. autodoc2-docstring:: cookie_composer.io.deserialize_composition

.. py:function:: serialize_rendered_composition(composition: cookie_composer.composition.RenderedComposition) -> typing.List[dict]
   :canonical: cookie_composer.io.serialize_rendered_composition

   .. autodoc2-docstring:: cookie_composer.io.serialize_rendered_composition

.. py:function:: deserialize_rendered_composition(composition_info: typing.List[dict], location: pathlib.Path) -> cookie_composer.composition.RenderedComposition
   :canonical: cookie_composer.io.deserialize_rendered_composition

   .. autodoc2-docstring:: cookie_composer.io.deserialize_rendered_composition

.. py:function:: read_yaml(path_or_url: typing.Union[str, pathlib.Path]) -> typing.List[dict]
   :canonical: cookie_composer.io.read_yaml

   .. autodoc2-docstring:: cookie_composer.io.read_yaml

.. py:function:: write_yaml(path: pathlib.Path, contents: typing.List[dict]) -> None
   :canonical: cookie_composer.io.write_yaml

   .. autodoc2-docstring:: cookie_composer.io.write_yaml

.. py:function:: is_composition_file(path_or_url: typing.Union[str, pathlib.Path]) -> bool
   :canonical: cookie_composer.io.is_composition_file

   .. autodoc2-docstring:: cookie_composer.io.is_composition_file

.. py:function:: read_composition(path_or_url: typing.Union[str, pathlib.Path], **kwargs) -> cookie_composer.composition.Composition
   :canonical: cookie_composer.io.read_composition

   .. autodoc2-docstring:: cookie_composer.io.read_composition

.. py:function:: read_rendered_composition(path: pathlib.Path) -> cookie_composer.composition.RenderedComposition
   :canonical: cookie_composer.io.read_rendered_composition

   .. autodoc2-docstring:: cookie_composer.io.read_rendered_composition

.. py:function:: write_rendered_composition(composition: cookie_composer.composition.RenderedComposition) -> None
   :canonical: cookie_composer.io.write_rendered_composition

   .. autodoc2-docstring:: cookie_composer.io.write_rendered_composition

.. py:function:: get_composition_from_path_or_url(path_or_url: str, checkout: typing.Optional[str] = None, default_config: bool = False, directory: typing.Optional[str] = None, no_input: bool = False, output_dir: typing.Optional[pathlib.Path] = None, overwrite_if_exists: bool = False, skip_if_file_exists: bool = False, initial_context: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> cookie_composer.composition.Composition
   :canonical: cookie_composer.io.get_composition_from_path_or_url

   .. autodoc2-docstring:: cookie_composer.io.get_composition_from_path_or_url
