:py:mod:`cookie_composer.matching`
==================================

.. py:module:: cookie_composer.matching

.. autodoc2-docstring:: cookie_composer.matching
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`rel_fnmatch <cookie_composer.matching.rel_fnmatch>`
     - .. autodoc2-docstring:: cookie_composer.matching.rel_fnmatch
          :summary:
   * - :py:obj:`matches_any_glob <cookie_composer.matching.matches_any_glob>`
     - .. autodoc2-docstring:: cookie_composer.matching.matches_any_glob
          :summary:

API
~~~

.. py:function:: rel_fnmatch(name: str, pat: str) -> bool
   :canonical: cookie_composer.matching.rel_fnmatch

   .. autodoc2-docstring:: cookie_composer.matching.rel_fnmatch

.. py:function:: matches_any_glob(path: typing.Union[str, pathlib.Path], patterns: typing.List[str]) -> bool
   :canonical: cookie_composer.matching.matches_any_glob

   .. autodoc2-docstring:: cookie_composer.matching.matches_any_glob
