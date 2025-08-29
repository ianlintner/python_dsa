"""
Backtracking Category

This module contains LeetCode problems that utilize backtracking algorithms.
Backtracking is a systematic method for solving constraint satisfaction problems
by incrementally building candidates to the solutions and abandoning candidates
that cannot lead to a valid solution.

Key concepts covered:
    - Recursive exploration of solution space
- Pruning invalid branches early (backtrack)
- Generate all possible combinations, permutations, subsets
- Constraint satisfaction problems
- Decision tree exploration with rollback
- State space search with undoing changes

Common patterns=- Choose, explore, unchoose (backtrack)
- Building solutions incrementally
- Using recursion with base cases
- Tracking visited states and undoing changes
- Early termination when constraints violated
"""

from .._types import Category

CATEGORY_INFO = {
    "name": "Backtracking",
    "description": "Problems utilizing backtracking algorithms for systematic solution space exploration",
    "key_concepts": [
        "Recursive exploration of solution space",
        "Pruning invalid branches early (backtrack)",
        "Generate all possible combinations, permutations, subsets",
        "Constraint satisfaction problems",
        "Decision tree exploration with rollback",
        "State space search with undoing changes",
    ],
    "common_patterns": [
        "Choose, explore, unchoose (backtrack)",
        "Building solutions incrementally",
        "Using recursion with base cases",
        "Tracking visited states and undoing changes",
        "Early termination when constraints violated",
    ],
}

__all__ = ["CATEGORY_INFO", "Category"]
