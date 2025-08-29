"""
Spiral Matrix

Problem: Spiral Matrix
LeetCode link: https://leetcode.com/problems/spiral-matrix/
Description: Given an m x n matrix, return all elements of the matrix in spiral order.
"""


class Solution:
    def solve(self, *args) -> list[int]:
        """Return elements of matrix in spiral order."""
        matrix = args[0]
        res = []
        if not matrix or not matrix[0]:
            return res
        top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                res.append(matrix[top][j])
            top += 1
            for i in range(top, bottom + 1):
                res.append(matrix[i][right])
            right -= 1
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    res.append(matrix[bottom][j])
                bottom -= 1
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    res.append(matrix[i][left])
                left += 1
        return res


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="spiral_matrix",
#     title="Spiral Matrix",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
