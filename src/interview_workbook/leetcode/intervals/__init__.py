"""
Intervals Category - LeetCode Problems

This category focuses on problems involving intervals, including:
    - Merging overlapping intervals
- Inserting intervals while maintaining sorted order
- Finding non-overlapping intervals
- Scheduling problems (meeting rooms)
- Optimizing interval arrangements

Key concepts:
    - Sorting intervals by start/end times
- Merging overlapping regions
- Greedy algorithms for interval optimization
- Event-based processing
- Sweep line algorithms

Common patterns:
    - Sort intervals by start time
- Iterate and merge overlapping intervals
- Use priority queues for dynamic scheduling
- Two-pointer techniques for optimization
"""

from .._types import Category

# Category information for discovery and documentation
CATEGORY_INFO = {
    "name": "Intervals",
    "description": "Problems involving interval manipulation, merging, and scheduling",
    "key_concepts": [
        "Interval merging and overlapping",
        "Sorting by start/end times",
        "Greedy scheduling algorithms",
        "Event processing and sweep line",
        "Meeting room scheduling patterns",
    ],
    "common_patterns": [
        "Sort intervals then merge overlapping",
        "Use priority queue for dynamic scheduling",
        "Transform intervals to events for processing",
        "Greedy selection for optimization problems",
    ],
    "category": Category.INTERVALS,
}
