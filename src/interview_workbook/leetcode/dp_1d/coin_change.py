"""
Coin Change

TODO: Add problem description
"""


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
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="coin_change",
#     title="Coin Change",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
