# Configuration file for Sphinx documentation

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Voxel Centroid'
copyright = '2026, SkyGliderus'
author = 'SkyGliderus'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

master_doc = 'index'