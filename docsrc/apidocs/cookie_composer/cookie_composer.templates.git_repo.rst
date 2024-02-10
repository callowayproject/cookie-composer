:py:mod:`cookie_composer.templates.git_repo`
============================================

.. py:module:: cookie_composer.templates.git_repo

.. autodoc2-docstring:: cookie_composer.templates.git_repo
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_repo_name <cookie_composer.templates.git_repo.get_repo_name>`
     - .. autodoc2-docstring:: cookie_composer.templates.git_repo.get_repo_name
          :summary:
   * - :py:obj:`template_repo_from_git <cookie_composer.templates.git_repo.template_repo_from_git>`
     - .. autodoc2-docstring:: cookie_composer.templates.git_repo.template_repo_from_git
          :summary:
   * - :py:obj:`get_cached_remote <cookie_composer.templates.git_repo.get_cached_remote>`
     - .. autodoc2-docstring:: cookie_composer.templates.git_repo.get_cached_remote
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.templates.git_repo.logger>`
     - .. autodoc2-docstring:: cookie_composer.templates.git_repo.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.templates.git_repo.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.templates.git_repo.logger

.. py:function:: get_repo_name(repo_url: str, checkout: typing.Optional[str] = None) -> str
   :canonical: cookie_composer.templates.git_repo.get_repo_name

   .. autodoc2-docstring:: cookie_composer.templates.git_repo.get_repo_name

.. py:function:: template_repo_from_git(git_uri: str, locality: cookie_composer.templates.types.Locality, cache_dir: pathlib.Path, checkout: typing.Optional[str] = None) -> cookie_composer.templates.types.TemplateRepo
   :canonical: cookie_composer.templates.git_repo.template_repo_from_git

   .. autodoc2-docstring:: cookie_composer.templates.git_repo.template_repo_from_git

.. py:function:: get_cached_remote(git_uri: str, cache_dir: pathlib.Path, checkout: typing.Optional[str] = None) -> git.Repo
   :canonical: cookie_composer.templates.git_repo.get_cached_remote

   .. autodoc2-docstring:: cookie_composer.templates.git_repo.get_cached_remote
