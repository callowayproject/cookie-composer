"""
Sphinx configuration.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(".."))

import cookie_composer  # NOQA: E402

project = "Cookie Composer"
author = "Corey Oordt"
copyright = f"{date.today():%Y}, {author}"

version = cookie_composer.__version__
release = cookie_composer.__version__

# -- General configuration ---------------------------------------------

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.viewcode",
    # "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx_click",
]
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2
autosummary_generate = True
autodoc2_packages = ["../cookie_composer"]
napoleon_attr_annotations = True
napoleon_include_special_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_init_with_doc = True
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False
primary_domain = "py"


# -- Options for HTML output -------------------------------------------

html_title = "Cookie Composer"
html_logo = "_static/img/composer-logo.svg"
html_theme = "sphinx_material"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "Cookie Composer",
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://callowayproject.github.io/cookie-composer/",
    # Set the color and the accent color
    "color_primary": "blue",
    "color_accent": "light-blue",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/callowayproject/cookie-composer/",
    "repo_name": "Project",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 3,
    # If False, expand all TOC entries
    "globaltoc_collapse": False,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
    "master_doc": True,
}
