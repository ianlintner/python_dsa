"""
Group Anagrams - LeetCode Problem

Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.
"""

from collections import defaultdict
from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Group anagrams using sorted strings as keys.

        Time Complexity: O(n * m log m) - where n is number of strings, m is max string length
        Space Complexity: O(n * m) - for storing all strings in groups

        Args:
            strs: List of strings to group

        Returns:
            List[List[str]]: Groups of anagrams
        """
        anagram_groups = defaultdict(list)

        for s in strs:
            # Use sorted string as key - anagrams will have same sorted form
            key = "".join(sorted(s))
            anagram_groups[key].append(s)

        return list(anagram_groups.values())

    def groupAnagramsFrequency(self, strs: List[str]) -> List[List[str]]:
        """
        Alternative using character frequency as key.

        Time Complexity: O(n * m) - where n is number of strings, m is max string length
        Space Complexity: O(n * m) - for storing all strings in groups
        """
        anagram_groups = defaultdict(list)

        for s in strs:
            # Use character frequency tuple as key
            char_count = [0] * 26
            for char in s:
                char_count[ord(char) - ord("a")] += 1
            key = tuple(char_count)
            anagram_groups[key].append(s)

        return list(anagram_groups.values())


def demo():
    """Demonstrate Group Anagrams solution with test cases."""
    solution = Solution()

    def sort_groups(groups):
        """Helper to sort groups for consistent comparison."""
        return sorted([sorted(group) for group in groups])

    test_cases = [
        TestCase(
            input_args=(["eat", "tea", "tan", "ate", "nat", "bat"],),
            expected=[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
            description="Basic anagram grouping",
        ),
        TestCase(input_args=([""],), expected=[[""]], description="Single empty string"),
        TestCase(input_args=(["a"],), expected=[["a"]], description="Single character"),
        TestCase(
            input_args=(["abc", "bca", "cab", "xyz", "zyx", "yxz"],),
            expected=[["abc", "bca", "cab"], ["xyz", "zyx", "yxz"]],
            description="Two anagram groups",
        ),
        TestCase(
            input_args=(["ab", "ba", "abc", "bca", "cab"],),
            expected=[["ab", "ba"], ["abc", "bca", "cab"]],
            description="Different length anagrams",
        ),
        TestCase(input_args=([""],), expected=[[""]], description="Empty string only"),
        TestCase(
            input_args=(["a", "b", "c"],), expected=[["a"], ["b"], ["c"]], description="No anagrams"
        ),
    ]

    # Custom comparison function for anagram groups
    def compare_results(actual, expected):
        return sort_groups(actual) == sort_groups(expected)

    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()
            actual = solution.groupAnagrams(*test_case.input_args)
            end_time = time.perf_counter()

            passed = compare_results(actual, test_case.expected)
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": passed,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args,
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    return create_demo_output(
        title="Group Anagrams",
        description="Group anagrams using sorted strings as keys",
        results=results,
        complexity_analysis={
            "time": "O(n * m log m) - where n is number of strings, m is max string length",
            "space": "O(n * m) - for storing all strings in groups",
        },
        key_insights=[
            "Anagrams have identical sorted character sequences",
            "Hash map with sorted string as key groups anagrams efficiently",
            "Alternative: use character frequency tuple as key for O(n*m) time",
            "defaultdict simplifies group creation logic",
        ],
        common_pitfalls=[
            "Remember anagrams can be returned in any order",
            "Consider empty strings as valid input",
            "Character frequency approach only works for lowercase letters",
            "Sorting approach works for any character set",
        ],
        follow_up_questions=[
            "How would you optimize for very long strings?",
            "What if strings contain unicode characters?",
            "Can you solve without sorting individual strings?",
            "How would you handle case-insensitive anagrams?",
        ],
    )


# Register this problem
register_problem(
    id=49,
    slug="group-anagrams",
    title="Group Anagrams",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags={"array", "hash-table", "string", "sorting"},
    module="src.interview_workbook.leetcode.arrays_hashing.group_anagrams",
    url="https://leetcode.com/problems/group-anagrams/",
    notes="Hash map with sorted string keys to group anagrams",
)
