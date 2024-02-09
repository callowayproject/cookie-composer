:py:mod:`cookie_composer.utils`
===============================

.. py:module:: cookie_composer.utils

.. autodoc2-docstring:: cookie_composer.utils
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_context_for_layer <cookie_composer.utils.get_context_for_layer>`
     - .. autodoc2-docstring:: cookie_composer.utils.get_context_for_layer
          :summary:
   * - :py:obj:`echo <cookie_composer.utils.echo>`
     - .. autodoc2-docstring:: cookie_composer.utils.echo
          :summary:
   * - :py:obj:`get_deleted_files <cookie_composer.utils.get_deleted_files>`
     - .. autodoc2-docstring:: cookie_composer.utils.get_deleted_files
          :summary:
   * - :py:obj:`remove_paths <cookie_composer.utils.remove_paths>`
     - .. autodoc2-docstring:: cookie_composer.utils.remove_paths
          :summary:
   * - :py:obj:`remove_readonly_bit <cookie_composer.utils.remove_readonly_bit>`
     - .. autodoc2-docstring:: cookie_composer.utils.remove_readonly_bit
          :summary:
   * - :py:obj:`remove_single_path <cookie_composer.utils.remove_single_path>`
     - .. autodoc2-docstring:: cookie_composer.utils.remove_single_path
          :summary:

API
~~~

.. py:function:: get_context_for_layer(composition: cookie_composer.composition.RenderedComposition, index: typing.Optional[int] = None) -> dict
   :canonical: cookie_composer.utils.get_context_for_layer

   .. autodoc2-docstring:: cookie_composer.utils.get_context_for_layer

.. py:function:: echo(message: typing.Optional[typing.Any] = None, file: typing.Optional[typing.IO] = None, nl: bool = True, err: bool = False, color: typing.Optional[bool] = None, **styles) -> None
   :canonical: cookie_composer.utils.echo

   .. autodoc2-docstring:: cookie_composer.utils.echo

.. py:function:: get_deleted_files(template_dir: pathlib.Path, project_dir: pathlib.Path) -> typing.Set[pathlib.Path]
   :canonical: cookie_composer.utils.get_deleted_files

   .. autodoc2-docstring:: cookie_composer.utils.get_deleted_files

.. py:function:: remove_paths(root: pathlib.Path, paths_to_remove: typing.Set[pathlib.Path]) -> None
   :canonical: cookie_composer.utils.remove_paths

   .. autodoc2-docstring:: cookie_composer.utils.remove_paths

.. py:function:: remove_readonly_bit(func: typing.Callable[[str], None], path: str, _: typing.Any) -> None
   :canonical: cookie_composer.utils.remove_readonly_bit

   .. autodoc2-docstring:: cookie_composer.utils.remove_readonly_bit

.. py:function:: remove_single_path(path: pathlib.Path) -> None
   :canonical: cookie_composer.utils.remove_single_path

   .. autodoc2-docstring:: cookie_composer.utils.remove_single_path
