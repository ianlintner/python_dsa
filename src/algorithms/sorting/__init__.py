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
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
