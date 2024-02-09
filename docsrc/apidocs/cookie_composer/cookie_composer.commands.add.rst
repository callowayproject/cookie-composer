:py:mod:`cookie_composer.commands.add`
======================================

.. py:module:: cookie_composer.commands.add

.. autodoc2-docstring:: cookie_composer.commands.add
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`add_cmd <cookie_composer.commands.add.add_cmd>`
     - .. autodoc2-docstring:: cookie_composer.commands.add.add_cmd
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.commands.add.logger>`
     - .. autodoc2-docstring:: cookie_composer.commands.add.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.commands.add.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.commands.add.logger

.. py:function:: add_cmd(path_or_url: str, destination_dir: typing.Optional[pathlib.Path] = None, no_input: bool = False, checkout: typing.Optional[str] = None, directory: typing.Optional[str] = None, overwrite_if_exists: bool = False, skip_if_file_exists: bool = False, default_config: bool = False, accept_hooks: str = 'all', initial_context: typing.Optional[typing.MutableMapping[str, typing.Any]] = None) -> None
   :canonical: cookie_composer.commands.add.add_cmd

   .. autodoc2-docstring:: cookie_composer.commands.add.add_cmd
