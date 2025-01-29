"""Sphinx configuration file."""
# pylint: disable=invalid-name

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import sys
from typing import List

os.environ["SPHINX"] = "1"

if os.path.exists('/app'):
  sys.path.insert(0, os.path.abspath('/app'))
if os.path.exists('../../text_lint'):
  sys.path.insert(0, os.path.abspath('../..'))
  sys.path.insert(0, os.path.abspath('../../text_lint'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'text_lint'
copyright = '2025, Niall Byrne'  # pylint: disable=redefined-builtin
author = 'Niall Byrne'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path: List[str] = ['_templates']
exclude_patterns: List[str] = []


def autosummary_filter() -> List[str]:
  """Create a list of import paths to exclude from documentation.

  :returns: A list of paths to exclude from documentation.
  """
  exclude_paths: List[str] = []
  project_dir = os.path.join("..", "..", project)
  for root, dirs, filenames in os.walk(project_dir):
    root_path = pathlib.Path(root).relative_to(os.path.join("..", ".."))

    for name in set(dirs).intersection(autosummary_filter_folders):
      exclude_path = root_path / name
      exclude_paths.append('.'.join(exclude_path.with_suffix('').parts))

    for filename in set(filenames).intersection(autosummary_filter_filenames):
      exclude_path = root_path / os.path.splitext(filename)[0]
      exclude_paths.append('.'.join(exclude_path.with_suffix('').parts))

  return exclude_paths


# autodoc config
autodoc_typehints = "both"
autodoc_typehints_format = "short"
autodoc_inherit_docstrings = True
autodoc_typehints_description_target = "documented_params"

# autosummary config
autosummary_filter_folders = {"__pycache__", "tests"}
autosummary_filter_filenames = {"conftest.py"}
autosummary_generate = True
autosummary_ignore_module_all = True
autosummary_mock_imports = autosummary_filter()

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'css/theme_overrides.css',
]
