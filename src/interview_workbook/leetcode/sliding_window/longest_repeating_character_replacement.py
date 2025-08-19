"""
Longest Repeating Character Replacement - LeetCode Problem

You are given a string s and an integer k. You can choose any character of the string and change it
to any other uppercase English letter. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing
the above operations.
"""

from collections import defaultdict

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """
        Find longest repeating character replacement using sliding window.

        Time Complexity: O(n) - single pass through string
        Space Complexity: O(1) - at most 26 characters in frequency map

        Args:
            s: Input string of uppercase English letters
            k: Maximum number of character replacements allowed

        Returns:
            int: Length of longest substring with same character after replacements
        """
        char_count = defaultdict(int)
        left = 0
        max_length = 0
        max_char_count = 0

        for right in range(len(s)):
            # Add current character to frequency map
            char_count[s[right]] += 1
            max_char_count = max(max_char_count, char_count[s[right]])

            # Current window size
            window_size = right - left + 1

            # If we need more than k replacements, shrink window
            if window_size - max_char_count > k:
                char_count[s[left]] -= 1
                left += 1

            # Update maximum length
            max_length = max(max_length, right - left + 1)

        return max_length

    def characterReplacementOptimized(self, s: str, k: int) -> int:
        """
        Optimized version that doesn't update max_char_count when shrinking.

        Time Complexity: O(n) - single pass
        Space Complexity: O(1) - at most 26 characters
        """
        char_count = defaultdict(int)
        left = 0
        max_char_count = 0

        for right in range(len(s)):
            char_count[s[right]] += 1
            max_char_count = max(max_char_count, char_count[s[right]])

            # If current window is invalid, slide the window
            if right - left + 1 - max_char_count > k:
                char_count[s[left]] -= 1
                left += 1

        # The final window size is the answer
        return len(s) - left

    def characterReplacementBruteForce(self, s: str, k: int) -> int:
        """
        Brute force approach checking all possible substrings (not optimal).

        Time Complexity: O(n²) - nested loops with character counting
        Space Complexity: O(1) - frequency array
        """
        max_length = 0
        n = len(s)

        for i in range(n):
            char_count = defaultdict(int)
            max_char_freq = 0

            for j in range(i, n):
                char_count[s[j]] += 1
                max_char_freq = max(max_char_freq, char_count[s[j]])

                window_size = j - i + 1
                replacements_needed = window_size - max_char_freq

                if replacements_needed <= k:
                    max_length = max(max_length, window_size)
                else:
                    break  # No point checking longer substrings from this start

        return max_length


def demo():
    """Demonstrate Longest Repeating Character Replacement solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(input_args=("ABAB", 2), expected=4, description="Replace B's to get 'AAAA'"),
        TestCase(
            input_args=("AABABBA", 1),
            expected=4,
            description="Replace one character to get 'AAAA' or 'BBBB'",
        ),
        TestCase(input_args=("AAAA", 2), expected=4, description="Already all same characters"),
        TestCase(
            input_args=("ABCDEF", 1),
            expected=2,
            description="All different characters - can get length 2",
        ),
        TestCase(input_args=("A", 1), expected=1, description="Single character"),
        TestCase(
            input_args=("AABCABCBB", 2),
            expected=5,
            description="Complex case with multiple options",
        ),
        TestCase(input_args=("ABABACB", 3), expected=7, description="Can replace entire string"),
        TestCase(input_args=("AAABBBCCC", 2), expected=5, description="Groups of same characters"),
        TestCase(input_args=("ABCABC", 2), expected=4, description="Repeating pattern"),
    ]

    # Execute test cases manually
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()

            s, k = test_case.input_args
            actual = solution.characterReplacement(s, k)

            end_time = time.perf_counter()

            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": f"s='{s}', k={k}",
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
                    "input": f"s='{test_case.input_args[0]}', k={test_case.input_args[1]}",
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    # Format results as test results string
    test_results_lines = ["=== Longest Repeating Character Replacement ===", ""]
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
• Sliding window with character frequency tracking
• Key insight: window_size - max_char_count = replacements needed
• Shrink window when replacements exceed k
• max_char_count tracks most frequent character in current window

Common Pitfalls:
• Remember to update max_char_count when adding characters
• Window becomes invalid when replacements needed > k
• Consider that we want the longest valid window
• Optimization: don't need to recalculate max_char_count when shrinking

Follow-up Questions:
• What if we could replace with any character, not just uppercase letters?
• How would you modify to find the actual substring, not just length?
• What if k could be negative or zero?
• Can you solve for lowercase letters or mixed case?
"""

    return create_demo_output(
        problem_title="Longest Repeating Character Replacement",
        test_results=test_results_str,
        time_complexity="O(n) - single pass through string with sliding window",
        space_complexity="O(1) - at most 26 characters in frequency map",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=424,
    slug="longest-repeating-character-replacement",
    title="Longest Repeating Character Replacement",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["hash-table", "string", "sliding-window"],
    url="https://leetcode.com/problems/longest-repeating-character-replacement/",
    notes="Sliding window with character frequency and replacement counting",
)
