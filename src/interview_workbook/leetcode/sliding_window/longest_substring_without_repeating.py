"""
Longest Substring Without Repeating Characters - LeetCode Problem

Given a string s, find the length of the longest substring without repeating characters.
"""

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find longest substring without repeating characters using sliding window.

        Time Complexity: O(n) - each character visited at most twice
        Space Complexity: O(min(m, n)) - where m is charset size, n is string length

        Args:
            s: Input string

        Returns:
            int: Length of longest substring without repeating characters
        """
        if not s:
            return 0

        char_index = {}  # Map character to its most recent index
        left = 0
        max_length = 0

        for right in range(len(s)):
            char = s[right]

            # If character is already in current window, move left pointer
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1

            # Update character's most recent index
            char_index[char] = right

            # Update maximum length
            max_length = max(max_length, right - left + 1)

        return max_length

    def lengthOfLongestSubstringSet(self, s: str) -> int:
        """
        Alternative using set for character tracking.

        Time Complexity: O(2n) = O(n) - in worst case each character visited twice
        Space Complexity: O(min(m, n)) - set storage
        """
        if not s:
            return 0

        char_set = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            # Shrink window until no duplicates
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            # Add current character to set
            char_set.add(s[right])

            # Update maximum length
            max_length = max(max_length, right - left + 1)

        return max_length

    def lengthOfLongestSubstringBruteForce(self, s: str) -> int:
        """
        Brute force approach checking all substrings (not optimal).

        Time Complexity: O(n³) - nested loops with set operations
        Space Complexity: O(min(m, n)) - set storage for checking duplicates
        """
        if not s:
            return 0

        max_length = 0
        n = len(s)

        for i in range(n):
            for j in range(i, n):
                # Check if substring s[i:j+1] has all unique characters
                substring = s[i : j + 1]
                if len(substring) == len(set(substring)):
                    max_length = max(max_length, len(substring))
                else:
                    break  # No point checking longer substrings from this start

        return max_length


def demo():
    """Demonstrate Longest Substring Without Repeating Characters solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(input_args=("abcabcbb",), expected=3, description="Basic case - 'abc' is longest"),
        TestCase(input_args=("bbbbb",), expected=1, description="All same characters - 'b'"),
        TestCase(input_args=("pwwkew",), expected=3, description="Mixed case - 'wke' is longest"),
        TestCase(input_args=("",), expected=0, description="Empty string"),
        TestCase(input_args=(" ",), expected=1, description="Single space character"),
        TestCase(input_args=("au",), expected=2, description="Two unique characters"),
        TestCase(input_args=("dvdf",), expected=3, description="'vdf' is longest"),
        TestCase(input_args=("anviaj",), expected=5, description="'nviaj' is longest"),
        TestCase(input_args=("abcdef",), expected=6, description="All unique characters"),
        TestCase(input_args=("tmmzuxt",), expected=5, description="'mzuxt' is longest"),
    ]

    results = run_test_cases(solution.lengthOfLongestSubstring, test_cases)

    return create_demo_output(
        problem_title="Longest Substring Without Repeating Characters",
        test_results=results,
        time_complexity="O(n) - each character visited at most twice",
        space_complexity="O(min(m, n)) - hash map/set storage where m is charset size",
        approach_notes="Sliding window technique with hash map for tracking character positions",
    )


# Register this problem
register_problem(
    id=3,
    slug="longest-substring-without-repeating-characters",
    title="Longest Substring Without Repeating Characters",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["hash-table", "string", "sliding-window"],
    url="https://leetcode.com/problems/longest-substring-without-repeating-characters/",
    notes="Sliding window with hash map for tracking character positions",
)
