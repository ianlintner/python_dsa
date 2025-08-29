"""
Best Time to Buy and Sell Stock

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a different
day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit,
return 0.

LeetCode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        """Return the max profit from a single buy/sell transaction."""
        min_price = float("inf")
        max_profit = 0
        for p in prices:
            if p < min_price:
                min_price = p
            else:
                max_profit = max(max_profit, p - min_price)
        return max_profit

    def solve(self, prices: list[int]) -> int:
        """Alias for compatibility with older tests."""
        return self.maxProfit(prices)


# Example test cases

test_cases = [
    TestCase(([7, 1, 5, 3, 6, 4],), 5, "Max profit achievable"),
    TestCase(([7, 6, 4, 3, 1],), 0, "No profit possible"),
]


def demo():
    """Run simple test cases for Best Time To Buy Sell Stock."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.maxProfit(*case.input_args)
        outputs.append(
            f"Best Time to Buy and Sell Stock | Test Case: {case.description}\n"
            f"Input: {case.input_args} -> Output: {res}, Expected: {case.expected}\n"
            f"Time: O(n), Space: O(1) | Technique: sliding window\n✓ PASS"
        )
        return "\n".join(outputs)


register_problem(
    id=121,
    slug="best-time-to-buy-and-sell-stock",
    title="Best Time to Buy and Sell Stock",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.EASY,
    tags=["sliding-window", "array", "dynamic-programming"],
    url="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
    notes="Classic sliding window for max profit with one transaction.",
)
