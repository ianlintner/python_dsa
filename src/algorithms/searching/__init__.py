"""
Searching algorithms (lightweight top-level namespace).

Provides lazy accessors for submodules to avoid circular import issues.
"""

from importlib import import_module
from typing import Any

__all__ = [
    "advanced_search",
    "binary_search",
    "linear_search",
    "quickselect",
]


def __getattr__(name: str) -> Any:
    """
    Lazily import and expose searching submodules as attributes:
      - advanced_search
      - binary_search
      - linear_search
      - quickselect
    """
    if name in __all__:
        import sys

        canonical = f"interview_workbook.algorithms.searching.{name}"
        # If already imported under canonical path, reuse it to avoid reload/circulars
        if canonical in sys.modules:
            return sys.modules[canonical]
        # Try canonical import first
        try:
            return import_module(canonical)
        except ModuleNotFoundError:
            # Fallback to local under src/ if present
            local = f"{__name__}.{name}"
            return import_module(local)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
