"""
Problem: Counting Bits
LeetCode link: https://leetcode.com/problems/counting-bits/
Description: Given an integer n, return an array ans of length n + 1 such that ans[i] is
the number of 1's in the binary representation of i, for each i from 0 to n.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, n: int) -> list[int]:
        """Return array where ith element is number of set bits in i's binary representation."""
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp


def demo():
    """Demo for Counting Bits problem."""
    import random

    random.seed(0)
    n = 5
    result = Solution().solve(n)
    return f"Counting bits up to {n}: {result}"


register_problem(
    id=338,
    slug="counting_bits",
    title="Counting Bits",
    category=Category.BIT_MANIP,
    difficulty=Difficulty.MEDIUM,
    tags=["bit manipulation", "dp"],
    url="https://leetcode.com/problems/counting-bits/",
    notes="Standard bit manipulation + DP trick",
)
