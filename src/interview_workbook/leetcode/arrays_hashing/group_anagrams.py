"""
Group Anagrams

Given an array of strings, group the anagrams together.

Two strings are anagrams if they contain the same characters in different orders.
"""

import random
from collections import defaultdict

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

random.seed(0)


class Solution:
    def solve(self, strs: list[str]) -> list[list[str]]:
        """Group anagrams from a list of words.

        Approach:
        - Sort each word into a tuple of characters as the key.
        - Collect words sharing the same sorted key.
        """
        groups = defaultdict(list)
        for word in strs:
            key = "".join(sorted(word))
            groups[key].append(word)
        return list(groups.values())


def demo():
    """Demonstration of Group Anagrams problem."""
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    solver = Solution()
    result = solver.solve(strs)
    return f"Input: {strs}\nGrouped Anagrams: {result}"


register_problem(
    id=49,
    slug="group_anagrams",
    title="Group Anagrams",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["hashmap", "string", "sorting"],
    url="https://leetcode.com/problems/group-anagrams/",
    notes="Uses sorted string as key in hashmap to group anagrams.",
)
