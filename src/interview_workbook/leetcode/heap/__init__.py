"""
Heap/Priority Queue Category

This module contains LeetCode problems that utilize heap and priority queue data structures.
Heaps are specialized tree-based data structures that satisfy the heap property,
making them ideal for efficiently maintaining ordered collections and finding extrema.

Key concepts covered:
- Min-heap and max-heap operations
- Priority queue implementations
- K-th largest/smallest element problems
- Stream processing with dynamic ordering
- Task scheduling and optimization problems
- Two-heap technique for median finding

Common patterns:
- Using heapq module for efficient heap operations
- Maintaining running medians with dual heaps
- Priority-based scheduling and resource allocation
- Top-K problems with heap-based selection
"""

from .._types import Category

CATEGORY_INFO = {
    "name": "Heap/Priority Queue",
    "description": "Problems utilizing heap and priority queue data structures",
    "key_concepts": [
        "Min-heap and max-heap operations",
        "Priority queue implementations",
        "K-th largest/smallest element problems",
        "Stream processing with dynamic ordering",
        "Task scheduling and optimization",
        "Two-heap technique for median finding",
    ],
    "common_patterns": [
        "Using heapq module for efficient heap operations",
        "Maintaining running medians with dual heaps",
        "Priority-based scheduling and resource allocation",
        "Top-K problems with heap-based selection",
    ],
}

__all__ = ["CATEGORY_INFO", "Category"]
