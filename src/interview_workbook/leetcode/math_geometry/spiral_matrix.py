"""
LeetCode 54: Spiral Matrix

Given an m x n matrix, return all elements of the matrix in spiral order.

Time Complexity: O(m * n)
Space Complexity: O(1) - excluding the output array
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Traverse matrix in spiral order using boundary approach.

        Algorithm:
        1. Define four boundaries: top, bottom, left, right
        2. Move in spiral order: right -> down -> left -> up
        3. After each direction, adjust the corresponding boundary
        4. Continue until all elements are visited
        """
        if not matrix or not matrix[0]:
            return []

        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # Move right along top row
            for j in range(left, right + 1):
                result.append(matrix[top][j])
            top += 1

            # Move down along right column
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1

            # Move left along bottom row (if we still have rows)
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    result.append(matrix[bottom][j])
                bottom -= 1

            # Move up along left column (if we still have columns)
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    result.append(matrix[i][left])
                left += 1

        return result

    def spiralOrder_simulation(self, matrix: List[List[int]]) -> List[int]:
        """
        Alternative approach using direction simulation.

        Simulate the spiral movement by tracking current position
        and changing direction when hitting boundaries or visited cells.
        """
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        visited = [[False] * n for _ in range(m)]

        # Directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction_idx = 0

        row, col = 0, 0

        for _ in range(m * n):
            result.append(matrix[row][col])
            visited[row][col] = True

            # Calculate next position
            next_row = row + directions[direction_idx][0]
            next_col = col + directions[direction_idx][1]

            # Check if we need to change direction
            if (
                next_row < 0
                or next_row >= m
                or next_col < 0
                or next_col >= n
                or visited[next_row][next_col]
            ):
                # Change direction (turn right)
                direction_idx = (direction_idx + 1) % 4
                next_row = row + directions[direction_idx][0]
                next_col = col + directions[direction_idx][1]

            row, col = next_row, next_col

        return result


# Test cases
TEST_CASES = [
    TestCase(
        name="Example 1 - 3x4 matrix",
        input_args=([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],),
        expected=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
        description="3x4 rectangular matrix",
    ),
    TestCase(
        name="Example 2 - 3x3 matrix",
        input_args=([[1, 2, 3], [4, 5, 6], [7, 8, 9]],),
        expected=[1, 2, 3, 6, 9, 8, 7, 4, 5],
        description="3x3 square matrix",
    ),
    TestCase(
        name="Single row",
        input_args=([[1, 2, 3, 4]],),
        expected=[1, 2, 3, 4],
        description="Single row matrix",
    ),
    TestCase(
        name="Single column",
        input_args=([[1], [2], [3], [4]],),
        expected=[1, 2, 3, 4],
        description="Single column matrix",
    ),
    TestCase(
        name="Single element",
        input_args=([[5]],),
        expected=[5],
        description="Single element matrix",
    ),
    TestCase(
        name="2x2 matrix",
        input_args=([[1, 2], [3, 4]],),
        expected=[1, 2, 4, 3],
        description="2x2 square matrix",
    ),
    TestCase(
        name="Tall matrix",
        input_args=([[1, 2], [3, 4], [5, 6], [7, 8]],),
        expected=[1, 2, 4, 6, 8, 7, 5, 3],
        description="4x2 tall matrix",
    ),
    TestCase(
        name="Wide matrix",
        input_args=([[1, 2, 3, 4, 5]],),
        expected=[1, 2, 3, 4, 5],
        description="1x5 wide matrix",
    ),
]


def create_demo_output():
    """Demonstrate spiral matrix traversal."""
    solution = Solution()

    print("=== LeetCode 54: Spiral Matrix ===\n")

    # Example with detailed explanation
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    print("Input matrix:")
    for row in matrix:
        print(f"  {row}")
    print()

    result = solution.spiralOrder(matrix)
    print(f"Spiral order: {result}")
    print()

    # Show step-by-step traversal
    print("Step-by-step traversal:")
    m, n = len(matrix), len(matrix[0])
    top, bottom, left, right = 0, m - 1, 0, n - 1
    step = 1

    while top <= bottom and left <= right:
        print(f"Step {step}: Move right from ({top}, {left}) to ({top}, {right})")
        elements = [matrix[top][j] for j in range(left, right + 1)]
        print(f"  Elements: {elements}")
        top += 1
        step += 1

        if top > bottom:
            break

        print(f"Step {step}: Move down from ({top}, {right}) to ({bottom}, {right})")
        elements = [matrix[i][right] for i in range(top, bottom + 1)]
        print(f"  Elements: {elements}")
        right -= 1
        step += 1

        if left > right:
            break

        print(f"Step {step}: Move left from ({bottom}, {right}) to ({bottom}, {left})")
        elements = [matrix[bottom][j] for j in range(right, left - 1, -1)]
        print(f"  Elements: {elements}")
        bottom -= 1
        step += 1

        if top > bottom:
            break

        print(f"Step {step}: Move up from ({bottom}, {left}) to ({top}, {left})")
        elements = [matrix[i][left] for i in range(bottom, top - 1, -1)]
        print(f"  Elements: {elements}")
        left += 1
        step += 1

    print()

    # Compare approaches
    print("=== Comparison of approaches ===")

    test_matrices = [[[1, 2, 3], [4, 5, 6]], [[1, 2], [3, 4], [5, 6]]]

    for i, test_matrix in enumerate(test_matrices, 1):
        print(f"\nTest {i}: {len(test_matrix)}x{len(test_matrix[0])} matrix")
        for row in test_matrix:
            print(f"  {row}")

        result1 = solution.spiralOrder(test_matrix)
        result2 = solution.spiralOrder_simulation(test_matrix)

        print(f"Boundary approach: {result1}")
        print(f"Simulation approach: {result2}")

    # Visualize spiral path
    print("\n=== Spiral Path Visualization ===")
    matrix_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Matrix:")
    for row in matrix_3x3:
        print(f"  {row}")

    print("\nSpiral path:")
    print("  1 → 2 → 3")
    print("          ↓")
    print("  4   5   6")
    print("  ↑       ↓")
    print("  7 ← 8 ← 9")

    result_3x3 = solution.spiralOrder(matrix_3x3)
    print(f"Result: {result_3x3}")

    return create_demo_output(
        title="Spiral Matrix",
        description="Traverse matrix in spiral order",
        input_data={"matrix": matrix},
        expected_output=result,
    )


def test_solution():
    """Test function for the spiral matrix problem."""
    solution = Solution()
    
    for test_case in TEST_CASES:
        matrix = test_case.input_args[0]
        result = solution.spiralOrder(matrix)
        
        if result == test_case.expected:
            print(f"✓ {test_case.name}: PASS")
        else:
            print(f"✗ {test_case.name}: FAIL")
            print(f"  Expected: {test_case.expected}")
            print(f"  Got: {result}")


if __name__ == "__main__":
    test_solution()


# Register the problem
register_problem(
    slug="spiral-matrix",
    leetcode_num=54,
    title="Spiral Matrix",
    difficulty=Difficulty.MEDIUM,
    category=Category.MATH_GEOMETRY,
    solution_func=lambda args: Solution().spiralOrder(args),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["matrix", "simulation", "array"],
    notes="Traverse matrix in spiral order using boundary tracking approach",
)
