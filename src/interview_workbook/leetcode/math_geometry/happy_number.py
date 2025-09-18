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
    """Run a simple demonstration for Happy Number problem."""
    s = Solution()
    n1, n2 = 19, 2
    result1 = s.solve(n1)
    result2 = s.solve(n2)
    return f"{n1} -> {result1}; {n2} -> {result2}"


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
