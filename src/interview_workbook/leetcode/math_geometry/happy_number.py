"""
Happy Number

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> bool:
        """Determine if a number is a happy number using cycle detection."""
        n = args[0]
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(d) ** 2 for d in str(n))
        return n == 1


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=202,
    slug="happy_number",
    title="Happy Number",
    category=Category.MATH_GEOMETRY,
    difficulty=Difficulty.EASY,
    tags=["hashmap", "math", "two_pointers"],
    url="https://leetcode.com/problems/happy-number/",
    notes="",
)
