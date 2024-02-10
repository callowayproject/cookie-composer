:py:mod:`cookie_composer.exceptions`
====================================

.. py:module:: cookie_composer.exceptions

.. autodoc2-docstring:: cookie_composer.exceptions
   :allowtitles:

Module Contents
---------------

API
~~~

.. py:exception:: MissingCompositionFileError(path_or_url: str)
   :canonical: cookie_composer.exceptions.MissingCompositionFileError

   Bases: :py:obj:`Exception`

   .. autodoc2-docstring:: cookie_composer.exceptions.MissingCompositionFileError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.MissingCompositionFileError.__init__

.. py:exception:: MergeError(origin: typing.Optional[str] = None, destination: typing.Optional[str] = None, strategy: typing.Optional[str] = None, error_message: typing.Optional[str] = '')
   :canonical: cookie_composer.exceptions.MergeError

   Bases: :py:obj:`Exception`

   .. autodoc2-docstring:: cookie_composer.exceptions.MergeError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.MergeError.__init__

.. py:exception:: GitError()
   :canonical: cookie_composer.exceptions.GitError

   Bases: :py:obj:`Exception`

   .. autodoc2-docstring:: cookie_composer.exceptions.GitError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.GitError.__init__

.. py:exception:: ChangesetUnicodeError()
   :canonical: cookie_composer.exceptions.ChangesetUnicodeError

   Bases: :py:obj:`Exception`

   .. autodoc2-docstring:: cookie_composer.exceptions.ChangesetUnicodeError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.ChangesetUnicodeError.__init__

.. py:exception:: InvalidZipRepositoryError(message: str = '')
   :canonical: cookie_composer.exceptions.InvalidZipRepositoryError

   Bases: :py:obj:`Exception`

   .. autodoc2-docstring:: cookie_composer.exceptions.InvalidZipRepositoryError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.InvalidZipRepositoryError.__init__

.. py:exception:: EmptyZipRepositoryError(url: str)
   :canonical: cookie_composer.exceptions.EmptyZipRepositoryError

   Bases: :py:obj:`cookie_composer.exceptions.InvalidZipRepositoryError`

   .. autodoc2-docstring:: cookie_composer.exceptions.EmptyZipRepositoryError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.EmptyZipRepositoryError.__init__

.. py:exception:: NoZipDirectoryError(url: str)
   :canonical: cookie_composer.exceptions.NoZipDirectoryError

   Bases: :py:obj:`cookie_composer.exceptions.InvalidZipRepositoryError`

   .. autodoc2-docstring:: cookie_composer.exceptions.NoZipDirectoryError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.NoZipDirectoryError.__init__

.. py:exception:: InvalidZipPasswordError()
   :canonical: cookie_composer.exceptions.InvalidZipPasswordError

   Bases: :py:obj:`cookie_composer.exceptions.InvalidZipRepositoryError`

   .. autodoc2-docstring:: cookie_composer.exceptions.InvalidZipPasswordError

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.exceptions.InvalidZipPasswordError.__init__
