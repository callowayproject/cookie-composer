:py:mod:`cookie_composer.authentication`
========================================

.. py:module:: cookie_composer.authentication

.. autodoc2-docstring:: cookie_composer.authentication
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_hosts_file <cookie_composer.authentication.get_hosts_file>`
     - .. autodoc2-docstring:: cookie_composer.authentication.get_hosts_file
          :summary:
   * - :py:obj:`login_to_svc <cookie_composer.authentication.login_to_svc>`
     - .. autodoc2-docstring:: cookie_composer.authentication.login_to_svc
          :summary:
   * - :py:obj:`get_cached_token <cookie_composer.authentication.get_cached_token>`
     - .. autodoc2-docstring:: cookie_composer.authentication.get_cached_token
          :summary:
   * - :py:obj:`add_auth_to_url <cookie_composer.authentication.add_auth_to_url>`
     - .. autodoc2-docstring:: cookie_composer.authentication.add_auth_to_url
          :summary:
   * - :py:obj:`github_auth_device <cookie_composer.authentication.github_auth_device>`
     - .. autodoc2-docstring:: cookie_composer.authentication.github_auth_device
          :summary:

API
~~~

.. py:function:: get_hosts_file() -> pathlib.Path
   :canonical: cookie_composer.authentication.get_hosts_file

   .. autodoc2-docstring:: cookie_composer.authentication.get_hosts_file

.. py:function:: login_to_svc(service: typing.Optional[str] = None, protocol: typing.Optional[str] = None, scopes: typing.Optional[str] = None, token: typing.Optional[str] = None) -> str
   :canonical: cookie_composer.authentication.login_to_svc

   .. autodoc2-docstring:: cookie_composer.authentication.login_to_svc

.. py:function:: get_cached_token(account_name: str) -> typing.Optional[str]
   :canonical: cookie_composer.authentication.get_cached_token

   .. autodoc2-docstring:: cookie_composer.authentication.get_cached_token

.. py:function:: add_auth_to_url(url: str) -> str
   :canonical: cookie_composer.authentication.add_auth_to_url

   .. autodoc2-docstring:: cookie_composer.authentication.add_auth_to_url

.. py:function:: github_auth_device(n_polls: int = 9999) -> typing.Optional[str]
   :canonical: cookie_composer.authentication.github_auth_device

   .. autodoc2-docstring:: cookie_composer.authentication.github_auth_device
