"""
Permutation In String

TODO: Add problem description
"""

from collections import Counter

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return True if any permutation of s1 is a substring of s2."""
        s1, s2 = args
        if len(s1) > len(s2):
            return False
        s1_count = Counter(s1)
        window = Counter()
        l = 0
        for r, ch in enumerate(s2):
            window[ch] += 1
            if r - l + 1 > len(s1):
                window[s2[l]] -= 1
                if window[s2[l]] == 0:
                    del window[s2[l]]
                l += 1
            if window == s1_count:
                return True
        return False


def demo():
    """Run a simple demonstration for Permutation In String."""
    s1 = "ab"
    s2 = "eidbaooo"
    result = Solution().solve(s1, s2)
    print(f"Input: s1={s1}, s2={s2} -> Contains permutation? {result}")
    return f"Input: s1={s1}, s2={s2} -> Contains permutation? {result}"


register_problem(
    id=567,
    slug="permutation_in_string",
    title="Permutation In String",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["hash table", "two pointers", "string", "sliding window"],
    url="https://leetcode.com/problems/permutation-in-string/",
    notes="Sliding window with character counts compared to target counts.",
)
