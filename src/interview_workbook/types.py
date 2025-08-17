"""
Common type aliases shared across the interview_workbook package.

Notes and validation assumptions:
- Graph / WeightedGraph keys must be hashable; adjacency lists must contain only hashable nodes.
- Edge weights (int) are non-negative where algorithms assume Dijkstra; Bellman-Ford may accept
  negatives but not negative cycles unless explicitly stated.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Sequence

Graph = dict[Hashable, list[Hashable]]
WeightedGraph = dict[Hashable, list[tuple[Hashable, int]]]
Index = int
Pair = tuple[int, int]
# Python typing lacks a direct Comparable bound; rely on runtime comparisons.
Comparable = object

__all__ = [
    "Graph",
    "WeightedGraph",
    "Index",
    "Pair",
    "Comparable",
    "Hashable",
    "Sequence",
    "Iterable",
    "Callable",
]
