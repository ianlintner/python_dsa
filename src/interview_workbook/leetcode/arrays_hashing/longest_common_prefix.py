"""
Longest Common Prefix - LeetCode Problem

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        """
        Find longest common prefix using character-by-character comparison.

        Time Complexity: O(S) - where S is sum of all characters in all strings
        Space Complexity: O(1) - only storing result string

        Args:
            strs: List of strings

        Returns:
            str: Longest common prefix
        """
        if not strs:
            return ""

        # Start with first string as potential prefix
        prefix = strs[0]

        for i in range(1, len(strs)):
            # Compare prefix with current string
            while prefix and not strs[i].startswith(prefix):
                # Remove last character from prefix
                prefix = prefix[:-1]

            # Early termination if no common prefix
            if not prefix:
                break

        return prefix

    def longestCommonPrefixVertical(self, strs: List[str]) -> str:
        """
        Vertical scanning approach - compare character by character across all strings.

        Time Complexity: O(S) - where S is sum of all characters
        Space Complexity: O(1) - constant extra space
        """
        if not strs:
            return ""

        # Find minimum length string
        min_len = min(len(s) for s in strs)

        for i in range(min_len):
            char = strs[0][i]
            # Check if this character matches in all strings
            for s in strs:
                if s[i] != char:
                    return strs[0][:i]

        # All characters up to min_len match
        return strs[0][:min_len]

    def longestCommonPrefixDivideConquer(self, strs: List[str]) -> str:
        """
        Divide and conquer approach.

        Time Complexity: O(S) - where S is sum of all characters
        Space Complexity: O(m log n) - recursion stack where m is length of result, n is number of strings
        """
        if not strs:
            return ""

        def common_prefix(str1: str, str2: str) -> str:
            """Find common prefix between two strings."""
            min_len = min(len(str1), len(str2))
            for i in range(min_len):
                if str1[i] != str2[i]:
                    return str1[:i]
            return str1[:min_len]

        def divide_conquer(left: int, right: int) -> str:
            """Divide and conquer recursive function."""
            if left == right:
                return strs[left]

            mid = (left + right) // 2
            left_prefix = divide_conquer(left, mid)
            right_prefix = divide_conquer(mid + 1, right)

            return common_prefix(left_prefix, right_prefix)

        return divide_conquer(0, len(strs) - 1)

    def longestCommonPrefixTrie(self, strs: List[str]) -> str:
        """
        Trie-based approach (educational but overkill for this problem).

        Time Complexity: O(S) - to build trie
        Space Complexity: O(S) - trie storage
        """
        if not strs:
            return ""

        # Simple trie node
        class TrieNode:
            def __init__(self):
                self.children = {}
                self.count = 0

        # Build trie
        root = TrieNode()
        for s in strs:
            node = root
            for char in s:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.count += 1

        # Find longest common prefix
        prefix = ""
        node = root
        n = len(strs)

        while len(node.children) == 1:
            char = next(iter(node.children))
            child = node.children[char]
            if child.count == n:  # All strings have this character
                prefix += char
                node = child
            else:
                break

        return prefix


def demo():
    """Demonstrate Longest Common Prefix solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=(["flower", "flow", "flight"],),
            expected="fl",
            description="Common prefix 'fl'",
        ),
        TestCase(
            input_args=(["dog", "racecar", "car"],), expected="", description="No common prefix"
        ),
        TestCase(
            input_args=(["interspecies", "interstellar", "interstate"],),
            expected="inters",
            description="Longer common prefix",
        ),
        TestCase(input_args=([""],), expected="", description="Single empty string"),
        TestCase(input_args=(["a"],), expected="a", description="Single character string"),
        TestCase(
            input_args=(["abc", "abc", "abc"],), expected="abc", description="All strings identical"
        ),
        TestCase(input_args=(["", "b"],), expected="", description="Empty string in array"),
        TestCase(
            input_args=(["ab", "a"],), expected="a", description="One string is prefix of another"
        ),
        TestCase(
            input_args=(["c", "acc", "ccc"],), expected="", description="First character differs"
        ),
    ]

    # Execute test cases manually
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()

            strs = test_case.input_args[0]
            actual = solution.longestCommonPrefix(strs)

            end_time = time.perf_counter()

            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": f"strs={strs}",
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": actual == test_case.expected,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": f"strs={test_case.input_args[0]}",
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    # Format results as test results string
    test_results_lines = ["=== Longest Common Prefix ===", ""]
    passed_count = 0
    total_time = sum(r["time_ms"] for r in results)

    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: '{result['expected']}'")
        test_results_lines.append(f"  Got: '{result['actual']}'")
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
• Horizontal scanning reduces prefix with each comparison
• Vertical scanning compares character by character across strings
• Early termination when no common prefix possible
• String.startswith() provides clean comparison logic

Common Pitfalls:
• Handle empty input array correctly
• Consider empty strings within the array
• Don't forget to handle single string case
• Be careful with string indexing bounds

Follow-up Questions:
• How would you optimize for very long strings?
• What if strings are sorted lexicographically?
• How would you find longest common suffix instead?
• Can you solve using binary search on prefix length?
"""

    return create_demo_output(
        problem_title="Longest Common Prefix",
        test_results=test_results_str,
        time_complexity="O(S) - where S is sum of all characters in all strings",
        space_complexity="O(1) - constant extra space for horizontal scanning",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=14,
    slug="longest-common-prefix",
    title="Longest Common Prefix",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["string", "array"],
    url="https://leetcode.com/problems/longest-common-prefix/",
    notes="String comparison with horizontal scanning approach",
)
