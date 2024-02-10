:py:mod:`cookie_composer.templates.types`
=========================================

.. py:module:: cookie_composer.templates.types

.. autodoc2-docstring:: cookie_composer.templates.types
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Locality <cookie_composer.templates.types.Locality>`
     - .. autodoc2-docstring:: cookie_composer.templates.types.Locality
          :summary:
   * - :py:obj:`TemplateFormat <cookie_composer.templates.types.TemplateFormat>`
     - .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat
          :summary:
   * - :py:obj:`TemplateRepo <cookie_composer.templates.types.TemplateRepo>`
     - .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo
          :summary:
   * - :py:obj:`Template <cookie_composer.templates.types.Template>`
     - .. autodoc2-docstring:: cookie_composer.templates.types.Template
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`get_template_name <cookie_composer.templates.types.get_template_name>`
     - .. autodoc2-docstring:: cookie_composer.templates.types.get_template_name
          :summary:

API
~~~

.. py:class:: Locality()
   :canonical: cookie_composer.templates.types.Locality

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`

   .. autodoc2-docstring:: cookie_composer.templates.types.Locality

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.templates.types.Locality.__init__

   .. py:attribute:: LOCAL
      :canonical: cookie_composer.templates.types.Locality.LOCAL
      :value: 'local'

      .. autodoc2-docstring:: cookie_composer.templates.types.Locality.LOCAL

   .. py:attribute:: REMOTE
      :canonical: cookie_composer.templates.types.Locality.REMOTE
      :value: 'remote'

      .. autodoc2-docstring:: cookie_composer.templates.types.Locality.REMOTE

.. py:class:: TemplateFormat()
   :canonical: cookie_composer.templates.types.TemplateFormat

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`

   .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat

   .. rubric:: Initialization

   .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat.__init__

   .. py:attribute:: ZIP
      :canonical: cookie_composer.templates.types.TemplateFormat.ZIP
      :value: 'zip'

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat.ZIP

   .. py:attribute:: GIT
      :canonical: cookie_composer.templates.types.TemplateFormat.GIT
      :value: 'git'

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat.GIT

   .. py:attribute:: HG
      :canonical: cookie_composer.templates.types.TemplateFormat.HG
      :value: 'hg'

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat.HG

   .. py:attribute:: PLAIN
      :canonical: cookie_composer.templates.types.TemplateFormat.PLAIN
      :value: 'plain'

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateFormat.PLAIN

.. py:class:: TemplateRepo
   :canonical: cookie_composer.templates.types.TemplateRepo

   .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo

   .. py:attribute:: source
      :canonical: cookie_composer.templates.types.TemplateRepo.source
      :type: str
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.source

   .. py:attribute:: cached_source
      :canonical: cookie_composer.templates.types.TemplateRepo.cached_source
      :type: pathlib.Path
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.cached_source

   .. py:attribute:: format
      :canonical: cookie_composer.templates.types.TemplateRepo.format
      :type: cookie_composer.templates.types.TemplateFormat
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.format

   .. py:attribute:: locality
      :canonical: cookie_composer.templates.types.TemplateRepo.locality
      :type: cookie_composer.templates.types.Locality
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.locality

   .. py:attribute:: checkout
      :canonical: cookie_composer.templates.types.TemplateRepo.checkout
      :type: typing.Optional[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.checkout

   .. py:attribute:: password
      :canonical: cookie_composer.templates.types.TemplateRepo.password
      :type: typing.Optional[str]
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.password

   .. py:property:: current_sha
      :canonical: cookie_composer.templates.types.TemplateRepo.current_sha
      :type: typing.Optional[str]

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.current_sha

   .. py:property:: latest_sha
      :canonical: cookie_composer.templates.types.TemplateRepo.latest_sha
      :type: typing.Optional[str]

      .. autodoc2-docstring:: cookie_composer.templates.types.TemplateRepo.latest_sha

.. py:class:: Template
   :canonical: cookie_composer.templates.types.Template

   .. autodoc2-docstring:: cookie_composer.templates.types.Template

   .. py:attribute:: repo
      :canonical: cookie_composer.templates.types.Template.repo
      :type: cookie_composer.templates.types.TemplateRepo
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.repo

   .. py:attribute:: directory
      :canonical: cookie_composer.templates.types.Template.directory
      :type: str
      :value: <Multiline-String>

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.directory

   .. py:attribute:: _context
      :canonical: cookie_composer.templates.types.Template._context
      :type: typing.Optional[dict]
      :value: None

      .. autodoc2-docstring:: cookie_composer.templates.types.Template._context

   .. py:method:: cleanup() -> None
      :canonical: cookie_composer.templates.types.Template.cleanup

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.cleanup

   .. py:property:: name
      :canonical: cookie_composer.templates.types.Template.name
      :type: str

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.name

   .. py:property:: cached_path
      :canonical: cookie_composer.templates.types.Template.cached_path
      :type: pathlib.Path

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.cached_path

   .. py:property:: context_file_path
      :canonical: cookie_composer.templates.types.Template.context_file_path
      :type: pathlib.Path

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.context_file_path

   .. py:property:: context
      :canonical: cookie_composer.templates.types.Template.context
      :type: dict

      .. autodoc2-docstring:: cookie_composer.templates.types.Template.context

.. py:function:: get_template_name(path_or_url: str, directory: typing.Optional[str] = None, checkout: typing.Optional[str] = None) -> str
   :canonical: cookie_composer.templates.types.get_template_name

   .. autodoc2-docstring:: cookie_composer.templates.types.get_template_name
