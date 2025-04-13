"""
Manifold - A Python package for building & running AI app node
"""

try:
    from importlib.metadata import version as get_version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version as get_version, PackageNotFoundError  # for Python <3.8

try:
    __version__ = get_version("manifold")
except PackageNotFoundError:
    __version__ = "unknown"

version = __version__

from .hub.main import Manifold
from .node.main import ManifoldNode

__all__ = ["Manifold", "ManifoldNode", "version"]