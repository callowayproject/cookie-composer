:py:mod:`cookie_composer.layers`
================================

.. py:module:: cookie_composer.layers

.. autodoc2-docstring:: cookie_composer.layers
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`WriteStrategy <cookie_composer.layers.WriteStrategy>`
     - .. autodoc2-docstring:: cookie_composer.layers.WriteStrategy
          :summary:
   * - :py:obj:`LayerConfig <cookie_composer.layers.LayerConfig>`
     - .. autodoc2-docstring:: cookie_composer.layers.LayerConfig
          :summary:
   * - :py:obj:`RenderedLayer <cookie_composer.layers.RenderedLayer>`
     - .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_write_strategy <cookie_composer.layers.get_write_strategy>`
     - .. autodoc2-docstring:: cookie_composer.layers.get_write_strategy
          :summary:
   * - :py:obj:`get_template_rendered_name <cookie_composer.layers.get_template_rendered_name>`
     - .. autodoc2-docstring:: cookie_composer.layers.get_template_rendered_name
          :summary:
   * - :py:obj:`render_layer <cookie_composer.layers.render_layer>`
     - .. autodoc2-docstring:: cookie_composer.layers.render_layer
          :summary:
   * - :py:obj:`get_layer_context <cookie_composer.layers.get_layer_context>`
     - .. autodoc2-docstring:: cookie_composer.layers.get_layer_context
          :summary:
   * - :py:obj:`render_layers <cookie_composer.layers.render_layers>`
     - .. autodoc2-docstring:: cookie_composer.layers.render_layers
          :summary:
   * - :py:obj:`get_accept_hooks_per_layer <cookie_composer.layers.get_accept_hooks_per_layer>`
     - .. autodoc2-docstring:: cookie_composer.layers.get_accept_hooks_per_layer
          :summary:
   * - :py:obj:`merge_layers <cookie_composer.layers.merge_layers>`
     - .. autodoc2-docstring:: cookie_composer.layers.merge_layers
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.layers.logger>`
     - .. autodoc2-docstring:: cookie_composer.layers.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.layers.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.layers.logger

.. py:class:: WriteStrategy
   :canonical: cookie_composer.layers.WriteStrategy

   Bases: :py:obj:`enum.Enum`

   .. autodoc2-docstring:: cookie_composer.layers.WriteStrategy

   .. py:attribute:: WRITE
      :canonical: cookie_composer.layers.WriteStrategy.WRITE
      :value: 1

      .. autodoc2-docstring:: cookie_composer.layers.WriteStrategy.WRITE

   .. py:attribute:: SKIP
      :canonical: cookie_composer.layers.WriteStrategy.SKIP
      :value: 2

      .. autodoc2-docstring:: cookie_composer.layers.WriteStrategy.SKIP

   .. py:attribute:: MERGE
      :canonical: cookie_composer.layers.WriteStrategy.MERGE
      :value: 3

      .. autodoc2-docstring:: cookie_composer.layers.WriteStrategy.MERGE

.. py:class:: LayerConfig(**data: typing.Any)
   :canonical: cookie_composer.layers.LayerConfig

   Bases: :py:obj:`pydantic.BaseModel`

   .. autodoc2-docstring:: cookie_composer.layers.LayerConfig

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.__init__

   .. py:attribute:: template
      :canonical: cookie_composer.layers.LayerConfig.template
      :type: cookie_composer.templates.types.Template
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.template

   .. py:attribute:: no_input
      :canonical: cookie_composer.layers.LayerConfig.no_input
      :type: bool
      :value: False

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.no_input

   .. py:attribute:: initial_context
      :canonical: cookie_composer.layers.LayerConfig.initial_context
      :type: typing.MutableMapping[str, typing.Any]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.initial_context

   .. py:attribute:: skip_hooks
      :canonical: cookie_composer.layers.LayerConfig.skip_hooks
      :type: bool
      :value: False

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.skip_hooks

   .. py:attribute:: skip_if_file_exists
      :canonical: cookie_composer.layers.LayerConfig.skip_if_file_exists
      :type: bool
      :value: True

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.skip_if_file_exists

   .. py:attribute:: skip_generation
      :canonical: cookie_composer.layers.LayerConfig.skip_generation
      :type: typing.List[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.skip_generation

   .. py:attribute:: overwrite
      :canonical: cookie_composer.layers.LayerConfig.overwrite
      :type: typing.List[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.overwrite

   .. py:attribute:: overwrite_exclude
      :canonical: cookie_composer.layers.LayerConfig.overwrite_exclude
      :type: typing.List[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.overwrite_exclude

   .. py:attribute:: merge_strategies
      :canonical: cookie_composer.layers.LayerConfig.merge_strategies
      :type: typing.Dict[str, str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.merge_strategies

   .. py:property:: layer_name
      :canonical: cookie_composer.layers.LayerConfig.layer_name
      :type: str

      .. autodoc2-docstring:: cookie_composer.layers.LayerConfig.layer_name

.. py:class:: RenderedLayer(**data: typing.Any)
   :canonical: cookie_composer.layers.RenderedLayer

   Bases: :py:obj:`pydantic.BaseModel`

   .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.__init__

   .. py:attribute:: layer
      :canonical: cookie_composer.layers.RenderedLayer.layer
      :type: cookie_composer.layers.LayerConfig
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.layer

   .. py:attribute:: location
      :canonical: cookie_composer.layers.RenderedLayer.location
      :type: pydantic.DirectoryPath
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.location

   .. py:attribute:: rendered_context
      :canonical: cookie_composer.layers.RenderedLayer.rendered_context
      :type: typing.MutableMapping[str, typing.Any]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.rendered_context

   .. py:attribute:: rendered_commit
      :canonical: cookie_composer.layers.RenderedLayer.rendered_commit
      :type: typing.Optional[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.rendered_commit

   .. py:attribute:: rendered_name
      :canonical: cookie_composer.layers.RenderedLayer.rendered_name
      :type: typing.Optional[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.rendered_name

   .. py:property:: latest_commit
      :canonical: cookie_composer.layers.RenderedLayer.latest_commit
      :type: typing.Optional[str]

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.latest_commit

   .. py:method:: set_rendered_name(values: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]
      :canonical: cookie_composer.layers.RenderedLayer.set_rendered_name
      :classmethod:

      .. autodoc2-docstring:: cookie_composer.layers.RenderedLayer.set_rendered_name

.. py:function:: get_write_strategy(origin: pathlib.Path, destination: pathlib.Path, rendered_layer: cookie_composer.layers.RenderedLayer) -> cookie_composer.layers.WriteStrategy
   :canonical: cookie_composer.layers.get_write_strategy

   .. autodoc2-docstring:: cookie_composer.layers.get_write_strategy

.. py:function:: get_template_rendered_name(template: cookie_composer.templates.types.Template, context: typing.MutableMapping) -> str
   :canonical: cookie_composer.layers.get_template_rendered_name

   .. autodoc2-docstring:: cookie_composer.layers.get_template_rendered_name

.. py:function:: render_layer(layer_config: cookie_composer.layers.LayerConfig, render_dir: pathlib.Path, full_context: typing.Optional[cookie_composer.data_merge.Context] = None, accept_hooks: str = 'yes') -> cookie_composer.layers.RenderedLayer
   :canonical: cookie_composer.layers.render_layer

   .. autodoc2-docstring:: cookie_composer.layers.render_layer

.. py:function:: get_layer_context(layer_config: cookie_composer.layers.LayerConfig, user_config: dict, full_context: typing.Optional[cookie_composer.data_merge.Context] = None) -> cookie_composer.data_merge.Context
   :canonical: cookie_composer.layers.get_layer_context

   .. autodoc2-docstring:: cookie_composer.layers.get_layer_context

.. py:function:: render_layers(layers: typing.List[cookie_composer.layers.LayerConfig], destination: pathlib.Path, initial_context: typing.Optional[dict] = None, no_input: bool = False, accept_hooks: str = 'all') -> typing.List[cookie_composer.layers.RenderedLayer]
   :canonical: cookie_composer.layers.render_layers

   .. autodoc2-docstring:: cookie_composer.layers.render_layers

.. py:function:: get_accept_hooks_per_layer(accept_hooks: str, num_layers: int) -> list
   :canonical: cookie_composer.layers.get_accept_hooks_per_layer

   .. autodoc2-docstring:: cookie_composer.layers.get_accept_hooks_per_layer

.. py:function:: merge_layers(destination: pathlib.Path, rendered_layer: cookie_composer.layers.RenderedLayer) -> None
   :canonical: cookie_composer.layers.merge_layers

   .. autodoc2-docstring:: cookie_composer.layers.merge_layers
