"""
LeetCode 322: Coin Change

You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Time Complexity: O(n * amount)
Space Complexity: O(amount)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Dynamic programming approach using bottom-up tabulation.

        For each amount from 1 to target amount, we try each coin and take
        the minimum number of coins needed.

        dp[i] = minimum coins needed to make amount i
        dp[i] = min(dp[i-coin] + 1) for all valid coins

        Time: O(n * amount) - For each amount, try all coins
        Space: O(amount) - DP array of size amount + 1
        """
        if amount == 0:
            return 0

        # Initialize DP array with impossible value (amount + 1)
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins needed to make amount 0

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != amount + 1 else -1

    def coinChangeRecursive(self, coins: List[int], amount: int) -> int:
        """
        Recursive approach with memoization (top-down DP).

        This approach is more intuitive but less efficient due to
        function call overhead.

        Time: O(n * amount) - Each subproblem solved once
        Space: O(amount) - Recursion stack + memoization
        """
        if amount == 0:
            return 0

        memo = {}

        def dp(remaining):
            if remaining == 0:
                return 0
            if remaining < 0:
                return float("inf")
            if remaining in memo:
                return memo[remaining]

            result = float("inf")
            for coin in coins:
                result = min(result, dp(remaining - coin) + 1)

            memo[remaining] = result
            return result

        result = dp(amount)
        return result if result != float("inf") else -1

    def coinChangeBFS(self, coins: List[int], amount: int) -> int:
        """
        BFS approach: treat as shortest path problem.

        Each amount is a node, each coin denomination is an edge.
        Find shortest path from amount to 0.

        Time: O(n * amount) - In worst case, visit all amounts
        Space: O(amount) - Queue and visited set
        """
        if amount == 0:
            return 0

        from collections import deque

        queue = deque([amount])
        visited = {amount}
        level = 0

        while queue:
            level += 1
            for _ in range(len(queue)):
                current = queue.popleft()

                for coin in coins:
                    next_amount = current - coin
                    if next_amount == 0:
                        return level
                    if next_amount > 0 and next_amount not in visited:
                        visited.add(next_amount)
                        queue.append(next_amount)

        return -1

    def coinChangeGreedy(self, coins: List[int], amount: int) -> int:
        """
        Greedy approach: use largest coins first.

        This works only for certain coin systems (like standard currency)
        but fails for arbitrary coin sets. Included for educational purposes.

        Time: O(n log n + amount/min_coin) - Sorting + greedy selection
        Space: O(1) - No extra space needed
        """
        if amount == 0:
            return 0

        coins.sort(reverse=True)  # Use largest coins first
        count = 0

        for coin in coins:
            if amount >= coin:
                num_coins = amount // coin
                count += num_coins
                amount -= num_coins * coin

        return count if amount == 0 else -1


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different coin change scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        ([1, 3, 4], 6, 2),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 2, 5], 11, 3),
        ([1, 4, 5], 8, 2),
        ([1, 3, 4], 6, 2),
        ([2, 5, 10, 1], 27, 4),
    ]

    for coins, amount, _expected in test_cases:
        result = solution.coinChange(coins, amount)
        demos.append(f"Coins: {coins}, Amount: {amount}")
        demos.append(f"Minimum coins: {result}")

        # Show DP table construction for smaller examples
        if amount <= 12 and len(coins) <= 4:
            demos.append("DP table construction:")
            dp = [amount + 1] * (amount + 1)
            dp[0] = 0

            for i in range(1, amount + 1):
                for coin in coins:
                    if coin <= i:
                        dp[i] = min(dp[i], dp[i - coin] + 1)

                if dp[i] == amount + 1:
                    demos.append(f"  dp[{i}] = impossible")
                else:
                    demos.append(f"  dp[{i}] = {dp[i]}")

            if result != -1:
                # Show optimal solution reconstruction
                demos.append("Optimal coin selection:")
                current_amount = amount
                coin_count = {}

                while current_amount > 0:
                    for coin in coins:
                        if (
                            coin <= current_amount
                            and dp[current_amount - coin] == dp[current_amount] - 1
                        ):
                            coin_count[coin] = coin_count.get(coin, 0) + 1
                            current_amount -= coin
                            break

                for coin, count in sorted(coin_count.items()):
                    demos.append(f"  Use {count}x coin of value {coin}")

        demos.append("")

    # Algorithm comparison
    demos.append("=== Algorithm Analysis ===")
    demos.append("Dynamic Programming Approach:")
    demos.append("- Bottom-up: build solutions for smaller amounts first")
    demos.append("- For each amount, try all coins and take minimum")
    demos.append("- Recurrence: dp[i] = min(dp[i-coin] + 1) for all valid coins")
    demos.append("- Base case: dp[0] = 0 (0 coins needed for amount 0)")
    demos.append("")

    demos.append("Why Greedy Fails:")
    demos.append("- Greedy: always use largest coin possible")
    demos.append("- Example: coins=[1,3,4], amount=6")
    demos.append("  - Greedy: 4+1+1 = 3 coins")
    demos.append("  - Optimal: 3+3 = 2 coins")
    demos.append("- Greedy works only for canonical coin systems")
    demos.append("")

    # Show greedy failure example
    demos.append("=== Greedy vs DP Comparison ===")
    comparison_cases = [
        ([1, 3, 4], 6),
        ([1, 5, 10, 21, 25], 63),
        ([1, 4, 5], 8),
    ]

    for coins, amount in comparison_cases:
        dp_result = solution.coinChange(coins, amount)
        # Note: greedy might modify coins array, so use copy
        greedy_result = solution.coinChangeGreedy(coins.copy(), amount)

        demos.append(f"Coins: {coins}, Amount: {amount}")
        demos.append(f"DP result: {dp_result}")
        demos.append(f"Greedy result: {greedy_result}")
        if dp_result != greedy_result and greedy_result != -1:
            demos.append("  → Greedy gives suboptimal result!")
        elif greedy_result == -1 and dp_result != -1:
            demos.append("  → Greedy fails to find solution!")
        else:
            demos.append("  → Both methods agree")
        demos.append("")

    # Performance comparison
    import time

    large_coins = [1, 5, 10, 25]
    large_amount = 1000

    # Time DP approach
    start_time = time.time()
    for _ in range(100):
        solution.coinChange(large_coins, large_amount)
    dp_time = time.time() - start_time

    # Time recursive approach
    start_time = time.time()
    for _ in range(100):
        solution.coinChangeRecursive(large_coins, large_amount)
    recursive_time = time.time() - start_time

    # Time BFS approach
    start_time = time.time()
    for _ in range(10):
        solution.coinChangeBFS(large_coins, large_amount)
    bfs_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"DP iterative (100 runs): {dp_time:.6f}s")
    demos.append(f"DP recursive (100 runs): {recursive_time:.6f}s")
    demos.append(f"BFS approach (10 runs): {bfs_time:.6f}s")
    demos.append("")
    demos.append("DP iterative: O(n*amount) time, O(amount) space")
    demos.append("DP recursive: O(n*amount) time, O(amount) space + call overhead")
    demos.append("BFS: O(n*amount) time, O(amount) space")
    demos.append("")

    # Edge cases and considerations
    demos.append("=== Edge Cases ===")
    demos.append("- Amount = 0: return 0 (no coins needed)")
    demos.append("- No solution exists: return -1")
    demos.append("- Single coin type: division-based solution possible")
    demos.append("- Large amounts: DP table can be memory-intensive")
    demos.append("- Coin value > amount: coin is ignored")
    demos.append("")

    # Optimization techniques
    demos.append("=== Optimization Techniques ===")
    demos.append("1. Early termination: if dp[amount] is already minimal")
    demos.append("2. Space optimization: only need previous row for 2D version")
    demos.append("3. Coin sorting: process larger coins first for pruning")
    demos.append("4. BFS with pruning: stop when first solution found")
    demos.append("5. Mathematical optimization for specific coin sets")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Currency exchange: minimize number of bills/coins")
    demos.append("- Resource allocation: minimize number of resource units")
    demos.append("- Packet transmission: optimal packet size selection")
    demos.append("- Inventory management: minimize number of containers")
    demos.append("- Change-making algorithms in point-of-sale systems")
    demos.append("- Knapsack-type optimization problems")
    demos.append("- Game theory: optimal move selection with costs")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(
        input_args=([1, 3, 4], 6), expected=2, description="Use coins 3+3 for optimal solution"
    ),
    TestCase(
        input_args=([2], 3), expected=-1, description="Impossible to make odd amount with even coin"
    ),
    TestCase(input_args=([1], 0), expected=0, description="Zero amount needs zero coins"),
    TestCase(input_args=([1, 2, 5], 11), expected=3, description="Standard coin change example"),
    TestCase(input_args=([1, 4, 5], 8), expected=2, description="Use coins 4+4 instead of 5+1+1+1"),
    TestCase(input_args=([2, 5, 10, 1], 27), expected=4, description="Optimal: 10+10+5+2"),
    TestCase(input_args=([1], 1), expected=1, description="Single coin, single amount"),
    TestCase(
        input_args=([1, 3, 4], 0), expected=0, description="Zero amount with multiple coin types"
    ),
    TestCase(input_args=([5, 10, 25], 30), expected=2, description="Use coins 25+5"),
    TestCase(input_args=([1, 5, 10, 25], 67), expected=6, description="Greedy optimal case"),
]


def test_solution():
    """Test the coin change solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.coinChange, TEST_CASES)


# Register the problem
register_problem(
    slug="coin_change",
    leetcode_num=322,
    title="Coin Change",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_1D,
    solution_func=Solution().coinChange,
    test_func=test_solution,
    demo_func=create_demo_output,
)
