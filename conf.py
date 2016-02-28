import sys
import os
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'FeedPipe'
copyright = u'2016, Arthur Axel fREW Schmidt'
author = u'Arthur Axel fREW Schmidt'
version = u'0.0.1'
release = u'0.0.1'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
html_static_path = []
html_sidebars = {}
htmlhelp_basename = 'FeedPipedoc'
