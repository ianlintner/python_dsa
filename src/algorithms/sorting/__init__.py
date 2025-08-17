"""
Sorting algorithms (lightweight top-level namespace).

Modules:
- bubble_sort
- insertion_sort
- selection_sort
- non_comparison_sorts
"""

from . import bubble_sort, insertion_sort, non_comparison_sorts, selection_sort

__all__ = [
    "bubble_sort",
    "insertion_sort",
    "non_comparison_sorts",
    "selection_sort",
]
