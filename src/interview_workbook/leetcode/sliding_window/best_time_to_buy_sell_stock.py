"""
LeetCode 121: Best Time to Buy and Sell Stock

You are given an array `prices` where `prices[i]` is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing
a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve
any profit, return 0.

URL: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Difficulty: Easy
Category: Sliding Window

Patterns:
- Sliding window / two pointers
- Tracking minimum and maximum difference
- Dynamic programming (can also be solved with DP)
- Kadane's algorithm variant

Complexity:
- Time: O(n) - single pass through array
- Space: O(1) - only using constant extra variables

Pitfalls:
- Must buy before selling (can't sell then buy)
- Can only complete one transaction
- Profit cannot be negative (return 0 if no profit)
- Handle edge cases: empty array, single price

Follow-ups:
- What if you can make multiple transactions? (Best Time to Buy and Sell Stock II)
- What if you can make at most k transactions? (Best Time to Buy and Sell Stock IV)
- What if you have a cooldown period? (Best Time to Buy and Sell Stock with Cooldown)
- What if you have transaction fees?
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, run_test_cases, create_demo_output
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        """
        Find maximum profit from single buy-sell transaction.

        Args:
            prices: List of stock prices by day

        Returns:
            Maximum profit achievable, or 0 if no profit possible
        """
        if not prices or len(prices) < 2:
            return 0

        min_price = prices[0]  # Track minimum price seen so far
        max_profit = 0  # Track maximum profit achievable

        for price in prices[1:]:
            # Calculate profit if we sell today
            profit = price - min_price

            # Update maximum profit
            max_profit = max(max_profit, profit)

            # Update minimum price for future transactions
            min_price = min(min_price, price)

        return max_profit

    def maxProfitAlternative(self, prices: list[int]) -> int:
        """
        Alternative implementation using explicit buy/sell day tracking.
        Same time/space complexity, more explicit about the window.
        """
        if not prices or len(prices) < 2:
            return 0

        max_profit = 0
        buy_day = 0  # Index of best day to buy so far

        for sell_day in range(1, len(prices)):
            # Calculate profit for current sell day
            profit = prices[sell_day] - prices[buy_day]
            max_profit = max(max_profit, profit)

            # Update buy day if we found a lower price
            if prices[sell_day] < prices[buy_day]:
                buy_day = sell_day

        return max_profit


# Test cases
test_cases = [
    TestCase(([7, 1, 5, 3, 6, 4],), 5, "Buy at 1, sell at 6"),
    TestCase(([7, 6, 4, 3, 1],), 0, "Prices only decrease"),
    TestCase(([1, 2],), 1, "Simple profit case"),
    TestCase(([2, 1, 2, 1, 0, 1, 2],), 2, "Multiple opportunities, best is 0->2"),
    TestCase(([1],), 0, "Single price"),
    TestCase(([],), 0, "Empty array"),
    TestCase(([5, 5, 5, 5],), 0, "All prices same"),
    TestCase(([1, 2, 3, 4, 5],), 4, "Steadily increasing"),
    TestCase(([2, 4, 1],), 2, "Peak in middle"),
    TestCase(([3, 2, 6, 5, 0, 3],), 4, "Buy at 2, sell at 6"),
]


def demo() -> str:
    """Run Best Time to Buy and Sell Stock demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.maxProfit, test_cases, "LeetCode 121: Best Time to Buy and Sell Stock"
    )

    return create_demo_output(
        "Best Time to Buy and Sell Stock",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. We need to find maximum difference where larger element comes after smaller
2. Track minimum price seen so far as potential buy point
3. For each day, calculate profit if selling today vs min price seen
4. This is a variant of sliding window where window represents buy->sell period

Connection to sliding window:
- The "window" is from min_price_day to current_day
- We expand the window by moving right pointer (current day)
- We contract/reset when we find a new minimum (better buy opportunity)

Alternative approaches:
1. Brute force O(n²): Try all pairs, but inefficient
2. Dynamic programming: dp[i] = max profit ending at day i
3. Kadane's algorithm variant: Transform to max subarray problem
        """.strip(),
    )


# Register the problem
register_problem(
    id=121,
    slug="best_time_to_buy_sell_stock",
    title="Best Time to Buy and Sell Stock",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.EASY,
    tags=["array", "sliding_window", "dynamic_programming"],
    url="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
    notes="Classic sliding window problem disguised as stock trading; demonstrates min/max tracking pattern",
)
