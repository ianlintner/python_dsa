

def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """
    0/1 Knapsack Problem - each item can be taken at most once.

    Time: O(n * capacity)
    Space: O(n * capacity)

    Classic DP problem: dp[i][w] = max value using first i items with weight limit w

    Interview follow-ups:
    - How to optimize space? (Use 1D array, process backwards)
    - How to reconstruct solution? (Track which items were taken)
    - What if weights are very large? (Use value-based DP instead)
    - Fractional knapsack? (Use greedy by value/weight ratio)
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0

    # dp[i][w] = maximum value using items 0..i-1 with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i - 1][w]

            # Take item i-1 if it fits
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][capacity]


def knapsack_01_optimized(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Space-optimized 0/1 Knapsack using 1D array.

    Time: O(n * capacity)
    Space: O(capacity)

    Key insight: Process weights in reverse order to avoid using updated values.
    """
    if not weights or capacity == 0:
        return 0

    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # Process in reverse to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def knapsack_01_with_items(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, list[int]]:
    """
    0/1 Knapsack with reconstruction of selected items.

    Returns: (max_value, list_of_selected_item_indices)
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # Reconstruct solution
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # Item index
            w -= weights[i - 1]

    selected_items.reverse()
    return dp[n][capacity], selected_items


def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Unbounded Knapsack - unlimited quantity of each item.

    Time: O(n * capacity)
    Space: O(capacity)

    Similar to coin change problem - can use each item multiple times.
    """
    if not weights or capacity == 0:
        return 0

    dp = [0] * (capacity + 1)

    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def bounded_knapsack(
    weights: list[int], values: list[int], counts: list[int], capacity: int
) -> int:
    """
    Bounded Knapsack - limited quantity of each item.

    Time: O(capacity * sum(counts))
    Space: O(capacity)

    Each item i can be taken at most counts[i] times.
    """
    if not weights or capacity == 0:
        return 0

    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # Process each item type
        for _ in range(counts[i]):
            # Process in reverse (like 0/1 knapsack)
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def fractional_knapsack(weights: list[int], values: list[int], capacity: int) -> float:
    """
    Fractional Knapsack - can take fractions of items.

    Time: O(n log n) for sorting
    Space: O(n) for sorting

    Greedy approach: sort by value/weight ratio, take highest ratios first.
    """
    if not weights or capacity == 0:
        return 0.0

    # Create list of (value/weight ratio, weight, value, index)
    items = []
    for i in range(len(weights)):
        if weights[i] > 0:  # Avoid division by zero
            ratio = values[i] / weights[i]
            items.append((ratio, weights[i], values[i], i))

    # Sort by ratio in descending order
    items.sort(reverse=True)

    total_value = 0.0
    remaining_capacity = capacity

    for ratio, weight, value, _ in items:
        if remaining_capacity >= weight:
            # Take the whole item
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of the item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            break

    return total_value


def multiple_knapsack(
    weights: list[int], values: list[int], counts: list[int], capacity: int
) -> int:
    """
    Multiple Knapsack using binary representation optimization.

    Time: O(capacity * sum(log(counts[i])))
    Space: O(capacity)

    Optimize bounded knapsack by representing counts in binary.
    Instead of counts[i] items, use log(counts[i]) groups.
    """
    if not weights or capacity == 0:
        return 0

    # Convert to 0/1 knapsack by binary representation
    new_weights = []
    new_values = []

    for i in range(len(weights)):
        count = counts[i]
        k = 1
        while k < count:
            new_weights.append(k * weights[i])
            new_values.append(k * values[i])
            count -= k
            k *= 2

        if count > 0:
            new_weights.append(count * weights[i])
            new_values.append(count * values[i])

    return knapsack_01_optimized(new_weights, new_values, capacity)


def partition_equal_subset_sum(nums: list[int]) -> bool:
    """
    Partition Equal Subset Sum - special case of knapsack.

    LeetCode 416: Partition Equal Subset Sum

    Can partition array into two subsets with equal sum?
    This is 0/1 knapsack where target = sum(nums) // 2
    """
    total_sum = sum(nums)

    if total_sum % 2 != 0:
        return False

    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]

    return dp[target]


def target_sum(nums: list[int], target: int) -> int:
    """
    Target Sum - assign +/- to each number to reach target.

    LeetCode 494: Target Sum

    Transform to knapsack: find subset with sum = (total + target) // 2
    """
    total = sum(nums)

    if target > total or target < -total or (total + target) % 2 != 0:
        return 0

    subset_sum = (total + target) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for num in nums:
        for j in range(subset_sum, num - 1, -1):
            dp[j] += dp[j - num]

    return dp[subset_sum]


def demo():
    """Demo function for knapsack algorithms."""
    print("Knapsack Problems Demo")
    print("=" * 40)

    # Basic 0/1 knapsack
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7

    print("0/1 Knapsack:")
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Capacity: {capacity}")

    max_value_2d = knapsack_01(weights, values, capacity)
    max_value_1d = knapsack_01_optimized(weights, values, capacity)
    max_value_items, selected = knapsack_01_with_items(weights, values, capacity)

    print(f"Max value (2D DP): {max_value_2d}")
    print(f"Max value (1D DP): {max_value_1d}")
    print(f"Max value with items: {max_value_items}")
    print(f"Selected items (indices): {selected}")
    print(f"Selected weights: {[weights[i] for i in selected]}")
    print(f"Selected values: {[values[i] for i in selected]}")
    print()

    # Unbounded knapsack
    print("Unbounded Knapsack:")
    unbounded_value = unbounded_knapsack(weights, values, capacity)
    print(f"Max value (unlimited items): {unbounded_value}")
    print()

    # Bounded knapsack
    counts = [2, 1, 1, 1]  # Can take at most 2 of first item
    print("Bounded Knapsack:")
    print(f"Item counts: {counts}")
    bounded_value = bounded_knapsack(weights, values, counts, capacity)
    multiple_value = multiple_knapsack(weights, values, counts, capacity)
    print(f"Max value (bounded): {bounded_value}")
    print(f"Max value (multiple/binary): {multiple_value}")
    print()

    # Fractional knapsack
    print("Fractional Knapsack:")
    fractional_value = fractional_knapsack(weights, values, capacity)
    print(f"Max value (fractional): {fractional_value:.2f}")
    print()

    # Partition equal subset sum
    print("Partition Equal Subset Sum:")
    partition_nums = [1, 5, 11, 5]
    can_partition = partition_equal_subset_sum(partition_nums)
    print(f"Array: {partition_nums}")
    print(f"Can partition into equal subsets: {can_partition}")
    print()

    # Target sum
    print("Target Sum:")
    target_nums = [1, 1, 1, 1, 1]
    target_val = 3
    ways = target_sum(target_nums, target_val)
    print(f"Array: {target_nums}")
    print(f"Target: {target_val}")
    print(f"Number of ways: {ways}")
    print()

    # Performance comparison
    print("Algorithm Comparison:")
    print("0/1 Knapsack:")
    print("  - Each item used at most once")
    print("  - Time: O(n * capacity), Space: O(capacity) optimized")
    print("  - Most common variant in interviews")
    print()
    print("Unbounded Knapsack:")
    print("  - Unlimited quantity of each item")
    print("  - Similar to coin change problem")
    print("  - Time: O(n * capacity), Space: O(capacity)")
    print()
    print("Bounded Knapsack:")
    print("  - Limited quantity of each item")
    print("  - Can optimize with binary representation")
    print("  - Time: O(capacity * sum(counts))")
    print()
    print("Fractional Knapsack:")
    print("  - Can take fractions of items")
    print("  - Greedy algorithm (not DP)")
    print("  - Time: O(n log n), Space: O(1)")
    print()
    print("Applications:")
    print("  - Resource allocation")
    print("  - Investment portfolio optimization")
    print("  - Cargo loading")
    print("  - Memory management")
    print("  - Subset sum problems")


if __name__ == "__main__":
    demo()
