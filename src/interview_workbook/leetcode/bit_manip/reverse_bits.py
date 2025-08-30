"""
Reverse Bits

TODO: Add problem description
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, n: int) -> int:
        """Return the integer obtained by reversing the 32-bit binary representation of n."""
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result


def demo() -> str:
    """Run a deterministic demo for Reverse Bits."""
    random.seed(0)
    sol = Solution()
    test_values = [0, 1, 43261596, 4294967293]
    results = {val: sol.solve(val) for val in test_values}
    return str(results)


register_problem(
    id=190,
    slug="reverse_bits",
    title="Reverse Bits",
    category=Category.BIT_MANIP,
    difficulty=Difficulty.EASY,
    tags=["divide_conquer", "bit_manipulation"],
    url="https://leetcode.com/problems/reverse-bits/",
    notes="",
)
