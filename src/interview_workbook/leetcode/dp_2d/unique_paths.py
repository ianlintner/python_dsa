"""
Unique Paths

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


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
    """Run a demo for the Unique Paths problem."""
    solver = Solution()
    m, n = 3, 7
    result = solver.solve(m, n)
    return str(result)


register_problem(
    id=62,
    slug="unique_paths",
    title="Unique Paths",
    category=Category.DP_2D,
    difficulty=Difficulty.MEDIUM,
    tags=["math", "dynamic_programming", "combinatorics"],
    url="https://leetcode.com/problems/unique-paths/",
    notes="",
)
