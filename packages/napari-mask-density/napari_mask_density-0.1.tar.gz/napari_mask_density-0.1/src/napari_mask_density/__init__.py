try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._widget import MaskAnalyzer

__all__ = ("__version__", "MaskAnalyzer")
