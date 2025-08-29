"""
Car Fleet

TODO: Add problem description
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> None:
        """TODO: Implement solution."""
        pass


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
register_problem(
    slug="car_fleet",
    title="Car Fleet",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack"],
    url="https://leetcode.com/problems/car-fleet/",
    notes="Greedy with sorting and stack",
)
