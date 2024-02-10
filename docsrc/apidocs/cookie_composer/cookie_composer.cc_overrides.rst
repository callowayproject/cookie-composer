:py:mod:`cookie_composer.cc_overrides`
======================================

.. py:module:: cookie_composer.cc_overrides

.. autodoc2-docstring:: cookie_composer.cc_overrides
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`JsonifyContextExtension <cookie_composer.cc_overrides.JsonifyContextExtension>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides.JsonifyContextExtension
          :summary:
   * - :py:obj:`CustomStrictEnvironment <cookie_composer.cc_overrides.CustomStrictEnvironment>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides.CustomStrictEnvironment
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`jsonify_context <cookie_composer.cc_overrides.jsonify_context>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides.jsonify_context
          :summary:
   * - :py:obj:`update_extensions <cookie_composer.cc_overrides.update_extensions>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides.update_extensions
          :summary:
   * - :py:obj:`prompt_for_config <cookie_composer.cc_overrides.prompt_for_config>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides.prompt_for_config
          :summary:
   * - :py:obj:`_render_dicts <cookie_composer.cc_overrides._render_dicts>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides._render_dicts
          :summary:
   * - :py:obj:`_render_simple <cookie_composer.cc_overrides._render_simple>`
     - .. autodoc2-docstring:: cookie_composer.cc_overrides._render_simple
          :summary:

API
~~~

.. py:function:: jsonify_context(value: typing.Any) -> typing.MutableMapping
   :canonical: cookie_composer.cc_overrides.jsonify_context

   .. autodoc2-docstring:: cookie_composer.cc_overrides.jsonify_context

.. py:class:: JsonifyContextExtension(environment: jinja2.Environment)
   :canonical: cookie_composer.cc_overrides.JsonifyContextExtension

   Bases: :py:obj:`jinja2.ext.Extension`

   .. autodoc2-docstring:: cookie_composer.cc_overrides.JsonifyContextExtension

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.cc_overrides.JsonifyContextExtension.__init__

.. py:class:: CustomStrictEnvironment(**kwargs)
   :canonical: cookie_composer.cc_overrides.CustomStrictEnvironment

   Bases: :py:obj:`cookiecutter.environment.StrictEnvironment`

   .. autodoc2-docstring:: cookie_composer.cc_overrides.CustomStrictEnvironment

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.cc_overrides.CustomStrictEnvironment.__init__

   .. py:method:: _read_extensions(context: typing.MutableMapping[str, typing.Any]) -> typing.List[str]
      :canonical: cookie_composer.cc_overrides.CustomStrictEnvironment._read_extensions

      .. autodoc2-docstring:: cookie_composer.cc_overrides.CustomStrictEnvironment._read_extensions

.. py:function:: update_extensions(existing_config: typing.MutableMapping[str, typing.Any], prompts: typing.MutableMapping[str, typing.Any]) -> typing.List[str]
   :canonical: cookie_composer.cc_overrides.update_extensions

   .. autodoc2-docstring:: cookie_composer.cc_overrides.update_extensions

.. py:function:: prompt_for_config(prompts: dict, aggregated_context: cookie_composer.data_merge.Context, layer_context: typing.Optional[typing.MutableMapping[str, typing.Any]] = None, no_input: bool = False) -> typing.MutableMapping[str, typing.Any]
   :canonical: cookie_composer.cc_overrides.prompt_for_config

   .. autodoc2-docstring:: cookie_composer.cc_overrides.prompt_for_config

.. py:function:: _render_dicts(context: typing.MutableMapping, env: jinja2.Environment, no_input: bool, prompts: dict) -> None
   :canonical: cookie_composer.cc_overrides._render_dicts

   .. autodoc2-docstring:: cookie_composer.cc_overrides._render_dicts

.. py:function:: _render_simple(context: typing.MutableMapping, context_prompts: dict, env: jinja2.Environment, no_input: bool, prompts: dict) -> None
   :canonical: cookie_composer.cc_overrides._render_simple

   .. autodoc2-docstring:: cookie_composer.cc_overrides._render_simple
