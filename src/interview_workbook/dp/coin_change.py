def coin_change_min_coins(coins: list[int], amount: int) -> int:
    """
    Find minimum number of coins to make given amount.

    Time: O(amount * len(coins))
    Space: O(amount)

    LeetCode 322: Coin Change

    DP recurrence: dp[i] = min(dp[i - coin] + 1) for all coins <= i

    Interview follow-ups:
    - What if no solution exists? (Return -1)
    - How to reconstruct the actual coins used? (Track parent pointers)
    - What if coins array is empty? (Return -1 unless amount is 0)
    - Space optimization? (This is already optimal for this approach)
    """
    if amount == 0:
        return 0
    if not coins:
        return -1

    # dp[i] = minimum coins needed to make amount i
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float("inf"):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_count_ways(coins: list[int], amount: int) -> int:
    """
    Count number of ways to make given amount.

    Time: O(amount * len(coins))
    Space: O(amount)

    LeetCode 518: Coin Change 2

    This is the classic "unbounded knapsack" problem.
    """
    # dp[i] = number of ways to make amount i
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make 0: use no coins

    # Process coins one by one to avoid counting permutations
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


def coin_change_with_reconstruction(
    coins: list[int], amount: int
) -> tuple[int, list[int]]:
    """
    Find minimum coins and return the actual coins used.

    Returns: (min_coins, coins_used) or (-1, []) if impossible
    """
    if amount == 0:
        return 0, []
    if not coins:
        return -1, []

    dp = [float("inf")] * (amount + 1)
    parent = [-1] * (amount + 1)  # Track which coin was used
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float("inf"):
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin

    if dp[amount] == float("inf"):
        return -1, []

    # Reconstruct the solution
    coins_used = []
    current = amount
    while current > 0:
        coin = parent[current]
        coins_used.append(coin)
        current -= coin

    return dp[amount], coins_used


def coin_change_limited(coins: list[int], counts: list[int], amount: int) -> int:
    """
    Coin change with limited number of each coin (bounded knapsack).

    Args:
        coins: List of coin denominations
        counts: Number of each coin available
        amount: Target amount

    Returns: Minimum coins needed, or -1 if impossible

    This is the "bounded knapsack" variant.
    """
    if amount == 0:
        return 0

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin, count in zip(coins, counts):
        # Process from right to left to avoid using same coin multiple times
        for i in range(amount, coin - 1, -1):
            if dp[i - coin] != float("inf"):
                # Try using 1, 2, ..., min(count, i//coin) of this coin
                for k in range(1, min(count, i // coin) + 1):
                    if i - k * coin >= 0:
                        dp[i] = min(dp[i], dp[i - k * coin] + k)

    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_all_denominations(amount: int) -> list[list[int]]:
    """
    Find all possible ways to make amount using standard US coins.

    Returns all combinations (not permutations) of coins.
    """
    coins = [1, 5, 10, 25]  # penny, nickel, dime, quarter
    result = []

    def backtrack(remaining: int, coin_index: int, current_combination: list[int]):
        if remaining == 0:
            result.append(current_combination[:])
            return

        if coin_index >= len(coins) or remaining < 0:
            return

        coin = coins[coin_index]
        max_count = remaining // coin

        # Try using 0, 1, 2, ..., max_count of current coin
        for count in range(max_count + 1):
            current_combination.extend([coin] * count)
            backtrack(remaining - coin * count, coin_index + 1, current_combination)
            # Remove the coins we just added
            for _ in range(count):
                current_combination.pop()

    backtrack(amount, 0, [])
    return result


def coin_change_greedy(coins: list[int], amount: int) -> tuple[int, list[int]]:
    """
    Greedy approach for coin change (only works for certain coin systems).

    WARNING: This only works for "canonical" coin systems like US coins.
    For arbitrary coin systems, greedy may not give optimal solution.

    Time: O(len(coins) * log(len(coins)) + amount/largest_coin)
    Space: O(1)
    """
    if amount == 0:
        return 0, []

    # Sort coins in descending order
    coins_sorted = sorted(coins, reverse=True)
    coins_used = []
    total_coins = 0

    for coin in coins_sorted:
        count = amount // coin
        if count > 0:
            coins_used.extend([coin] * count)
            total_coins += count
            amount -= coin * count

    if amount > 0:
        return -1, []  # Cannot make exact change

    return total_coins, coins_used


def minimum_coins_infinite_supply(coins: list[int], amount: int) -> int:
    """
    Alternative implementation using BFS approach.

    Time: O(amount * len(coins))
    Space: O(amount)

    This can be more intuitive to understand than DP.
    """
    if amount == 0:
        return 0

    from collections import deque

    queue = deque([(0, 0)])  # (current_amount, coins_used)
    visited = {0}

    while queue:
        current_amount, coins_used = queue.popleft()

        for coin in coins:
            next_amount = current_amount + coin

            if next_amount == amount:
                return coins_used + 1

            if next_amount < amount and next_amount not in visited:
                visited.add(next_amount)
                queue.append((next_amount, coins_used + 1))

    return -1


def demo():
    """Demo function for coin change problems."""
    print("Coin Change Problems Demo")
    print("=" * 40)

    # Standard coin change
    coins = [1, 3, 4]
    amount = 6

    min_coins = coin_change_min_coins(coins, amount)
    ways = coin_change_count_ways(coins, amount)
    min_coins_with_solution, solution = coin_change_with_reconstruction(coins, amount)

    print(f"Coins: {coins}, Amount: {amount}")
    print(f"Minimum coins needed: {min_coins}")
    print(f"Number of ways: {ways}")
    print(f"Actual coins used: {solution} (total: {min_coins_with_solution})")
    print()

    # US coins example
    us_coins = [1, 5, 10, 25]
    us_amount = 67

    us_min = coin_change_min_coins(us_coins, us_amount)
    us_greedy_count, us_greedy_coins = coin_change_greedy(us_coins, us_amount)

    print(f"US coins for ${us_amount / 100:.2f}:")
    print(f"DP solution: {us_min} coins")
    print(f"Greedy solution: {us_greedy_count} coins: {us_greedy_coins}")
    print()

    # Limited coins example
    limited_coins = [1, 3, 4]
    limited_counts = [2, 1, 1]  # 2 ones, 1 three, 1 four
    limited_amount = 6

    limited_result = coin_change_limited(limited_coins, limited_counts, limited_amount)
    print(
        f"Limited coins {limited_coins} with counts {limited_counts} for amount {limited_amount}:"
    )
    print(f"Minimum coins: {limited_result}")
    print()

    # All combinations for small amount
    small_amount = 10
    all_ways = coin_change_all_denominations(small_amount)
    print(f"All ways to make {small_amount} cents with US coins:")
    for i, way in enumerate(all_ways[:5]):  # Show first 5
        print(f"  {i + 1}: {way}")
    if len(all_ways) > 5:
        print(f"  ... and {len(all_ways) - 5} more ways")
    print()

    # Edge cases
    print("Edge cases:")
    print(f"Amount 0: {coin_change_min_coins([1, 2, 5], 0)} coins")
    print(f"No coins: {coin_change_min_coins([], 5)} coins")
    print(f"Impossible: {coin_change_min_coins([3, 5], 1)} coins")

    # BFS approach comparison
    bfs_result = minimum_coins_infinite_supply(coins, amount)
    print(f"BFS approach for {coins}, amount {amount}: {bfs_result} coins")


if __name__ == "__main__":
    demo()
