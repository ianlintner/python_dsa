"""
LeetCode 1143: Longest Common Subsequence

Given two strings text1 and text2, return the length of their longest common subsequence.
If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters
(can be none) deleted without changing the relative order of the remaining characters.

A common subsequence of two strings is a subsequence that is common to both strings.

Example:
    Input: text1 = "abcde", text2 = "ace"
    Output: 3
    Explanation: The longest common subsequence is "ace" and its length is 3.

Constraints:
    - 1 <= text1.length, text2.length <= 1000
    - text1 and text2 consist of only lowercase English characters.
"""

import time

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        Space-optimized 2D DP approach using 1D arrays.

        The key insight is that we only need the previous row to compute the current row.
        For each position (i, j), we have:
        - If text1[i-1] == text2[j-1]: dp[j] = dp_prev[j-1] + 1
        - Else: dp[j] = max(dp[j-1], dp_prev[j])

        Time: O(m * n), Space: O(n)
        """
        m, n = len(text1), len(text2)

        # Use two arrays to represent current and previous rows
        dp_prev = [0] * (n + 1)
        dp_curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp_curr[j] = dp_prev[j - 1] + 1
                else:
                    dp_curr[j] = max(dp_curr[j - 1], dp_prev[j])

            # Swap arrays for next iteration
            dp_prev, dp_curr = dp_curr, dp_prev

        return dp_prev[n]

    def longestCommonSubsequence2D(self, text1: str, text2: str) -> int:
        """
        Standard 2D DP approach.

        dp[i][j] represents the LCS length of text1[0:i] and text2[0:j]
        Base case: dp[0][j] = dp[i][0] = 0 (empty string has no common subsequence)

        Recurrence:
        - If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
        - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(text1), len(text2)

        # Create DP table with (m+1) x (n+1) dimensions
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    # Characters match, extend LCS by 1
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    # Take the maximum from either excluding current char from text1 or text2
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def longestCommonSubsequenceRecursive(self, text1: str, text2: str) -> int:
        """
        Recursive approach with memoization.

        For each position, we either:
        1. Match characters if they're equal
        2. Try skipping from either string and take the maximum

        Time: O(m * n), Space: O(m * n) for recursion stack + memoization
        """
        memo = {}

        def lcs(i: int, j: int) -> int:
            # Base cases
            if i == len(text1) or j == len(text2):
                return 0

            if (i, j) in memo:
                return memo[(i, j)]

            if text1[i] == text2[j]:
                # Characters match, include in LCS
                result = 1 + lcs(i + 1, j + 1)
            else:
                # Try both possibilities and take maximum
                result = max(lcs(i + 1, j), lcs(i, j + 1))

            memo[(i, j)] = result
            return result

        return lcs(0, 0)

    def longestCommonSubsequenceWithSequence(self, text1: str, text2: str) -> tuple[int, str]:
        """
        Extended version that returns both length and actual LCS.

        Uses 2D DP with backtracking to reconstruct the sequence.

        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Backtrack to find the actual LCS
        lcs = []
        i, j = m, n

        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                # This character is part of LCS
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                # Move up (exclude current char from text1)
                i -= 1
            else:
                # Move left (exclude current char from text2)
                j -= 1

        return dp[m][n], "".join(reversed(lcs))


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different LCS scenarios.
    """
    solution = Solution()

    demo_cases = [
        ("abcde", "ace", "Basic LCS example"),
        ("abc", "abc", "Identical strings"),
        ("abc", "def", "No common subsequence"),
        ("ABCDGH", "AEDFHR", "Mixed case LCS"),
        ("programming", "contest", "Real-world example"),
        ("AGGTAB", "GXTXAYB", "Classic textbook example"),
        ("abcdef", "fbdace", "Multiple valid LCS"),
    ]

    output = ["=== Longest Common Subsequence (LeetCode 1143) ===\n"]

    output.append("ALGORITHM EXPLANATION:")
    output.append("The Longest Common Subsequence (LCS) problem finds the longest sequence")
    output.append("that appears in both strings in the same relative order (but not necessarily")
    output.append("consecutive). This is a fundamental string algorithm with many applications.\n")

    output.append("DP STATE DEFINITION:")
    output.append("dp[i][j] = LCS length of text1[0:i] and text2[0:j]")
    output.append("Base case: dp[0][j] = dp[i][0] = 0 (empty string)")
    output.append("Recurrence:")
    output.append("  if text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1")
    output.append("  else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n")

    for text1, text2, description in demo_cases:
        output.append(f"--- {description} ---")
        output.append(f"Text1: '{text1}' (length {len(text1)})")
        output.append(f"Text2: '{text2}' (length {len(text2)})")

        # Get results from different approaches
        result_optimized = solution.longestCommonSubsequence(text1, text2)
        result_2d = solution.longestCommonSubsequence2D(text1, text2)
        result_recursive = solution.longestCommonSubsequenceRecursive(text1, text2)
        length, sequence = solution.longestCommonSubsequenceWithSequence(text1, text2)

        output.append(f"LCS Length: {result_optimized}")
        if sequence:
            output.append(f"Actual LCS: '{sequence}'")
        else:
            output.append("No common subsequence found")

        # Verify all approaches give same result
        assert result_optimized == result_2d == result_recursive == length
        output.append("")

    # Performance comparison
    output.append("PERFORMANCE COMPARISON:")
    test_text1 = "abcdefghijklmnopqrstuvwxyz" * 10  # 260 chars
    test_text2 = "acegikmoqsuwy" * 20  # 260 chars

    methods = [
        ("Space-optimized DP", solution.longestCommonSubsequence),
        ("Standard 2D DP", solution.longestCommonSubsequence2D),
        ("Recursive + Memo", solution.longestCommonSubsequenceRecursive),
    ]

    for name, method in methods:
        start_time = time.perf_counter()
        result = method(test_text1, test_text2)
        end_time = time.perf_counter()

        output.append(
            f"{name:20} | Result: {result:3} | Time: {(end_time - start_time) * 1000:.3f}ms"
        )

    output.append("\nSPACE COMPLEXITY ANALYSIS:")
    output.append("• Space-optimized DP: O(min(m,n)) - only need one row")
    output.append("• Standard 2D DP: O(m*n) - full DP table")
    output.append("• Recursive: O(m*n) - memoization table + O(m+n) stack")

    output.append("\nREAL-WORLD APPLICATIONS:")
    output.append("• DNA sequence alignment in bioinformatics")
    output.append("• File difference tools (diff, git)")
    output.append("• Plagiarism detection systems")
    output.append("• Version control merge algorithms")
    output.append("• Spell checkers and auto-correction")
    output.append("• Data synchronization protocols")

    # Visual example of DP table construction
    output.append("\nDP TABLE VISUALIZATION (for 'AGGTAB' vs 'GXTXAYB'):")
    text1, text2 = "AGGTAB", "GXTXAYB"
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Print table header
    output.append("    " + "  ".join([" "] + list(text2)))
    output.append("  " + "+--" * (n + 1) + "+")

    # Print table rows
    for i in range(m + 1):
        row_label = " " if i == 0 else text1[i - 1]
        row_values = " ".join(f"{dp[i][j]:2}" for j in range(n + 1))
        output.append(f"{row_label} | {row_values} |")

    output.append("\nThe final answer is dp[6][7] = 4, representing LCS 'GTAB'")

    return "\n".join(output)


# Test cases covering various scenarios
TEST_CASES = [
    TestCase(input_data=("abcde", "ace"), expected=3, description="Basic LCS example - 'ace'"),
    TestCase(input_data=("abc", "abc"), expected=3, description="Identical strings"),
    TestCase(input_data=("abc", "def"), expected=0, description="No common characters"),
    TestCase(input_data=("", "abc"), expected=0, description="Empty first string"),
    TestCase(input_data=("abc", ""), expected=0, description="Empty second string"),
    TestCase(input_data=("", ""), expected=0, description="Both strings empty"),
    TestCase(input_data=("a", "a"), expected=1, description="Single character match"),
    TestCase(input_data=("a", "b"), expected=0, description="Single character no match"),
    TestCase(input_data=("ABCDGH", "AEDFHR"), expected=3, description="Mixed case LCS - 'ADH'"),
    TestCase(
        input_data=("programming", "contest"),
        expected=4,
        description="Real-world example - 'ogrt' or similar",
    ),
    TestCase(
        input_data=("AGGTAB", "GXTXAYB"),
        expected=4,
        description="Classic textbook example - 'GTAB'",
    ),
    TestCase(
        input_data=("abcdefghijklmnop", "acegikmoqsuwy"),
        expected=7,
        description="Longer string with pattern",
    ),
    TestCase(input_data=("longest", "stone"), expected=3, description="LCS 'one' or similar"),
    TestCase(
        input_data=("intention", "execution"),
        expected=5,
        description="Edit distance related - 'ntion'",
    ),
    TestCase(
        input_data=("abcdef" * 100, "ace" * 100), expected=300, description="Performance test case"
    ),
]


def test_solution():
    """Test the solution with various test cases."""
    solution = Solution()

    def test_function(text1: str, text2: str) -> int:
        # Test all approaches give same result
        result1 = solution.longestCommonSubsequence(text1, text2)
        result2 = solution.longestCommonSubsequence2D(text1, text2)
        result3 = solution.longestCommonSubsequenceRecursive(text1, text2)

        assert result1 == result2 == result3, (
            f"Inconsistent results: {result1}, {result2}, {result3}"
        )
        return result1

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="longest-common-subsequence",
    leetcode_num=1143,
    title="Longest Common Subsequence",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_2D,
    solution_func=Solution().longestCommonSubsequence,
    test_func=test_solution,
    demo_func=create_demo_output,
)
