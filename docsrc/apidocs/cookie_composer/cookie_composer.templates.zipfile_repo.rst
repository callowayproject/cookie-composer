:py:mod:`cookie_composer.templates.zipfile_repo`
================================================

.. py:module:: cookie_composer.templates.zipfile_repo

.. autodoc2-docstring:: cookie_composer.templates.zipfile_repo
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`template_repo_from_zipfile <cookie_composer.templates.zipfile_repo.template_repo_from_zipfile>`
     - .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.template_repo_from_zipfile
          :summary:
   * - :py:obj:`download_zipfile <cookie_composer.templates.zipfile_repo.download_zipfile>`
     - .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.download_zipfile
          :summary:
   * - :py:obj:`unzip <cookie_composer.templates.zipfile_repo.unzip>`
     - .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.unzip
          :summary:
   * - :py:obj:`validate_zipfile <cookie_composer.templates.zipfile_repo.validate_zipfile>`
     - .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.validate_zipfile
          :summary:
   * - :py:obj:`extract_zipfile <cookie_composer.templates.zipfile_repo.extract_zipfile>`
     - .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.extract_zipfile
          :summary:

API
~~~

.. py:function:: template_repo_from_zipfile(zip_uri: str, locality: cookie_composer.templates.types.Locality, cache_dir: pathlib.Path, no_input: bool = False, password: typing.Optional[str] = None) -> cookie_composer.templates.types.TemplateRepo
   :canonical: cookie_composer.templates.zipfile_repo.template_repo_from_zipfile

   .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.template_repo_from_zipfile

.. py:function:: download_zipfile(url: str, cache_dir: pathlib.Path, no_input: bool = False) -> pathlib.Path
   :canonical: cookie_composer.templates.zipfile_repo.download_zipfile

   .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.download_zipfile

.. py:function:: unzip(zip_uri: str, is_remote: bool, cache_dir: pathlib.Path, no_input: bool = False, password: typing.Optional[str] = None) -> pathlib.Path
   :canonical: cookie_composer.templates.zipfile_repo.unzip

   .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.unzip

.. py:function:: validate_zipfile(zip_path: pathlib.Path, zip_uri: str) -> None
   :canonical: cookie_composer.templates.zipfile_repo.validate_zipfile

   .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.validate_zipfile

.. py:function:: extract_zipfile(zip_path: pathlib.Path, no_input: bool, password: typing.Optional[str] = None) -> pathlib.Path
   :canonical: cookie_composer.templates.zipfile_repo.extract_zipfile

   .. autodoc2-docstring:: cookie_composer.templates.zipfile_repo.extract_zipfile
