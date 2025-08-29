from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty

"""
Daily Temperatures

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> None:
        """TODO: Implement solution."""
        pass


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=739,
    slug="daily_temperatures",
    title="Daily Temperatures",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "monotonic stack"],
    url="https://leetcode.com/problems/daily-temperatures/",
    notes="Use a monotonic stack to track previous warmer days.",
)
