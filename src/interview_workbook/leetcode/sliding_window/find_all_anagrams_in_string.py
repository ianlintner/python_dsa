"""
LeetCode 438: Find All Anagrams in a String

Given two strings s and p, return an array of all the start indices of p's anagrams in s.
You may return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.

URL: https://leetcode.com/problems/find-all-anagrams-in-a-string/
Difficulty: Medium
Category: Sliding Window

Patterns:
- Fixed-size sliding window (size of pattern)
- Frequency counting for anagram detection
- Efficient window management with character frequency maps

Complexity:
- Time: O(|s| + |p|) - linear scan with constant window operations
- Space: O(|p|) - frequency maps for pattern characters

Key Insights:
- Anagrams have identical character frequencies
- Use sliding window of pattern length over string
- Maintain frequency count for current window
- Compare window frequency with pattern frequency

Edge Cases:
- Pattern longer than string (no anagrams possible)
- Empty strings
- Single character pattern and string
- Pattern with repeated characters
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty
from collections import Counter
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        Find all start indices of anagrams of p in s.

        Args:
            s: Source string to search in
            p: Pattern string to find anagrams of

        Returns:
            List of starting indices where anagrams are found
        """
        if len(p) > len(s):
            return []

        result = []
        p_count = Counter(p)
        window_count = Counter()

        # Initialize window with first len(p) characters
        for i in range(len(p)):
            window_count[s[i]] += 1

        # Check if initial window is an anagram
        if window_count == p_count:
            result.append(0)

        # Slide the window
        for i in range(len(p), len(s)):
            # Add new character to window
            window_count[s[i]] += 1

            # Remove character that's sliding out
            left_char = s[i - len(p)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            # Check if current window is an anagram
            if window_count == p_count:
                result.append(i - len(p) + 1)

        return result

    def findAnagramsOptimized(self, s: str, p: str) -> List[int]:
        """
        Optimized version using array instead of Counter for lowercase letters only.

        Args:
            s: Source string to search in
            p: Pattern string to find anagrams of

        Returns:
            List of starting indices where anagrams are found
        """
        if len(p) > len(s):
            return []

        result = []

        # Frequency arrays for pattern and sliding window
        p_freq = [0] * 26
        window_freq = [0] * 26

        # Count pattern frequencies
        for char in p:
            p_freq[ord(char) - ord("a")] += 1

        # Initialize sliding window
        for i in range(len(p)):
            window_freq[ord(s[i]) - ord("a")] += 1

        # Check initial window
        if window_freq == p_freq:
            result.append(0)

        # Slide the window
        for i in range(len(p), len(s)):
            # Add new character
            window_freq[ord(s[i]) - ord("a")] += 1
            # Remove old character
            window_freq[ord(s[i - len(p)]) - ord("a")] -= 1

            # Check if current window matches pattern
            if window_freq == p_freq:
                result.append(i - len(p) + 1)

        return result


# Test cases
test_cases = [
    TestCase(("abab", "ab"), [0, 2], "Basic case with overlapping anagrams"),
    TestCase(("abcdefghijklmnopqrstuvwxyz", "abc"), [0], "Single anagram at start"),
    TestCase(("aab", "ab"), [1], "Anagram in middle"),
    TestCase(("abab", "abab"), [0], "Pattern matches entire substring"),
    TestCase(("abaacbabc", "abc"), [3, 4, 6], "Multiple anagrams"),
    TestCase(("aa", "bb"), [], "No anagrams possible"),
    TestCase(("a", "a"), [0], "Single character match"),
    TestCase(("ab", "ba"), [0], "Simple anagram pair"),
    TestCase(("aaaaaaaaaa", "aaaaaaaaaaaaa"), [], "Pattern longer than string"),
]


def demo() -> str:
    """Run Find All Anagrams demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.findAnagrams, test_cases, "LeetCode 438: Find All Anagrams in a String"
    )

    return create_demo_output(
        "Find All Anagrams in a String",
        test_results,
        time_complexity="O(|s| + |p|)",
        space_complexity="O(|p|)",
        approach_notes="""
Key insights:
1. Use sliding window of pattern length to scan through string
2. Maintain character frequency count for current window
3. Compare window frequency with pattern frequency for anagram detection
4. Efficiently update window by adding new character and removing old one

Two implementations provided:
- Counter-based: Works with any characters, more readable
- Array-based: Optimized for lowercase letters only, slightly faster

Both achieve optimal O(|s| + |p|) time complexity with linear scan and
constant-time window operations.
        """.strip(),
    )


# Register the problem
register_problem(
    id=438,
    slug="find_all_anagrams_in_string",
    title="Find All Anagrams in a String",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "sliding_window", "hashmap"],
    url="https://leetcode.com/problems/find-all-anagrams-in-a-string/",
    notes="Classic sliding window problem with frequency counting for anagram detection",
)
