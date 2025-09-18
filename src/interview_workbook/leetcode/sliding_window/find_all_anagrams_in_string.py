"""
Find All Anagrams In String

TODO: Add problem description
"""

from collections import Counter

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return list of start indices of anagrams of p in s."""
        s, p = args
        res = []
        if len(p) > len(s):
            return res
        p_count = Counter(p)
        s_count = Counter()
        l = 0
        for r, ch in enumerate(s):
            s_count[ch] += 1
            if r - l + 1 > len(p):
                s_count[s[l]] -= 1
                if s_count[s[l]] == 0:
                    del s_count[s[l]]
                l += 1
            if s_count == p_count:
                res.append(l)
        return res


def demo():
    """Run a simple demonstration for Find All Anagrams in String problem."""
    s = Solution()
    text, pattern = "cbaebabacd", "abc"
    result = s.solve(text, pattern)
    print(f"Finding all anagrams of '{pattern}' in '{text}' -> {result}")
    return f"'{pattern}' in '{text}' -> {result}"


register_problem(
    id=438,
    slug="find_all_anagrams_in_string",
    title="Find All Anagrams in a String",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "sliding_window", "hashmap"],
    url="https://leetcode.com/problems/find-all-anagrams-in-a-string/",
    notes="",
)
