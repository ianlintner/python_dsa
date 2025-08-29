"""
Rotate Image

TODO: Add problem description
"""


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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="rotate_image",
#     title="Rotate Image",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
