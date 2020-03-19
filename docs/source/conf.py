project = 'Junction'
copyright = '2019, Junction Developers'
author = 'Junction Developers'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['recommonmark']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The suffix of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Recommonmark/Markdown stuff ---------------------------------------------
# NOTE: This entire section should be removed once the old/ folder is removed
#       from the docs/ directory.

from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify


def setup(app):
    app.add_config_value('recommonmark_config', {
        'enable_auto_toc_tree': True,
    }, True)
    app.add_transform(AutoStructify)
