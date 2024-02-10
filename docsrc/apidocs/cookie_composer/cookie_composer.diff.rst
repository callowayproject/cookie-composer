:py:mod:`cookie_composer.diff`
==============================

.. py:module:: cookie_composer.diff

.. autodoc2-docstring:: cookie_composer.diff
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`_git_diff_command <cookie_composer.diff._git_diff_command>`
     - .. autodoc2-docstring:: cookie_composer.diff._git_diff_command
          :summary:
   * - :py:obj:`get_diff <cookie_composer.diff.get_diff>`
     - .. autodoc2-docstring:: cookie_composer.diff.get_diff
          :summary:
   * - :py:obj:`replace_diff_prefixes <cookie_composer.diff.replace_diff_prefixes>`
     - .. autodoc2-docstring:: cookie_composer.diff.replace_diff_prefixes
          :summary:
   * - :py:obj:`display_diff <cookie_composer.diff.display_diff>`
     - .. autodoc2-docstring:: cookie_composer.diff.display_diff
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`DIFF_SRC_PREFIX <cookie_composer.diff.DIFF_SRC_PREFIX>`
     - .. autodoc2-docstring:: cookie_composer.diff.DIFF_SRC_PREFIX
          :summary:
   * - :py:obj:`DIFF_DST_PREFIX <cookie_composer.diff.DIFF_DST_PREFIX>`
     - .. autodoc2-docstring:: cookie_composer.diff.DIFF_DST_PREFIX
          :summary:

API
~~~

.. py:data:: DIFF_SRC_PREFIX
   :canonical: cookie_composer.diff.DIFF_SRC_PREFIX
   :value: 'upstream-template-old'

   .. autodoc2-docstring:: cookie_composer.diff.DIFF_SRC_PREFIX

.. py:data:: DIFF_DST_PREFIX
   :canonical: cookie_composer.diff.DIFF_DST_PREFIX
   :value: 'upstream-template-new'

   .. autodoc2-docstring:: cookie_composer.diff.DIFF_DST_PREFIX

.. py:function:: _git_diff_command(*args: str) -> typing.List[str]
   :canonical: cookie_composer.diff._git_diff_command

   .. autodoc2-docstring:: cookie_composer.diff._git_diff_command

.. py:function:: get_diff(repo0: pathlib.Path, repo1: pathlib.Path) -> str
   :canonical: cookie_composer.diff.get_diff

   .. autodoc2-docstring:: cookie_composer.diff.get_diff

.. py:function:: replace_diff_prefixes(diff: str, repo0_path: str, repo1_path: str) -> str
   :canonical: cookie_composer.diff.replace_diff_prefixes

   .. autodoc2-docstring:: cookie_composer.diff.replace_diff_prefixes

.. py:function:: display_diff(repo0: pathlib.Path, repo1: pathlib.Path) -> None
   :canonical: cookie_composer.diff.display_diff

   .. autodoc2-docstring:: cookie_composer.diff.display_diff
