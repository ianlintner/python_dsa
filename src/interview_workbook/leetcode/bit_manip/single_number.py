"""
Single Number

TODO: Add problem description
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, nums: list[int]) -> int:
        """Return the element that appears only once in the array where every other element appears twice."""
        result = 0
        for num in nums:
            result ^= num
        return result


def demo() -> str:
    """Run a deterministic demo for Single Number."""
    random.seed(0)
    sol = Solution()
    test_values = [
        [2, 2, 1],
        [4, 1, 2, 1, 2],
        [1],
    ]
    print(f"Test values: {test_values}")
    results = {str(lst): sol.solve(lst) for lst in test_values}
    print(f"Final results: {results}")
    return str(results)


register_problem(
    id=136,
    slug="single_number",
    title="Single Number",
    category=Category.BIT_MANIP,
    difficulty=Difficulty.EASY,
    tags=["array", "bit_manipulation"],
    url="https://leetcode.com/problems/single-number/",
    notes="",
)
