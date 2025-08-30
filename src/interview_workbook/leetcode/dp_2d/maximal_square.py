"""
Maximal Square

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Return area of largest square of '1's in a binary matrix."""
        if len(args) != 1:
            return ""
        matrix = args[0]
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0])
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_side = 0

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if matrix[i - 1][j - 1] == "1" or matrix[i - 1][j - 1] == 1:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    max_side = max(max_side, dp[i][j])
        return max_side * max_side


def demo():
    """Run a demo for the Maximal Square problem."""
    solver = Solution()
    matrix = [
        ["1","0","1","0","0"],
        ["1","0","1","1","1"],
        ["1","1","1","1","1"],
        ["1","0","0","1","0"],
    ]
    result = solver.solve(matrix)
    return str(result)


register_problem(
    id=221,
    slug="maximal_square",
    title="Maximal Square",
    category=Category.DP_2D,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming"],
    url="https://leetcode.com/problems/maximal-square/",
    notes="",
)
