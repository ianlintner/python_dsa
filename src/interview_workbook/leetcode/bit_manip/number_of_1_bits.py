"""
Number Of 1 Bits

TODO: Add problem description
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, n: int) -> int:
        """Return the number of 1 bits in the binary representation of n."""
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count


def demo() -> str:
    """Run a deterministic demo for Number Of 1 Bits."""
    random.seed(0)
    sol = Solution()
    test_values = [0, 1, 2, 3, 7, 8, 15, 16, 31]
    print(f"Test values: {test_values}")
    results = {val: sol.solve(val) for val in test_values}
    print(f"Final results: {results}")
    return str(results)


register_problem(
    id=191,
    slug="number_of_1_bits",
    title="Number of 1 Bits",
    category=Category.BIT_MANIP,
    difficulty=Difficulty.EASY,
    tags=["divide_conquer", "bit_manipulation"],
    url="https://leetcode.com/problems/number-of-1-bits/",
    notes="",
)
