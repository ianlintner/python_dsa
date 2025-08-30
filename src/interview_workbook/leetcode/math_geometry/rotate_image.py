"""
Rotate Image

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> None:
        """Rotate the matrix 90 degrees clockwise in-place."""
        matrix = args[0]
        n = len(matrix)
        # transpose
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # reverse rows
        for row in matrix:
            row.reverse()
        return matrix


def demo():
    """TODO: Implement demo function."""
    pass


register_problem(
    id=48,
    slug="rotate_image",
    title="Rotate Image",
    category=Category.MATH_GEOMETRY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "math"],
    url="https://leetcode.com/problems/rotate-image/",
    notes="",
)
