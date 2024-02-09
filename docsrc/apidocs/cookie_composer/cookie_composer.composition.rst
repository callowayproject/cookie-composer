:py:mod:`cookie_composer.composition`
=====================================

.. py:module:: cookie_composer.composition

.. autodoc2-docstring:: cookie_composer.composition
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Composition <cookie_composer.composition.Composition>`
     - .. autodoc2-docstring:: cookie_composer.composition.Composition
          :summary:
   * - :py:obj:`RenderedComposition <cookie_composer.composition.RenderedComposition>`
     - .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.composition.logger>`
     - .. autodoc2-docstring:: cookie_composer.composition.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.composition.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.composition.logger

.. py:class:: Composition(**data: typing.Any)
   :canonical: cookie_composer.composition.Composition

   Bases: :py:obj:`pydantic.BaseModel`

   .. autodoc2-docstring:: cookie_composer.composition.Composition

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.composition.Composition.__init__

   .. py:attribute:: layers
      :canonical: cookie_composer.composition.Composition.layers
      :type: typing.List[cookie_composer.layers.LayerConfig]
      :value: None

      .. autodoc2-docstring:: cookie_composer.composition.Composition.layers

.. py:class:: RenderedComposition(**data: typing.Any)
   :canonical: cookie_composer.composition.RenderedComposition

   Bases: :py:obj:`pydantic.BaseModel`

   .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition.__init__

   .. py:attribute:: layers
      :canonical: cookie_composer.composition.RenderedComposition.layers
      :type: typing.List[cookie_composer.layers.RenderedLayer]
      :value: None

      .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition.layers

   .. py:attribute:: render_dir
      :canonical: cookie_composer.composition.RenderedComposition.render_dir
      :type: pydantic.DirectoryPath
      :value: None

      .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition.render_dir

   .. py:attribute:: rendered_name
      :canonical: cookie_composer.composition.RenderedComposition.rendered_name
      :type: str
      :value: None

      .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition.rendered_name

   .. py:property:: layer_names
      :canonical: cookie_composer.composition.RenderedComposition.layer_names
      :type: typing.List[str]

      .. autodoc2-docstring:: cookie_composer.composition.RenderedComposition.layer_names
