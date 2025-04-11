# __init__.py

# Metadata
__version__ = '0.1.0'
__author__ = 'Drestanto Muhammad Dyasputro'
__author_email__ = 'dyas@live.com'
__license__ = 'MIT'

# Importing the necessary classes from the fractal_forest module
from .node import Node
from .tree import Tree

# You can also include any helper functions or variables that are meant to be part of the public API
__all__ = ["Node", "Tree"]
