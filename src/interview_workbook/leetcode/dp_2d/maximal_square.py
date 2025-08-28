"""
LeetCode 221: Maximal Square

Given an m x n binary matrix filled with 0's and 1's, find the largest square
containing only 1's and return its area.

Example:
    Input: matrix = [["1","0","1","0","0"],
                    ["1","0","1","1","1"],
                    ["1","1","1","1","1"],
                    ["1","0","0","1","0"]]
    Output: 4
    Explanation: The largest square has side length 2, so area = 2*2 = 4.

Constraints:
    - m == matrix.length
    - n == matrix[i].length
    - 1 <= m, n <= 300
    - matrix[i][j] is '0' or '1'.
"""

import time
from typing import List, Tuple

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        """
        Space-optimized 2D DP approach using 1D arrays.

        The key insight is that for each cell (i,j), if it's '1', the maximum
        square side length ending at that cell depends on:
        - The cell above: dp[j] (previous row, same column)
        - The cell to the left: dp[j-1] (current row, previous column)
        - The cell diagonally above-left: dp_prev (previous row, previous column)

        dp[j] = min(dp[j], dp[j-1], dp_prev) + 1 if matrix[i][j] == '1'

        Time: O(m * n), Space: O(n)
        """
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        dp = [0] * n  # Current row DP values
        max_side = 0
        dp_prev = 0  # Diagonal value from previous iteration

        for i in range(m):
            for j in range(n):
                temp = dp[j]  # Store current value before updating

                if matrix[i][j] == "1":
                    if i == 0 or j == 0:
                        # First row or first column
                        dp[j] = 1
                    else:
                        # Take minimum of three neighbors and add 1
                        dp[j] = min(dp[j], dp[j - 1], dp_prev) + 1

                    max_side = max(max_side, dp[j])
                else:
                    dp[j] = 0

                dp_prev = temp  # Update diagonal for next iteration

        return max_side * max_side

    def maximalSquare2D(self, matrix: List[List[str]]) -> int:
        """
        Standard 2D DP approach.

        dp[i][j] represents the side length of the largest square whose
        bottom-right corner is at (i,j).

        Base case: dp[i][0] = dp[0][j] = matrix[i][j] (first row/column)
        Recurrence:
        - If matrix[i][j] == '1': dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        - Else: dp[i][j] = 0

        Time: O(m * n), Space: O(m * n)
        """
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        dp = [[0] * n for _ in range(m)]
        max_side = 0

        # Fill first row
        for j in range(n):
            dp[0][j] = int(matrix[0][j])
            max_side = max(max_side, dp[0][j])

        # Fill first column
        for i in range(m):
            dp[i][0] = int(matrix[i][0])
            max_side = max(max_side, dp[i][0])

        # Fill the rest of the table
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == "1":
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    max_side = max(max_side, dp[i][j])
                else:
                    dp[i][j] = 0

        return max_side * max_side

    def maximalSquareBruteForce(self, matrix: List[List[str]]) -> int:
        """
        Brute force approach - check every possible square.

        For each cell that contains '1', try to expand the square as much as possible.

        Time: O(m * n * min(m,n)^2), Space: O(1)
        """
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        max_side = 0

        def isValidSquare(row: int, col: int, side: int) -> bool:
            """Check if a square of given side length starting at (row,col) contains all 1's"""
            if row + side > m or col + side > n:
                return False

            for i in range(row, row + side):
                for j in range(col, col + side):
                    if matrix[i][j] == "0":
                        return False
            return True

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == "1":
                    # Try expanding square from this position
                    side = 1
                    while isValidSquare(i, j, side):
                        max_side = max(max_side, side)
                        side += 1

        return max_side * max_side

    def maximalSquareWithPosition(self, matrix: List[List[str]]) -> Tuple[int, Tuple[int, int]]:
        """
        Extended version that returns both area and the bottom-right corner
        of the maximal square.

        Time: O(m * n), Space: O(m * n)
        """
        if not matrix or not matrix[0]:
            return 0, (-1, -1)

        m, n = len(matrix), len(matrix[0])
        dp = [[0] * n for _ in range(m)]
        max_side = 0
        max_pos = (-1, -1)

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == "1":
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

                    if dp[i][j] > max_side:
                        max_side = dp[i][j]
                        max_pos = (i, j)  # Bottom-right corner
                else:
                    dp[i][j] = 0

        return max_side * max_side, max_pos

    def maximalSquareHistogram(self, matrix: List[List[str]]) -> int:
        """
        Alternative approach using largest rectangle in histogram concept.

        For each row, maintain heights of consecutive 1's ending at that row.
        Then find the largest square that can be formed using histogram approach.

        Time: O(m * n), Space: O(n)
        """
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        max_area = 0

        def largestSquareInHistogram(heights: List[int]) -> int:
            """Find largest square area in histogram"""
            stack = []
            max_square = 0

            for i in range(len(heights) + 1):
                h = heights[i] if i < len(heights) else 0

                while stack and heights[stack[-1]] > h:
                    height = heights[stack.pop()]
                    width = i if not stack else i - stack[-1] - 1
                    # For square, side length is min of height and width
                    side = min(height, width)
                    max_square = max(max_square, side * side)

                stack.append(i)

            return max_square

        for i in range(m):
            # Update heights for current row
            for j in range(n):
                if matrix[i][j] == "1":
                    heights[j] += 1
                else:
                    heights[j] = 0

            # Find largest square in current histogram
            max_area = max(max_area, largestSquareInHistogram(heights))

        return max_area


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different maximal square scenarios.
    """
    solution = Solution()

    demo_cases = [
        (
            [
                ["1", "0", "1", "0", "0"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "0", "1", "0"],
            ],
            "Basic example from problem",
        ),
        ([["0", "1"], ["1", "0"]], "No square possible"),
        ([["0"]], "Single 0"),
        ([["1"]], "Single 1"),
        (
            [["1", "1", "1", "1"], ["1", "1", "1", "1"], ["1", "1", "1", "1"]],
            "Full rectangle of 1's",
        ),
        ([["1", "1", "0", "1"], ["1", "1", "0", "1"], ["1", "1", "1", "1"]], "Mixed pattern"),
        (
            [
                ["0", "0", "0", "1"],
                ["1", "1", "0", "1"],
                ["1", "1", "1", "1"],
                ["0", "1", "1", "1"],
                ["0", "1", "1", "1"],
            ],
            "Larger test case",
        ),
        ([["1", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]], "Hollow square pattern"),
    ]

    output = ["=== Maximal Square (LeetCode 221) ===\n"]

    output.append("ALGORITHM EXPLANATION:")
    output.append("The Maximal Square problem finds the largest square containing only 1's")
    output.append("in a binary matrix. This is solved using DP where for each cell, we")
    output.append("determine the largest square that can end at that position.\n")

    output.append("DP STATE DEFINITION:")
    output.append("dp[i][j] = side length of largest square with bottom-right corner at (i,j)")
    output.append("Base case: dp[i][0] = dp[0][j] = matrix[i][j] (first row/column)")
    output.append("Recurrence:")
    output.append(
        "  if matrix[i][j] == '1': dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1"
    )
    output.append("  else: dp[i][j] = 0\n")

    output.append("KEY INSIGHT:")
    output.append("For a square to exist at position (i,j), there must be squares of")
    output.append("side length (k-1) at positions (i-1,j), (i,j-1), and (i-1,j-1).")
    output.append("The minimum of these three determines the maximum square at (i,j).\n")

    for matrix, description in demo_cases:
        output.append(f"--- {description} ---")
        output.append(f"Matrix ({len(matrix)}x{len(matrix[0])}):")
        for row in matrix:
            output.append(f"  {row}")

        # Get results from different approaches
        result_optimized = solution.maximalSquare(matrix)
        result_2d = solution.maximalSquare2D(matrix)
        result_brute = solution.maximalSquareBruteForce(matrix)
        result_histogram = solution.maximalSquareHistogram(matrix)
        area, pos = solution.maximalSquareWithPosition(matrix)

        output.append(f"Maximal square area: {result_optimized}")

        if area > 0:
            side_length = int(area**0.5)
            output.append(f"Square side length: {side_length}")
            if pos != (-1, -1):
                top_left_row = pos[0] - side_length + 1
                top_left_col = pos[1] - side_length + 1
                output.append(
                    f"Square position: top-left ({top_left_row},{top_left_col}), bottom-right {pos}"
                )

        # Verify all approaches give same result
        assert result_optimized == result_2d == result_brute == result_histogram == area
        output.append("")

    # Performance comparison
    output.append("PERFORMANCE COMPARISON:")
    # Create a challenging test case - large matrix with mixed patterns
    test_matrix = []
    size = 50
    for i in range(size):
        row = []
        for j in range(size):
            # Create a pattern with some squares
            if (i // 5 + j // 5) % 2 == 0:
                row.append("1")
            else:
                row.append("0" if (i + j) % 3 == 0 else "1")
        test_matrix.append(row)

    methods = [
        ("Space-optimized DP", solution.maximalSquare),
        ("Standard 2D DP", solution.maximalSquare2D),
        ("Histogram approach", solution.maximalSquareHistogram),
    ]

    for name, method in methods:
        start_time = time.perf_counter()
        result = method(test_matrix)
        end_time = time.perf_counter()

        output.append(
            f"{name:20} | Result: {result:3} | Time: {(end_time - start_time) * 1000:.3f}ms"
        )

    # Note: Brute force is too slow for large matrices, so we skip it

    output.append("\nSPACE COMPLEXITY ANALYSIS:")
    output.append("• Space-optimized DP: O(n) - only need one row")
    output.append("• Standard 2D DP: O(m*n) - full DP table")
    output.append("• Histogram approach: O(n) - height array and stack")
    output.append("• Brute force: O(1) - constant extra space")

    output.append("\nREAL-WORLD APPLICATIONS:")
    output.append("• Image processing: finding largest uniform regions")
    output.append("• Circuit design: optimizing chip layout and space utilization")
    output.append("• Game development: collision detection and area optimization")
    output.append("• Data compression: identifying repetitive patterns")
    output.append("• Warehouse management: optimal storage space allocation")
    output.append("• Computer graphics: texture mapping and sprite optimization")
    output.append("• Agricultural planning: field layout optimization")

    # Visual example of DP progression
    output.append("\nDP PROGRESSION EXAMPLE:")
    example_matrix = [
        ["1", "0", "1", "0"],
        ["1", "0", "1", "1"],
        ["1", "1", "1", "1"],
        ["0", "1", "1", "1"],
    ]

    m, n = len(example_matrix), len(example_matrix[0])
    dp = [[0] * n for _ in range(m)]

    output.append("Original matrix:")
    for row in example_matrix:
        output.append(f"  {' '.join(row)}")

    output.append("\nDP table (side lengths):")

    # Fill DP table step by step
    for i in range(m):
        for j in range(n):
            if example_matrix[i][j] == "1":
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
            else:
                dp[i][j] = 0

    for row in dp:
        output.append(f"  {' '.join(str(x) for x in row)}")

    max_side = max(max(row) for row in dp)
    output.append(f"\nMaximum side length: {max_side}")
    output.append(f"Maximal square area: {max_side * max_side}")

    output.append("\nALGORITHM VARIANTS:")
    output.append("• Maximal Rectangle: Find largest rectangle (not necessarily square)")
    output.append("• Count Squares: Count all possible squares in matrix")
    output.append("• Maximal Square with K 0's: Allow at most K zeros in the square")
    output.append("• Maximal Square in 3D: Extend to 3D matrices (cubes)")

    return "\n".join(output)


# Test cases covering various scenarios
TEST_CASES = [
    TestCase(
        input_data=(
            [
                ["1", "0", "1", "0", "0"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "0", "1", "0"],
            ]
        ),
        expected=4,
        description="Basic example - 2x2 square",
    ),
    TestCase(
        input_data=([["0", "1"], ["1", "0"]]), expected=1, description="No square larger than 1x1"
    ),
    TestCase(input_data=([["0"]]), expected=0, description="Single 0"),
    TestCase(input_data=([["1"]]), expected=1, description="Single 1"),
    TestCase(
        input_data=([["1", "1", "1", "1"], ["1", "1", "1", "1"], ["1", "1", "1", "1"]]),
        expected=9,
        description="3x3 square in 3x4 matrix",
    ),
    TestCase(input_data=([["1", "1"], ["1", "1"]]), expected=4, description="Perfect 2x2 square"),
    TestCase(
        input_data=([["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]),
        expected=0,
        description="All zeros",
    ),
    TestCase(
        input_data=([["1", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]]),
        expected=1,
        description="Hollow pattern - no large square",
    ),
    TestCase(
        input_data=([["1", "1", "0", "1"], ["1", "1", "0", "1"], ["1", "1", "1", "1"]]),
        expected=4,
        description="2x2 square with obstacles",
    ),
    TestCase(
        input_data=(
            [
                ["1", "0", "1", "1", "1"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "1", "1", "0"],
            ]
        ),
        expected=9,
        description="3x3 square possible",
    ),
    TestCase(
        input_data=(
            [
                ["1", "1", "1", "1", "1", "1", "1", "1"],
                ["1", "1", "1", "1", "1", "1", "1", "0"],
                ["1", "1", "1", "1", "1", "1", "1", "0"],
                ["1", "1", "1", "1", "1", "0", "0", "0"],
                ["0", "1", "1", "1", "1", "0", "0", "0"],
            ]
        ),
        expected=16,
        description="4x4 square in larger matrix",
    ),
]


def test_solution():
    """Test the solution with various test cases."""
    solution = Solution()

    def test_function(matrix: List[List[str]]) -> int:
        # Test multiple approaches give same result
        result1 = solution.maximalSquare(matrix)
        result2 = solution.maximalSquare2D(matrix)
        result3 = solution.maximalSquareHistogram(matrix)

        # Only test brute force on small matrices (to avoid timeout)
        if len(matrix) <= 10 and len(matrix[0]) <= 10:
            result4 = solution.maximalSquareBruteForce(matrix)
            assert result1 == result2 == result3 == result4, (
                f"Inconsistent results: {result1}, {result2}, {result3}, {result4}"
            )
        else:
            assert result1 == result2 == result3, (
                f"Inconsistent results: {result1}, {result2}, {result3}"
            )

        return result1

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="maximal-square",
    leetcode_num=221,
    title="Maximal Square",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_2D,
    solution_func=Solution().maximalSquare,
    test_func=test_solution,
    demo_func=create_demo_output,
)
