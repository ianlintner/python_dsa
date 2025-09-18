"""
Longest Common Prefix

Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string.
"""

import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

random.seed(0)


class Solution:
    def solve(self, strs: list[str]) -> str:
        """Find the longest common prefix among the given list of strings."""
        if not strs:
            return ""
        prefix = strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix


def demo():
    """Demonstration of Longest Common Prefix problem."""
    strs = ["flower", "flow", "flight"]
    solver = Solution()
    result = solver.solve(strs)
    print(f"Input strings: {strs}")
    print(f"Longest common prefix: {result}")
    return f"Input: {strs}\nLongest Common Prefix: {result}"


register_problem(
    id=14,
    slug="longest_common_prefix",
    title="Longest Common Prefix",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["string"],
    url="https://leetcode.com/problems/longest-common-prefix/",
    notes="Iteratively shrink the prefix until valid for all strings.",
)
