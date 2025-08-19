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

    # Format results as test results string
    test_results_lines = ["=== Group Anagrams ===", ""]
    passed_count = 0
    total_time = sum(r["time_ms"] for r in results)
    
    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: {result['expected']}")
        test_results_lines.append(f"  Got: {result['actual']}")
        test_results_lines.append(f"  Time: {result['time_ms']:.3f}ms")
        test_results_lines.append("")
        if result["passed"]:
            passed_count += 1
    
    test_results_lines.append(f"Results: {passed_count}/{len(results)} passed")
    test_results_lines.append(f"Total time: {total_time:.3f}ms")
    
    if passed_count == len(results):
        test_results_lines.append("🎉 All tests passed!")
    else:
        test_results_lines.append(f"❌ {len(results) - passed_count} test(s) failed")
    
    test_results_str = "\n".join(test_results_lines)
    
    approach_notes = """
Key Insights:
• Anagrams have identical sorted character sequences
• Hash map with sorted string as key groups anagrams efficiently
• Alternative: use character frequency tuple as key for O(n*m) time
• defaultdict simplifies group creation logic

Common Pitfalls:
• Remember anagrams can be returned in any order
• Consider empty strings as valid input
• Character frequency approach only works for lowercase letters
• Sorting approach works for any character set

Follow-up Questions:
• How would you optimize for very long strings?
• What if strings contain unicode characters?
• Can you solve without sorting individual strings?
• How would you handle case-insensitive anagrams?
"""

    return create_demo_output(
        problem_title="Group Anagrams",
        test_results=test_results_str,
        time_complexity="O(n * m log m) - where n is number of strings, m is max string length",
        space_complexity="O(n * m) - for storing all strings in groups",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=49,
    slug="group-anagrams",
    title="Group Anagrams",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hash-table", "string", "sorting"],
    url="https://leetcode.com/problems/group-anagrams/",
    notes="Hash map with sorted string keys to group anagrams",
)
