:py:mod:`cookie_composer.commands.authn`
========================================

.. py:module:: cookie_composer.commands.authn

.. autodoc2-docstring:: cookie_composer.commands.authn
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`auth <cookie_composer.commands.authn.auth>`
     - .. autodoc2-docstring:: cookie_composer.commands.authn.auth
          :summary:
   * - :py:obj:`login <cookie_composer.commands.authn.login>`
     - .. autodoc2-docstring:: cookie_composer.commands.authn.login
          :summary:
   * - :py:obj:`token <cookie_composer.commands.authn.token>`
     - .. autodoc2-docstring:: cookie_composer.commands.authn.token
          :summary:

API
~~~

.. py:function:: auth() -> None
   :canonical: cookie_composer.commands.authn.auth

   .. autodoc2-docstring:: cookie_composer.commands.authn.auth

.. py:function:: login(git_protocol: str, service: str, scopes: str, with_token: rich_click.File) -> None
   :canonical: cookie_composer.commands.authn.login

   .. autodoc2-docstring:: cookie_composer.commands.authn.login

.. py:function:: token(service: str) -> None
   :canonical: cookie_composer.commands.authn.token

   .. autodoc2-docstring:: cookie_composer.commands.authn.token
