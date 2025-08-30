"""
Valid Anagram

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, s: str, t: str) -> bool:
        """Check if two strings are anagrams using character counting."""
        if len(s) != len(t):
            return False

        from collections import Counter

        return Counter(s) == Counter(t)


def demo():
    """Demonstrate valid anagram solution."""
    sol = Solution()
    assert sol.solve("anagram", "nagaram") is True
    assert sol.solve("rat", "car") is False
    return "Valid Anagram demo passed."


register_problem(
    id=242,
    slug="valid_anagram",
    title="Valid Anagram",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["string", "hashmap", "sorting"],
    url="https://leetcode.com/problems/valid-anagram/",
    notes="",
)
