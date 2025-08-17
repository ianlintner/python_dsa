"""
Sorting algorithms (lightweight top-level namespace).

Provides lazy accessors for submodules to avoid circular import issues.
"""

from importlib import import_module
from typing import Any

__all__ = [
    "bubble_sort",
    "insertion_sort",
    "non_comparison_sorts",
    "selection_sort",
]


def __getattr__(name: str) -> Any:
    """
    Lazily import and expose sorting submodules as attributes:
      - bubble_sort
      - insertion_sort
      - selection_sort
      - non_comparison_sorts
    """
    if name in __all__:
        import sys

        canonical = f"interview_workbook.algorithms.sorting.{name}"
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
