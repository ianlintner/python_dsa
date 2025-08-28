"""
LeetCode 72: Edit Distance (Levenshtein Distance)

Given two strings word1 and word2, return the minimum number of operations required
to convert word1 to word2.

You have the following three operations permitted on a word:
• Insert a character
• Delete a character
• Replace a character

Example:
    Input: word1 = "horse", word2 = "ros"
    Output: 3
    Explanation:
    horse -> rorse (replace 'h' with 'r')
    rorse -> rose (remove 'r')
    rose -> ros (remove 'e')

Constraints:
    - 0 <= word1.length, word2.length <= 500
    - word1 and word2 consist of lowercase English letters.
"""

import time
from typing import List, Tuple

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Space-optimized 2D DP approach using 1D arrays.

        The key insight is that we only need the previous row to compute the current row.
        For each position (i, j), we have:
        - If word1[i-1] == word2[j-1]: dp[j] = dp_prev[j-1] (no operation needed)
        - Else: dp[j] = 1 + min(dp[j-1], dp_prev[j], dp_prev[j-1])
          - dp[j-1]: insert word2[j-1]
          - dp_prev[j]: delete word1[i-1]
          - dp_prev[j-1]: replace word1[i-1] with word2[j-1]

        Time: O(m * n), Space: O(n)
        """
        m, n = len(word1), len(word2)

        # Use two arrays to represent current and previous rows
        dp_prev = list(range(n + 1))  # Base case: transforming empty string to word2[:j]
        dp_curr = [0] * (n + 1)

        for i in range(1, m + 1):
            dp_curr[0] = i  # Base case: transforming word1[:i] to empty string

            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match, no operation needed
                    dp_curr[j] = dp_prev[j - 1]
                else:
                    # Take minimum of three operations + 1
                    dp_curr[j] = 1 + min(
                        dp_curr[j - 1],  # Insert word2[j-1]
                        dp_prev[j],  # Delete word1[i-1]
                        dp_prev[j - 1],  # Replace word1[i-1] with word2[j-1]
                    )

            # Swap arrays for next iteration
            dp_prev, dp_curr = dp_curr, dp_prev

        return dp_prev[n]

    def minDistance2D(self, word1: str, word2: str) -> int:
        """
        Standard 2D DP approach.

        dp[i][j] represents the minimum edit distance between word1[0:i] and word2[0:j]
        Base cases:
        - dp[0][j] = j (insert j characters)
        - dp[i][0] = i (delete i characters)

        Recurrence:
        - If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]
        - Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(word1), len(word2)

        # Create DP table with (m+1) x (n+1) dimensions
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete i characters from word1
        for j in range(n + 1):
            dp[0][j] = j  # Insert j characters to make word2

        # Fill the DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Take minimum of three operations + 1
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],  # Delete from word1
                        dp[i][j - 1],  # Insert into word1 (or delete from word2)
                        dp[i - 1][j - 1],  # Replace
                    )

        return dp[m][n]

    def minDistanceRecursive(self, word1: str, word2: str) -> int:
        """
        Recursive approach with memoization.

        For each position, we either:
        1. Match characters if they're equal (no cost)
        2. Try all three operations and take the minimum

        Time: O(m * n), Space: O(m * n) for recursion stack + memoization
        """
        memo = {}

        def editDistance(i: int, j: int) -> int:
            # Base cases
            if i == 0:
                return j  # Insert j characters
            if j == 0:
                return i  # Delete i characters

            if (i, j) in memo:
                return memo[(i, j)]

            if word1[i - 1] == word2[j - 1]:
                # Characters match, no operation needed
                result = editDistance(i - 1, j - 1)
            else:
                # Try all three operations and take minimum
                result = 1 + min(
                    editDistance(i - 1, j),  # Delete
                    editDistance(i, j - 1),  # Insert
                    editDistance(i - 1, j - 1),  # Replace
                )

            memo[(i, j)] = result
            return result

        return editDistance(len(word1), len(word2))

    def minDistanceWithOperations(self, word1: str, word2: str) -> Tuple[int, List[str]]:
        """
        Extended version that returns both distance and actual operations.

        Uses 2D DP with backtracking to reconstruct the sequence of operations.

        Time: O(m * n), Space: O(m * n)
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        # Backtrack to find the actual operations
        operations = []
        i, j = m, n

        while i > 0 or j > 0:
            if i == 0:
                # Only insertions left
                operations.append(f"Insert '{word2[j - 1]}' at position {i}")
                j -= 1
            elif j == 0:
                # Only deletions left
                operations.append(f"Delete '{word1[i - 1]}' at position {i - 1}")
                i -= 1
            elif word1[i - 1] == word2[j - 1]:
                # Characters match, no operation
                i -= 1
                j -= 1
            else:
                # Find which operation was used
                delete_cost = dp[i - 1][j]
                insert_cost = dp[i][j - 1]
                replace_cost = dp[i - 1][j - 1]

                min_cost = min(delete_cost, insert_cost, replace_cost)

                if min_cost == replace_cost:
                    operations.append(
                        f"Replace '{word1[i - 1]}' with '{word2[j - 1]}' at position {i - 1}"
                    )
                    i -= 1
                    j -= 1
                elif min_cost == delete_cost:
                    operations.append(f"Delete '{word1[i - 1]}' at position {i - 1}")
                    i -= 1
                else:  # insert_cost
                    operations.append(f"Insert '{word2[j - 1]}' at position {i}")
                    j -= 1

        return dp[m][n], list(reversed(operations))


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different edit distance scenarios.
    """
    solution = Solution()

    demo_cases = [
        ("horse", "ros", "Classic example from problem"),
        ("intention", "execution", "Longer transformation"),
        ("", "abc", "Empty to non-empty"),
        ("abc", "", "Non-empty to empty"),
        ("abc", "abc", "Identical strings"),
        ("cat", "cut", "Single character replacement"),
        ("sunday", "saturday", "Common prefix/suffix"),
        ("kitten", "sitting", "Classic edit distance example"),
        ("flaw", "lawn", "Multiple operations needed"),
    ]

    output = ["=== Edit Distance / Levenshtein Distance (LeetCode 72) ===\n"]

    output.append("ALGORITHM EXPLANATION:")
    output.append("The Edit Distance (Levenshtein Distance) measures the minimum number of")
    output.append("single-character edits (insertions, deletions, or substitutions) required")
    output.append("to transform one string into another. This is fundamental in many areas")
    output.append("like spell checking, DNA analysis, and data cleaning.\n")

    output.append("DP STATE DEFINITION:")
    output.append("dp[i][j] = minimum edit distance between word1[0:i] and word2[0:j]")
    output.append("Base cases:")
    output.append("  dp[0][j] = j (insert j characters)")
    output.append("  dp[i][0] = i (delete i characters)")
    output.append("Recurrence:")
    output.append("  if word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]")
    output.append("  else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])")
    output.append("                                 delete    insert    replace\n")

    for word1, word2, description in demo_cases:
        output.append(f"--- {description} ---")
        output.append(f"Word1: '{word1}' (length {len(word1)})")
        output.append(f"Word2: '{word2}' (length {len(word2)})")

        # Get results from different approaches
        result_optimized = solution.minDistance(word1, word2)
        result_2d = solution.minDistance2D(word1, word2)
        result_recursive = solution.minDistanceRecursive(word1, word2)
        distance, operations = solution.minDistanceWithOperations(word1, word2)

        output.append(f"Edit Distance: {result_optimized}")

        if operations:
            output.append("Operations sequence:")
            for i, op in enumerate(operations, 1):
                output.append(f"  {i}. {op}")
        else:
            output.append("No operations needed (identical strings)")

        # Verify all approaches give same result
        assert result_optimized == result_2d == result_recursive == distance
        output.append("")

    # Performance comparison
    output.append("PERFORMANCE COMPARISON:")
    test_word1 = "abcdefghijklmnop" * 10  # 150 chars
    test_word2 = "acegikmoqsuwy" * 10  # 130 chars

    methods = [
        ("Space-optimized DP", solution.minDistance),
        ("Standard 2D DP", solution.minDistance2D),
        ("Recursive + Memo", solution.minDistanceRecursive),
    ]

    for name, method in methods:
        start_time = time.perf_counter()
        result = method(test_word1, test_word2)
        end_time = time.perf_counter()

        output.append(
            f"{name:20} | Result: {result:3} | Time: {(end_time - start_time) * 1000:.3f}ms"
        )

    output.append("\nSPACE COMPLEXITY ANALYSIS:")
    output.append("• Space-optimized DP: O(min(m,n)) - only need one row")
    output.append("• Standard 2D DP: O(m*n) - full DP table")
    output.append("• Recursive: O(m*n) - memoization table + O(m+n) stack")

    output.append("\nREAL-WORLD APPLICATIONS:")
    output.append("• Spell checkers and auto-correction systems")
    output.append("• DNA sequence alignment and mutation analysis")
    output.append("• Plagiarism detection and text similarity")
    output.append("• Version control diff algorithms")
    output.append("• Machine translation quality assessment")
    output.append("• Record linkage and data deduplication")
    output.append("• Speech recognition error correction")

    # Visual example of DP table construction
    output.append("\nDP TABLE VISUALIZATION (for 'cat' vs 'cut'):")
    word1, word2 = "cat", "cut"
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    # Print table header
    output.append("    " + "  ".join([" "] + list(word2)))
    output.append("  " + "+--" * (n + 1) + "+")

    # Print table rows
    for i in range(m + 1):
        row_label = " " if i == 0 else word1[i - 1]
        row_values = " ".join(f"{dp[i][j]:2}" for j in range(n + 1))
        output.append(f"{row_label} | {row_values} |")

    output.append(f"\nThe final answer is dp[{m}][{n}] = {dp[m][n]}")
    output.append("Operation: Replace 'a' with 'u' at position 1")

    output.append("\nALGORITHM VARIANTS:")
    output.append("• Weighted Edit Distance: Different costs for different operations")
    output.append(
        "• Longest Common Subsequence: Special case where only insertions/deletions allowed"
    )
    output.append("• Hamming Distance: Only substitutions allowed (equal length strings)")
    output.append("• Damerau-Levenshtein: Includes transposition as a fourth operation")

    return "\n".join(output)


# Test cases covering various scenarios
TEST_CASES = [
    TestCase(
        input_args=(
            "horse",
            "ros",
        ),
        expected=3,
        description="Classic example: horse -> ros",
    ),
    TestCase(
        input_args=(
            "intention",
            "execution",
        ),
        expected=5,
        description="Longer transformation",
    ),
    TestCase(
        input_args=(
            "",
            "abc",
        ),
        expected=3,
        description="Empty to non-empty string",
    ),
    TestCase(
        input_args=(
            "abc",
            "",
        ),
        expected=3,
        description="Non-empty to empty string",
    ),
    TestCase(
        input_args=(
            "",
            "",
        ),
        expected=0,
        description="Both strings empty",
    ),
    TestCase(
        input_args=(
            "abc",
            "abc",
        ),
        expected=0,
        description="Identical strings",
    ),
    TestCase(
        input_args=(
            "a",
            "b",
        ),
        expected=1,
        description="Single character replacement",
    ),
    TestCase(
        input_args=(
            "a",
            "ab",
        ),
        expected=1,
        description="Single character insertion",
    ),
    TestCase(
        input_args=(
            "ab",
            "a",
        ),
        expected=1,
        description="Single character deletion",
    ),
    TestCase(
        input_args=(
            "cat",
            "cut",
        ),
        expected=1,
        description="Single replacement: a->u",
    ),
    TestCase(
        input_args=(
            "sunday",
            "saturday",
        ),
        expected=3,
        description="Common prefix/suffix case",
    ),
    TestCase(
        input_args=(
            "kitten",
            "sitting",
        ),
        expected=3,
        description="Classic example: kitten -> sitting",
    ),
    TestCase(
        input_args=(
            "flaw",
            "lawn",
        ),
        expected=2,
        description="Multiple operations",
    ),
    TestCase(
        input_args=(
            "abc",
            "def",
        ),
        expected=3,
        description="No common characters",
    ),
    TestCase(
        input_args=(
            "programming",
            "contest",
        ),
        expected=9,
        description="Real-world example",
    ),
]


def test_solution():
    """Test the solution with various test cases."""
    solution = Solution()

    def test_function(word1: str, word2: str) -> int:
        # Test all approaches give same result
        result1 = solution.minDistance(word1, word2)
        result2 = solution.minDistance2D(word1, word2)
        result3 = solution.minDistanceRecursive(word1, word2)

        assert result1 == result2 == result3, (
            f"Inconsistent results: {result1}, {result2}, {result3}"
        )
        return result1

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="edit-distance",
    leetcode_num=72,
    title="Edit Distance",
    difficulty=Difficulty.HARD,
    category=Category.DP_2D,
    solution_func=Solution().minDistance,
    test_func=test_solution,
    demo_func=create_demo_output,
)
