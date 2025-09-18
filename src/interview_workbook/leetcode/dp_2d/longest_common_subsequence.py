"""
Longest Common Subsequence

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Compute length of Longest Common Subsequence."""
        if len(args) != 2:
            return ""
        text1, text2 = args
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]


def demo():
    """Run a demo for the Longest Common Subsequence problem."""
    solver = Solution()
    text1 = "abcde"
    text2 = "ace"
    print(f"Input: {text1}, {text2}")
    result = solver.solve(text1, text2)
    print(f"Output: {result}")
    return str(result)


register_problem(
    id=1143,
    slug="longest_common_subsequence",
    title="Longest Common Subsequence",
    category=Category.DP_2D,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "dynamic_programming"],
    url="https://leetcode.com/problems/longest-common-subsequence/",
    notes="",
)
