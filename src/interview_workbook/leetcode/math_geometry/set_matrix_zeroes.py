"""
Set Matrix Zeroes

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> None:
        """Set matrix zeroes in-place with O(1) space."""
        matrix = args[0]
        rows, cols = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][j] == 0 for j in range(cols))
        first_col_zero = any(matrix[i][0] == 0 for i in range(rows))

        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_zero:
            for j in range(cols):
                matrix[0][j] = 0

        if first_col_zero:
            for i in range(rows):
                matrix[i][0] = 0

        return matrix


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=73,
    slug="set_matrix_zeroes",
    title="Set Matrix Zeroes",
    category=Category.MATH_GEOMETRY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hashmap"],
    url="https://leetcode.com/problems/set-matrix-zeroes/",
    notes="",
)
