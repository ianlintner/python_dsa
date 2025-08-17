"""
Unified package namespace for the Interview Workbook.

This package consolidates algorithms, data structures, graphs, dynamic programming,
string algorithms, common patterns, math utilities, systems topics, utilities, and concurrency
under a single top-level namespace: `interview_workbook`.

After migration, imports should use:
    from interview_workbook.algorithms.sorting.merge_sort import merge_sort
"""

__all__ = [
    "algorithms",
    "data_structures",
    "graphs",
    "strings",
    "dp",
    "patterns",
    "math_utils",
    "systems",
    "utils",
    "concurrency",
    "ml",
    "nlp",
]
