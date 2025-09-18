"""
Coin Change

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Return the fewest coins needed to make up the amount or -1 if not possible."""
        if len(args) != 2:
            return -1
        coins, amount = args
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] != amount + 1 else -1


def demo():
    """Run a demo for the Coin Change problem."""
    solver = Solution()
    coins = [1, 2, 5]
    amount = 11
    result = solver.solve(coins, amount)
    print(f"Coins: {coins}, Amount: {amount}")
    print(f"Final result: {result}")
    return str(result)


register_problem(
    id=322,
    slug="coin_change",
    title="Coin Change",
    category=Category.DP_1D,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming", "bfs"],
    url="https://leetcode.com/problems/coin-change/",
    notes="",
)
