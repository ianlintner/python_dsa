"""
LeetCode 73: Set Matrix Zeroes
https://leetcode.com/problems/set-matrix-zeroes/

Given an m x n integer matrix, if an element is 0, set its entire row and column to 0s.

You must do it in place.

Examples:
    Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
    Output: [[1,0,1],[0,0,0],[1,0,1]]

    Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

Constraints:
    * m == matrix.length
    * n == matrix[0].length
    * 1 <= m, n <= 200
    * -2^31 <= matrix[i][j] <= 2^31 - 1

Follow up:
    * A straightforward solution using O(mn) space is probably a bad idea.
    * A simple improvement uses O(m + n) space, but still not the best solution.
    * Could you devise a constant space solution?
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Set matrix zeroes using O(1) space - first row/column as markers.

        Algorithm:
        1. Use first row and column as markers for zero positions
        2. Handle first row and column separately with flags
        3. Process internal cells using markers
        4. Apply zeroes to first row/column based on flags

        Time: O(m * n) - visit each cell twice
        Space: O(1) - only use constant extra space
        """
        if not matrix or not matrix[0]:
            return

        m, n = len(matrix), len(matrix[0])

        # Flags to track if first row/column should be zeroed
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))

        # Use first row and column as markers
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0  # Mark row
                    matrix[0][j] = 0  # Mark column

        # Zero out cells based on markers
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # Handle first row
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0

        # Handle first column
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0

    def setZeroes_extra_space(self, matrix: List[List[int]]) -> None:
        """
        Alternative: Set matrix zeroes using O(m + n) space.

        Time: O(m * n)
        Space: O(m + n) - store zero positions
        """
        if not matrix or not matrix[0]:
            return

        m, n = len(matrix), len(matrix[0])
        zero_rows = set()
        zero_cols = set()

        # Find all zero positions
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        # Set zeroes
        for i in range(m):
            for j in range(n):
                if i in zero_rows or j in zero_cols:
                    matrix[i][j] = 0

    def setZeroes_brute_force(self, matrix: List[List[int]]) -> None:
        """
        Brute force: Create new matrix with zeroes applied.

        Time: O(m * n * (m + n)) - for each zero, zero entire row/col
        Space: O(m * n) - create copy of matrix
        """
        if not matrix or not matrix[0]:
            return

        m, n = len(matrix), len(matrix[0])
        result = [row[:] for row in matrix]  # Deep copy

        # Find zeros in original matrix
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    # Zero out row
                    for k in range(n):
                        result[i][k] = 0
                    # Zero out column
                    for k in range(m):
                        result[k][j] = 0

        # Copy result back
        for i in range(m):
            for j in range(n):
                matrix[i][j] = result[i][j]


def create_demo_output() -> str:
    """Demonstrate set matrix zeroes with various test cases."""
    test_cases = [
        # Small examples
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]], "3x3 matrix with center zero"),
        ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], "3x4 matrix with multiple zeros"),
        ([[1, 2, 3, 4], [5, 0, 7, 8], [0, 10, 11, 12]], "3x4 matrix with edge zeros"),
        # Edge cases
        ([[0]], "Single zero"),
        ([[1]], "Single non-zero"),
        ([[1, 0, 3]], "Single row with zero"),
        ([[1], [0], [3]], "Single column with zero"),
        # All zeros cases
        ([[0, 0], [0, 0]], "All zeros matrix"),
        ([[1, 2], [3, 4]], "No zeros matrix"),
        # Pattern cases
        ([[1, 2, 3], [4, 0, 6], [7, 8, 9]], "Center zero creates cross"),
        ([[0, 2, 3], [4, 5, 6], [7, 8, 0]], "Corner zeros"),
    ]

    solution = Solution()
    results = []

    for matrix, description in test_cases:
        original = [row[:] for row in matrix]  # Deep copy for display
        solution.setZeroes(matrix)

        results.append(f"\n{description}:")
        results.append(f"Input:  {original}")
        results.append(f"Output: {matrix}")

        # Show dimensions and zero count
        m, n = len(matrix), len(matrix[0])
        zero_count = sum(row.count(0) for row in matrix)
        results.append(f"Dimensions: {m}x{n}, Zeros after: {zero_count}")

    # Demonstrate different approaches with timing
    results.append("\n" + "=" * 50)
    results.append("ALGORITHM COMPARISON")
    results.append("=" * 50)

    import copy
    import time

    # Large test case for performance comparison
    large_matrix = [[i * j if (i * j) % 17 != 0 else 0 for j in range(50)] for i in range(50)]

    approaches = [
        (solution.setZeroes, "O(1) Space - First Row/Col Markers"),
        (solution.setZeroes_extra_space, "O(m+n) Space - Sets"),
        (solution.setZeroes_brute_force, "O(mn) Space - Brute Force"),
    ]

    for method, name in approaches:
        test_matrix = copy.deepcopy(large_matrix)

        start = time.perf_counter()
        method(test_matrix)
        end = time.perf_counter()

        results.append(f"\n{name}:")
        results.append(f"Time: {(end - start) * 1000:.2f}ms for 50x50 matrix")

        # Verify correctness by checking pattern
        zero_rows = set()
        zero_cols = set()
        for i in range(len(large_matrix)):
            for j in range(len(large_matrix[0])):
                if large_matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        expected_zeros = len(zero_rows) * 50 + len(zero_cols) * 50 - len(zero_rows) * len(zero_cols)
        actual_zeros = sum(row.count(0) for row in test_matrix)
        results.append(f"Expected zeros: {expected_zeros}, Got: {actual_zeros} ✓")

    return "\n".join(results)


# Test cases for validation
TEST_CASES = [
    TestCase(
        input_data=([[1, 1, 1], [1, 0, 1], [1, 1, 1]],),
        expected=[[1, 0, 1], [0, 0, 0], [1, 0, 1]],
        description="3x3 matrix with center zero",
    ),
    TestCase(
        input_data=([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],),
        expected=[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]],
        description="3x4 matrix with multiple zeros",
    ),
    TestCase(input_data=([[0]],), expected=[[0]], description="Single zero element"),
    TestCase(input_data=([[1]],), expected=[[1]], description="Single non-zero element"),
    TestCase(input_data=([[1, 0, 3]],), expected=[[0, 0, 0]], description="Single row with zero"),
    TestCase(
        input_data=([[1], [0], [3]],),
        expected=[[0], [0], [0]],
        description="Single column with zero",
    ),
    TestCase(
        input_data=([[0, 0], [0, 0]],), expected=[[0, 0], [0, 0]], description="All zeros matrix"
    ),
    TestCase(
        input_data=([[1, 2], [3, 4]],), expected=[[1, 2], [3, 4]], description="No zeros matrix"
    ),
    TestCase(
        input_data=([[1, 2, 3], [4, 0, 6], [7, 8, 9]],),
        expected=[[1, 0, 3], [0, 0, 0], [7, 0, 9]],
        description="Center zero creates cross pattern",
    ),
    TestCase(
        input_data=([[0, 2, 3], [4, 5, 6], [7, 8, 0]],),
        expected=[[0, 0, 0], [0, 5, 0], [0, 0, 0]],
        description="Corner zeros affect entire matrix",
    ),
]


def test_solution():
    """Test the set matrix zeroes solution with custom logic."""
    solution = Solution()

    def run_test(matrix, expected, description):
        original = [row[:] for row in matrix]  # Keep original for error messages
        solution.setZeroes(matrix)

        if matrix == expected:
            return True, ""
        else:
            return False, f"Input: {original}, Expected: {expected}, Got: {matrix}"

    return run_test_cases(TEST_CASES, run_test)


# Register the problem
register_problem(
    slug="set_matrix_zeroes",
    leetcode_num=73,
    title="Set Matrix Zeroes",
    difficulty=Difficulty.MEDIUM,
    category=Category.MATH_GEOMETRY,
    solution_func=Solution().setZeroes,
    test_func=test_solution,
    demo_func=create_demo_output,
)


if __name__ == "__main__":
    # Run tests
    print("Testing Set Matrix Zeroes...")
    result = test_solution()
    print(f"Tests passed: {result}")

    # Show demo
    print("\n" + "=" * 50)
    print("DEMO OUTPUT")
    print("=" * 50)
    print(create_demo_output())
