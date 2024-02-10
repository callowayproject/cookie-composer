:py:mod:`cookie_composer.templates.source`
==========================================

.. py:module:: cookie_composer.templates.source

.. autodoc2-docstring:: cookie_composer.templates.source
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`identify_repo <cookie_composer.templates.source.identify_repo>`
     - .. autodoc2-docstring:: cookie_composer.templates.source.identify_repo
          :summary:
   * - :py:obj:`get_template_repo <cookie_composer.templates.source.get_template_repo>`
     - .. autodoc2-docstring:: cookie_composer.templates.source.get_template_repo
          :summary:
   * - :py:obj:`resolve_local_path <cookie_composer.templates.source.resolve_local_path>`
     - .. autodoc2-docstring:: cookie_composer.templates.source.resolve_local_path
          :summary:

API
~~~

.. py:function:: identify_repo(url: str, local_path: typing.Optional[pathlib.Path] = None) -> typing.Tuple[cookie_composer.templates.types.TemplateFormat, cookie_composer.templates.types.Locality]
   :canonical: cookie_composer.templates.source.identify_repo

   .. autodoc2-docstring:: cookie_composer.templates.source.identify_repo

.. py:function:: get_template_repo(url: str, local_path: typing.Optional[pathlib.Path] = None, checkout: typing.Optional[str] = None, password: typing.Optional[str] = None) -> cookie_composer.templates.types.TemplateRepo
   :canonical: cookie_composer.templates.source.get_template_repo

   .. autodoc2-docstring:: cookie_composer.templates.source.get_template_repo

.. py:function:: resolve_local_path(url: str, local_path: typing.Optional[pathlib.Path] = None) -> pathlib.Path
   :canonical: cookie_composer.templates.source.resolve_local_path

   .. autodoc2-docstring:: cookie_composer.templates.source.resolve_local_path
