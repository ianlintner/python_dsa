"""
Longest Substring Without Repeating

Problem: Longest Substring Without Repeating Characters
LeetCode link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
Description: Given a string, find the length of the longest substring without repeating characters.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return length of longest substring without repeating characters."""
        (s,) = args
        seen = {}
        l = 0
        res = 0
        for r, ch in enumerate(s):
            if ch in seen and seen[ch] >= l:
                l = seen[ch] + 1
            seen[ch] = r
            res = max(res, r - l + 1)
        return res


def demo():
    """Run a simple demonstration for Longest Substring Without Repeating Characters problem."""
    s = Solution()
    text = "abcabcbb"
    result = s.solve(text)
    print(f"Input: '{text}' -> Output: {result}")
    return f"'{text}' -> {result}"


register_problem(
    id=3,
    slug="longest_substring_without_repeating",
    title="Longest Substring Without Repeating Characters",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "sliding_window", "hashmap"],
    url="https://leetcode.com/problems/longest-substring-without-repeating-characters/",
    notes="",
)
