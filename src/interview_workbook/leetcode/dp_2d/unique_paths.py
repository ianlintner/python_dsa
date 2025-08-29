"""
Unique Paths

TODO: Add problem description
"""


class Solution:
    def solve(self, *args) -> int:
        """Return number of unique paths in m x n grid (only right/down moves)."""
        if len(args) != 2:
            return ""
        m, n = args
        dp = [[1] * n for _ in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[m - 1][n - 1]


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="unique_paths",
#     title="Unique Paths",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
