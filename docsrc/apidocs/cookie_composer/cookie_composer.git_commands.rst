:py:mod:`cookie_composer.git_commands`
======================================

.. py:module:: cookie_composer.git_commands

.. autodoc2-docstring:: cookie_composer.git_commands
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`TempGitWorktreeDir <cookie_composer.git_commands.TempGitWorktreeDir>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.TempGitWorktreeDir
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_repo <cookie_composer.git_commands.get_repo>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.get_repo
          :summary:
   * - :py:obj:`clone <cookie_composer.git_commands.clone>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.clone
          :summary:
   * - :py:obj:`branch_exists <cookie_composer.git_commands.branch_exists>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.branch_exists
          :summary:
   * - :py:obj:`remote_branch_exists <cookie_composer.git_commands.remote_branch_exists>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.remote_branch_exists
          :summary:
   * - :py:obj:`checkout_ref <cookie_composer.git_commands.checkout_ref>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.checkout_ref
          :summary:
   * - :py:obj:`checkout_branch <cookie_composer.git_commands.checkout_branch>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.checkout_branch
          :summary:
   * - :py:obj:`apply_patch <cookie_composer.git_commands.apply_patch>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.apply_patch
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.git_commands.logger>`
     - .. autodoc2-docstring:: cookie_composer.git_commands.logger
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.git_commands.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.git_commands.logger

.. py:function:: get_repo(project_dir: typing.Union[str, pathlib.Path], search_parent_directories: bool = False, ensure_clean: bool = False) -> git.Repo
   :canonical: cookie_composer.git_commands.get_repo

   .. autodoc2-docstring:: cookie_composer.git_commands.get_repo

.. py:function:: clone(repo_url: str, dest_path: typing.Optional[pathlib.Path] = None) -> git.Repo
   :canonical: cookie_composer.git_commands.clone

   .. autodoc2-docstring:: cookie_composer.git_commands.clone

.. py:function:: branch_exists(repo: git.Repo, branch_name: str) -> bool
   :canonical: cookie_composer.git_commands.branch_exists

   .. autodoc2-docstring:: cookie_composer.git_commands.branch_exists

.. py:function:: remote_branch_exists(repo: git.Repo, branch_name: str, remote_name: str = 'origin') -> bool
   :canonical: cookie_composer.git_commands.remote_branch_exists

   .. autodoc2-docstring:: cookie_composer.git_commands.remote_branch_exists

.. py:function:: checkout_ref(repo: git.Repo, ref: str) -> None
   :canonical: cookie_composer.git_commands.checkout_ref

   .. autodoc2-docstring:: cookie_composer.git_commands.checkout_ref

.. py:function:: checkout_branch(repo: git.Repo, branch_name: str, remote_name: str = 'origin') -> None
   :canonical: cookie_composer.git_commands.checkout_branch

   .. autodoc2-docstring:: cookie_composer.git_commands.checkout_branch

.. py:function:: apply_patch(repo: git.Repo, diff: str) -> None
   :canonical: cookie_composer.git_commands.apply_patch

   .. autodoc2-docstring:: cookie_composer.git_commands.apply_patch

.. py:class:: TempGitWorktreeDir(worktree_path: pathlib.Path, repo_path: pathlib.Path, branch: str = 'master')
   :canonical: cookie_composer.git_commands.TempGitWorktreeDir

   .. autodoc2-docstring:: cookie_composer.git_commands.TempGitWorktreeDir

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.git_commands.TempGitWorktreeDir.__init__

   .. py:method:: __enter__()
      :canonical: cookie_composer.git_commands.TempGitWorktreeDir.__enter__

      .. autodoc2-docstring:: cookie_composer.git_commands.TempGitWorktreeDir.__enter__

   .. py:method:: __exit__(type, value, traceback)
      :canonical: cookie_composer.git_commands.TempGitWorktreeDir.__exit__

      .. autodoc2-docstring:: cookie_composer.git_commands.TempGitWorktreeDir.__exit__
