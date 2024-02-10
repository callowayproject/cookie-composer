:py:mod:`cookie_composer.merge_files.ini_file`
==============================================

.. py:module:: cookie_composer.merge_files.ini_file

.. autodoc2-docstring:: cookie_composer.merge_files.ini_file
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`merge_ini_files <cookie_composer.merge_files.ini_file.merge_ini_files>`
     - .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.merge_ini_files
          :summary:
   * - :py:obj:`config_to_dict <cookie_composer.merge_files.ini_file.config_to_dict>`
     - .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.config_to_dict
          :summary:
   * - :py:obj:`dict_to_config <cookie_composer.merge_files.ini_file.dict_to_config>`
     - .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.dict_to_config
          :summary:

API
~~~

.. py:function:: merge_ini_files(new_file: pathlib.Path, existing_file: pathlib.Path, merge_strategy: str) -> None
   :canonical: cookie_composer.merge_files.ini_file.merge_ini_files

   .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.merge_ini_files

.. py:function:: config_to_dict(config: configparser.ConfigParser) -> dict
   :canonical: cookie_composer.merge_files.ini_file.config_to_dict

   .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.config_to_dict

.. py:function:: dict_to_config(dictionary: dict) -> configparser.ConfigParser
   :canonical: cookie_composer.merge_files.ini_file.dict_to_config

   .. autodoc2-docstring:: cookie_composer.merge_files.ini_file.dict_to_config
