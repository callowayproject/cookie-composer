:py:mod:`cookie_composer.commands.create`
=========================================

.. py:module:: cookie_composer.commands.create

.. autodoc2-docstring:: cookie_composer.commands.create
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`create_cmd <cookie_composer.commands.create.create_cmd>`
     - .. autodoc2-docstring:: cookie_composer.commands.create.create_cmd
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.commands.create.logger>`
     - .. autodoc2-docstring:: cookie_composer.commands.create.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.commands.create.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.commands.create.logger

.. py:function:: create_cmd(path_or_url: str, output_dir: typing.Optional[pathlib.Path] = None, no_input: bool = False, checkout: typing.Optional[str] = None, directory: typing.Optional[str] = None, overwrite_if_exists: bool = False, skip_if_file_exists: bool = False, default_config: bool = False, accept_hooks: str = 'all', initial_context: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> pathlib.Path
   :canonical: cookie_composer.commands.create.create_cmd

   .. autodoc2-docstring:: cookie_composer.commands.create.create_cmd
