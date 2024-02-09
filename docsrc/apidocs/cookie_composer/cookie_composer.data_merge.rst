:py:mod:`cookie_composer.data_merge`
====================================

.. py:module:: cookie_composer.data_merge

.. autodoc2-docstring:: cookie_composer.data_merge
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Context <cookie_composer.data_merge.Context>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.Context
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`deep_merge <cookie_composer.data_merge.deep_merge>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.deep_merge
          :summary:
   * - :py:obj:`merge_iterables <cookie_composer.data_merge.merge_iterables>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.merge_iterables
          :summary:
   * - :py:obj:`comprehensive_merge <cookie_composer.data_merge.comprehensive_merge>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.comprehensive_merge
          :summary:
   * - :py:obj:`freeze_data <cookie_composer.data_merge.freeze_data>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.freeze_data
          :summary:
   * - :py:obj:`get_merge_strategy <cookie_composer.data_merge.get_merge_strategy>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.get_merge_strategy
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <cookie_composer.data_merge.logger>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.logger
          :summary:
   * - :py:obj:`DO_NOT_MERGE <cookie_composer.data_merge.DO_NOT_MERGE>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.DO_NOT_MERGE
          :summary:
   * - :py:obj:`NESTED_OVERWRITE <cookie_composer.data_merge.NESTED_OVERWRITE>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.NESTED_OVERWRITE
          :summary:
   * - :py:obj:`OVERWRITE <cookie_composer.data_merge.OVERWRITE>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.OVERWRITE
          :summary:
   * - :py:obj:`COMPREHENSIVE <cookie_composer.data_merge.COMPREHENSIVE>`
     - .. autodoc2-docstring:: cookie_composer.data_merge.COMPREHENSIVE
          :summary:

API
~~~

.. py:data:: logger
   :canonical: cookie_composer.data_merge.logger
   :value: None

   .. autodoc2-docstring:: cookie_composer.data_merge.logger

.. py:function:: deep_merge(*dicts: dict) -> dict
   :canonical: cookie_composer.data_merge.deep_merge

   .. autodoc2-docstring:: cookie_composer.data_merge.deep_merge

.. py:function:: merge_iterables(iter1: typing.Iterable, iter2: typing.Iterable) -> set
   :canonical: cookie_composer.data_merge.merge_iterables

   .. autodoc2-docstring:: cookie_composer.data_merge.merge_iterables

.. py:function:: comprehensive_merge(*args: typing.MutableMapping) -> typing.Any
   :canonical: cookie_composer.data_merge.comprehensive_merge

   .. autodoc2-docstring:: cookie_composer.data_merge.comprehensive_merge

.. py:class:: Context(*maps)
   :canonical: cookie_composer.data_merge.Context

   Bases: :py:obj:`collections.ChainMap`

   .. autodoc2-docstring:: cookie_composer.data_merge.Context

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.data_merge.Context.__init__

   .. py:property:: is_empty
      :canonical: cookie_composer.data_merge.Context.is_empty
      :type: bool

      .. autodoc2-docstring:: cookie_composer.data_merge.Context.is_empty

   .. py:method:: flatten() -> typing.MutableMapping
      :canonical: cookie_composer.data_merge.Context.flatten

      .. autodoc2-docstring:: cookie_composer.data_merge.Context.flatten

.. py:function:: freeze_data(obj: typing.Any) -> typing.Any
   :canonical: cookie_composer.data_merge.freeze_data

   .. autodoc2-docstring:: cookie_composer.data_merge.freeze_data

.. py:data:: DO_NOT_MERGE
   :canonical: cookie_composer.data_merge.DO_NOT_MERGE
   :value: 'do-not-merge'

   .. autodoc2-docstring:: cookie_composer.data_merge.DO_NOT_MERGE

.. py:data:: NESTED_OVERWRITE
   :canonical: cookie_composer.data_merge.NESTED_OVERWRITE
   :value: 'nested-overwrite'

   .. autodoc2-docstring:: cookie_composer.data_merge.NESTED_OVERWRITE

.. py:data:: OVERWRITE
   :canonical: cookie_composer.data_merge.OVERWRITE
   :value: 'overwrite'

   .. autodoc2-docstring:: cookie_composer.data_merge.OVERWRITE

.. py:data:: COMPREHENSIVE
   :canonical: cookie_composer.data_merge.COMPREHENSIVE
   :value: 'comprehensive'

   .. autodoc2-docstring:: cookie_composer.data_merge.COMPREHENSIVE

.. py:function:: get_merge_strategy(path: pathlib.Path, merge_strategies: typing.Dict[str, str]) -> str
   :canonical: cookie_composer.data_merge.get_merge_strategy

   .. autodoc2-docstring:: cookie_composer.data_merge.get_merge_strategy
