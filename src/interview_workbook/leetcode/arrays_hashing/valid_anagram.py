"""
Valid Anagram - LeetCode Problem

Given two strings s and t, return true if t is an anagram of s, and false otherwise.
An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.
"""

from typing import Dict
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Check if two strings are anagrams using character frequency counting.

        Time Complexity: O(n) - where n is length of strings
        Space Complexity: O(1) - at most 26 characters in frequency map

        Args:
            s: First string
            t: Second string

        Returns:
            bool: True if strings are anagrams, False otherwise
        """
        if len(s) != len(t):
            return False

        char_count = {}

        # Count characters in first string
        for char in s:
            char_count[char] = char_count.get(char, 0) + 1

        # Subtract character counts for second string
        for char in t:
            if char not in char_count:
                return False
            char_count[char] -= 1
            if char_count[char] == 0:
                del char_count[char]

        return len(char_count) == 0

    def isAnagramSort(self, s: str, t: str) -> bool:
        """
        Alternative solution using sorting.

        Time Complexity: O(n log n) - sorting dominates
        Space Complexity: O(n) - space for sorted strings
        """
        return sorted(s) == sorted(t)

    def isAnagramCounter(self, s: str, t: str) -> bool:
        """
        Alternative using collections.Counter for cleaner code.

        Time Complexity: O(n)
        Space Complexity: O(1) - at most 26 characters
        """
        from collections import Counter

        return Counter(s) == Counter(t)


def demo():
    """Demonstrate Valid Anagram solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=("anagram", "nagaram"), expected=True, description="Basic anagram case"
        ),
        TestCase(input_args=("rat", "car"), expected=False, description="Different characters"),
        TestCase(input_args=("listen", "silent"), expected=True, description="Common anagram pair"),
        TestCase(input_args=("", ""), expected=True, description="Empty strings"),
        TestCase(input_args=("a", "ab"), expected=False, description="Different lengths"),
        TestCase(input_args=("aab", "baa"), expected=True, description="Repeated characters"),
        TestCase(input_args=("abc", "def"), expected=False, description="Completely different"),
        TestCase(
            input_args=("aabbcc", "abcabc"), expected=True, description="Multiple repeated chars"
        ),
    ]

    results = run_test_cases(solution.isAnagram, test_cases)

    return create_demo_output(
        title="Valid Anagram",
        description="Check if two strings are anagrams using character frequency counting",
        results=results,
        complexity_analysis={
            "time": "O(n) - single pass through both strings",
            "space": "O(1) - at most 26 characters in frequency map",
        },
        key_insights=[
            "Anagrams must have same length and character frequencies",
            "Hash map provides O(1) character lookup and counting",
            "Early length check avoids unnecessary processing",
            "Counter approach from collections provides cleaner code",
        ],
        common_pitfalls=[
            "Don't forget to check string lengths first",
            "Consider case sensitivity requirements",
            "Handle empty strings correctly",
            "Be careful with character count decrementing logic",
        ],
        follow_up_questions=[
            "What if inputs contain unicode characters?",
            "How would you handle case-insensitive anagrams?",
            "Can you optimize space further for specific constraints?",
            "How would you find all anagram groups in a list?",
        ],
    )


# Register this problem
register_problem(
    id=242,
    slug="valid-anagram",
    title="Valid Anagram",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags={"hash-table", "string", "sorting"},
    module="src.interview_workbook.leetcode.arrays_hashing.valid_anagram",
    url="https://leetcode.com/problems/valid-anagram/",
    notes="Character frequency counting with hash map",
)
