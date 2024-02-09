:py:mod:`cookie_composer.cli`
=============================

.. py:module:: cookie_composer.cli

.. autodoc2-docstring:: cookie_composer.cli
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`cli <cookie_composer.cli.cli>`
     - .. autodoc2-docstring:: cookie_composer.cli.cli
          :summary:
   * - :py:obj:`validate_context_params <cookie_composer.cli.validate_context_params>`
     - .. autodoc2-docstring:: cookie_composer.cli.validate_context_params
          :summary:
   * - :py:obj:`create <cookie_composer.cli.create>`
     - .. autodoc2-docstring:: cookie_composer.cli.create
          :summary:
   * - :py:obj:`add <cookie_composer.cli.add>`
     - .. autodoc2-docstring:: cookie_composer.cli.add
          :summary:
   * - :py:obj:`update <cookie_composer.cli.update>`
     - .. autodoc2-docstring:: cookie_composer.cli.update
          :summary:
   * - :py:obj:`link <cookie_composer.cli.link>`
     - .. autodoc2-docstring:: cookie_composer.cli.link
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.cli.logger>`
     - .. autodoc2-docstring:: cookie_composer.cli.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.cli.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.cli.logger

.. py:function:: cli() -> None
   :canonical: cookie_composer.cli.cli

   .. autodoc2-docstring:: cookie_composer.cli.cli

.. py:function:: validate_context_params(ctx: typing.Any, param: typing.Any, value: list) -> typing.Optional[collections.OrderedDict]
   :canonical: cookie_composer.cli.validate_context_params

   .. autodoc2-docstring:: cookie_composer.cli.validate_context_params

.. py:function:: create(no_input: bool, checkout: str, directory: str, overwrite_if_exists: bool, skip_if_file_exists: bool, default_config: bool, destination: pathlib.Path, accept_hooks: str, path_or_url: str, context_params: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> None
   :canonical: cookie_composer.cli.create

   .. autodoc2-docstring:: cookie_composer.cli.create

.. py:function:: add(no_input: bool, checkout: str, directory: str, overwrite_if_exists: bool, skip_if_file_exists: bool, default_config: bool, destination: pathlib.Path, accept_hooks: str, path_or_url: str, context_params: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> None
   :canonical: cookie_composer.cli.add

   .. autodoc2-docstring:: cookie_composer.cli.add

.. py:function:: update(no_input: bool, destination: pathlib.Path, context_params: typing.Optional[collections.OrderedDict] = None) -> None
   :canonical: cookie_composer.cli.update

   .. autodoc2-docstring:: cookie_composer.cli.update

.. py:function:: link(no_input: bool, checkout: str, directory: str, overwrite_if_exists: bool, skip_if_file_exists: bool, default_config: bool, destination: typing.Optional[pathlib.Path], path_or_url: str, context_params: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> None
   :canonical: cookie_composer.cli.link

   .. autodoc2-docstring:: cookie_composer.cli.link
