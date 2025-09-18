"""
Climbing Stairs

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Return the number of distinct ways to climb n stairs (1 or 2 steps at a time)."""
        if not args:
            return 0
        n = args[0]
        if n <= 2:
            return n
        prev, curr = 1, 2
        for _ in range(3, n + 1):
            prev, curr = curr, prev + curr
        return curr


def demo():
    """Run a demo for the Climbing Stairs problem."""
    solver = Solution()
    n = 5
    result = solver.solve(n)
    print(f"Number of stairs: {n}")
    print(f"Final result: {result}")
    return str(result)


register_problem(
    id=70,
    slug="climbing_stairs",
    title="Climbing Stairs",
    category=Category.DP_1D,
    difficulty=Difficulty.EASY,
    tags=["math", "dynamic_programming"],
    url="https://leetcode.com/problems/climbing-stairs/",
    notes="",
)
