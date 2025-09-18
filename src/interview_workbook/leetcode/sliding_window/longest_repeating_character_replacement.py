"""
Longest Repeating Character Replacement

TODO: Add problem description
"""

from collections import defaultdict

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return length of longest substring with at most k replacements."""
        s, k = args
        count = defaultdict(int)
        res = 0
        l = 0
        maxf = 0
        for r, ch in enumerate(s):
            count[ch] += 1
            maxf = max(maxf, count[ch])
            while (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res


def demo():
    """Run a simple demonstration for Longest Repeating Character Replacement problem."""
    s = Solution()
    text, k = "AABABBA", 1
    result = s.solve(text, k)
    return f"'{text}' with k={k} -> {result}"


register_problem(
    id=424,
    slug="longest_repeating_character_replacement",
    title="Longest Repeating Character Replacement",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "sliding_window"],
    url="https://leetcode.com/problems/longest-repeating-character-replacement/",
    notes="",
)
