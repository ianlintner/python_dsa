"""
Type definitions for LeetCode problem metadata and categorization.
"""

from enum import Enum
from typing import TypedDict


class Difficulty(Enum):
    """Problem difficulty levels."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Category(Enum):
    """Problem categories based on algorithmic patterns."""
    ARRAYS_HASHING = "arrays_hashing"
    TWO_POINTERS = "two_pointers"
    SLIDING_WINDOW = "sliding_window"
    STACK = "stack"
    BINARY_SEARCH = "binary_search"
    LINKED_LIST = "linked_list"
    TREES = "trees"
    TRIES = "tries"
    HEAP = "heap"
    BACKTRACKING = "backtracking"
    GRAPHS = "graphs"
    INTERVALS = "intervals"
    GREEDY = "greedy"
    DP_1D = "dp_1d"
    DP_2D = "dp_2d"
    BIT_MANIP = "bit_manip"
    MATH_GEOMETRY = "math_geometry"


class ProblemMeta(TypedDict):
    """Metadata for a LeetCode problem."""
    id: int | None  # LeetCode problem ID when applicable
    slug: str  # Filesystem-safe identifier (e.g., "two_sum")
    title: str  # Human-readable title (e.g., "Two Sum")
    category: Category  # Problem category
    difficulty: Difficulty  # Problem difficulty
    tags: list[str]  # List of algorithmic pattern tags
    module: str  # Full dotted path to module
    url: str | None  # LeetCode problem URL if available
    notes: str | None  # Optional description or notes


# Common tags used across problems for additional categorization
COMMON_TAGS = {
    "hashmap", "array", "string", "two_pointers", "sliding_window",
    "binary_search", "sorting", "stack", "queue", "heap", "priority_queue",
    "linked_list", "tree", "binary_tree", "bst", "trie", "graph", "dfs", "bfs",
    "union_find", "topological_sort", "backtracking", "dynamic_programming",
    "greedy", "divide_conquer", "math", "bit_manipulation", "simulation",
    "prefix_sum", "monotonic_stack", "intervals", "design"
}
