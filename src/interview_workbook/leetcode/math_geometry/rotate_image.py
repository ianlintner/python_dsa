"""
LeetCode 48: Rotate Image

You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly.
DO NOT allocate another 2D matrix and do the rotation.

Time Complexity: O(n^2)
Space Complexity: O(1)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase
from .._types import Category, Difficulty


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Rotate matrix 90 degrees clockwise in-place.

        Approach: Two-step transformation
        1. Transpose the matrix (swap rows and columns)
        2. Reverse each row

        Example transformation for 3x3:
        [1,2,3]    [1,4,7]    [7,4,1]
        [4,5,6] -> [2,5,8] -> [8,5,2]
        [7,8,9]    [3,6,9]    [9,6,3]

        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)

        # Step 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i])
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()

    def rotate_layer_by_layer(self, matrix: List[List[int]]) -> None:
        """
        Alternative approach: Rotate layer by layer.

        Process the matrix from outside to inside, rotating each layer.
        For each layer, rotate 4 elements at a time.
        """
        n = len(matrix)

        # Process each layer (ring) from outside to inside
        for layer in range(n // 2):
            # For each element in the current layer
            for i in range(layer, n - layer - 1):
                # Store the top element
                temp = matrix[layer][i]

                # Move left to top
                matrix[layer][i] = matrix[n - 1 - i][layer]

                # Move bottom to left
                matrix[n - 1 - i][layer] = matrix[n - 1 - layer][n - 1 - i]

                # Move right to bottom
                matrix[n - 1 - layer][n - 1 - i] = matrix[i][n - 1 - layer]

                # Move temp (top) to right
                matrix[i][n - 1 - layer] = temp

    def rotate_with_extra_space(self, matrix: List[List[int]]) -> List[List[int]]:
        """
        Approach using extra space for comparison.

        Time Complexity: O(n^2)
        Space Complexity: O(n^2)
        """
        n = len(matrix)
        result = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                result[j][n - 1 - i] = matrix[i][j]

        return result


def matrix_to_string(matrix: List[List[int]]) -> str:
    """Helper function to display matrix nicely."""
    return "\n".join([str(row) for row in matrix])


# Test cases
TEST_CASES = [
    TestCase(
        name="Example 1 - 3x3 matrix",
        input_args=([[1, 2, 3], [4, 5, 6], [7, 8, 9]],),
        expected=[[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        description="3x3 matrix rotation",
    ),
    TestCase(
        name="Example 2 - 4x4 matrix",
        input_args=([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],),
        expected=[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]],
        description="4x4 matrix rotation",
    ),
    TestCase(
        name="Single element",
        input_args=([[1]],),
        expected=[[1]],
        description="1x1 matrix (no change)",
    ),
    TestCase(
        name="2x2 matrix",
        input_args=([[1, 2], [3, 4]],),
        expected=[[3, 1], [4, 2]],
        description="2x2 matrix rotation",
    ),
    TestCase(
        name="5x5 matrix",
        input_args=(
            [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15],
                [16, 17, 18, 19, 20],
                [21, 22, 23, 24, 25],
            ],
        ),
        expected=[
            [21, 16, 11, 6, 1],
            [22, 17, 12, 7, 2],
            [23, 18, 13, 8, 3],
            [24, 19, 14, 9, 4],
            [25, 20, 15, 10, 5],
        ],
        description="5x5 matrix rotation",
    ),
]


def create_demo_output():
    """Demonstrate different approaches to rotate matrix."""
    solution = Solution()

    print("=== LeetCode 48: Rotate Image ===\n")

    # Example with detailed explanation
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Original matrix:")
    print(matrix_to_string(matrix))
    print()

    # Show step-by-step transformation
    # Step 1: Transpose
    matrix_copy = [row[:] for row in matrix]  # Deep copy
    n = len(matrix_copy)

    print("Step 1: Transpose the matrix")
    for i in range(n):
        for j in range(i + 1, n):
            matrix_copy[i][j], matrix_copy[j][i] = matrix_copy[j][i], matrix_copy[i][j]

    print("After transpose:")
    print(matrix_to_string(matrix_copy))
    print()

    # Step 2: Reverse rows
    print("Step 2: Reverse each row")
    for i in range(n):
        matrix_copy[i].reverse()

    print("After reversing rows (final result):")
    print(matrix_to_string(matrix_copy))
    print()

    # Compare approaches
    print("=== Comparison of approaches ===")

    test_matrices = [[[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]]

    for i, test_matrix in enumerate(test_matrices, 1):
        print(f"\nTest {i}: {len(test_matrix)}x{len(test_matrix)} matrix")
        print("Original:")
        print(matrix_to_string(test_matrix))

        # Transpose + Reverse approach
        matrix1 = [row[:] for row in test_matrix]
        solution.rotate(matrix1)
        print("Transpose + Reverse result:")
        print(matrix_to_string(matrix1))

        # Layer by layer approach
        matrix2 = [row[:] for row in test_matrix]
        solution.rotate_layer_by_layer(matrix2)
        print("Layer by layer result:")
        print(matrix_to_string(matrix2))

        # Extra space approach (for comparison)
        matrix3 = solution.rotate_with_extra_space(test_matrix)
        print("Extra space result:")
        print(matrix_to_string(matrix3))

    return "\n".join(
        [
            "=== LeetCode 48: Rotate Image ===",
            "",
            "Original matrix:",
            matrix_to_string(matrix),
            "",
            "Step 1: Transpose the matrix",
            "After transpose:",
            matrix_to_string([[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
            "",
            "Step 2: Reverse each row",
            "After reversing rows (final result):",
            matrix_to_string(matrix_copy),
            "",
            "=== Comparison of approaches ===",
            f"All approaches produce the same result: {matrix_copy}",
        ]
    )


def test_solution():
    """Test function for the rotate image problem."""
    solution = Solution()

    for test_case in TEST_CASES:
        matrix = test_case.input_args[0]
        matrix_copy = [row[:] for row in matrix]
        solution.rotate(matrix_copy)

        if matrix_copy == test_case.expected:
            print(f"✓ {test_case.name}: PASS")
        else:
            print(f"✗ {test_case.name}: FAIL")
            print(f"  Expected: {test_case.expected}")
            print(f"  Got: {matrix_copy}")


if __name__ == "__main__":
    test_solution()


# Register the problem
register_problem(
    slug="rotate-image",
    leetcode_num=48,
    title="Rotate Image",
    difficulty=Difficulty.MEDIUM,
    category=Category.MATH_GEOMETRY,
    solution_func=lambda args: Solution().rotate(args),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["matrix", "simulation", "array"],
    notes="Rotate n x n matrix 90 degrees clockwise in-place using transpose + reverse rows approach",
)
