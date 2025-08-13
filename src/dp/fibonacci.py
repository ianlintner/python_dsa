from typing import Dict, List
from functools import lru_cache


def fibonacci_recursive(n: int) -> int:
    """
    Naive recursive Fibonacci - exponential time complexity.

    Time: O(2^n) - exponential, very slow
    Space: O(n) - recursion stack

    This is the classic example of why memoization is needed.
    Only use this to demonstrate the problem with naive recursion.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Fibonacci with memoization (top-down DP).

    Time: O(n)
    Space: O(n) for memo + O(n) recursion stack

    Interview follow-ups:
    - How does memoization help? (Avoids recomputing subproblems)
    - What's the space trade-off? (O(n) space for O(2^n) -> O(n) time improvement)
    - Can we do better on space? (Yes, bottom-up with O(1) space)
    """
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)

    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru_cache(n: int) -> int:
    """
    Fibonacci using Python's built-in LRU cache decorator.

    Time: O(n)
    Space: O(n)

    This is the most Pythonic way to add memoization.
    """
    if n <= 1:
        return n
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)


def fibonacci_bottom_up(n: int) -> int:
    """
    Bottom-up DP approach (tabulation).

    Time: O(n)
    Space: O(n) for the DP table

    Builds solution from smallest subproblems up to the target.
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_optimized(n: int) -> int:
    """
    Space-optimized bottom-up DP.

    Time: O(n)
    Space: O(1) - only store last two values

    This is the optimal solution for computing single Fibonacci number.
    """
    if n <= 1:
        return n

    prev2, prev1 = 0, 1

    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1


def fibonacci_matrix_power(n: int) -> int:
    """
    Matrix exponentiation approach for Fibonacci.

    Time: O(log n)
    Space: O(log n) for recursion stack

    Uses the fact that:
    [F(n+1)]   [1 1]^n   [1]
    [F(n)  ] = [1 0]   * [0]

    This is the fastest method for very large n.
    """

    def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """Multiply two 2x2 matrices."""
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
        """Compute matrix^power using fast exponentiation."""
        if power == 1:
            return matrix

        if power % 2 == 0:
            half_power = matrix_power(matrix, power // 2)
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))

    if n <= 1:
        return n

    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)

    return result_matrix[0][1]  # F(n) is at position [0][1]


def fibonacci_sequence(n: int) -> List[int]:
    """
    Generate first n Fibonacci numbers efficiently.

    Time: O(n)
    Space: O(n) for the result list

    Useful when you need multiple Fibonacci numbers.
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]

    sequence = [0, 1]

    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])

    return sequence


def tribonacci(n: int) -> int:
    """
    Tribonacci sequence: T(n) = T(n-1) + T(n-2) + T(n-3)

    Time: O(n)
    Space: O(1)

    Similar to Fibonacci but with three previous terms.
    Common interview variation.
    """
    if n == 0:
        return 0
    if n <= 2:
        return 1

    a, b, c = 0, 1, 1

    for i in range(3, n + 1):
        next_val = a + b + c
        a, b, c = b, c, next_val

    return c


def climbing_stairs(n: int) -> int:
    """
    Classic DP problem: How many ways to climb n stairs (1 or 2 steps at a time)?

    This is actually the Fibonacci sequence in disguise!
    ways(n) = ways(n-1) + ways(n-2)

    LeetCode 70: Climbing Stairs
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1


def house_robber(nums: List[int]) -> int:
    """
    House Robber problem - another Fibonacci-like DP.

    Can't rob adjacent houses. What's the maximum money you can rob?
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    LeetCode 198: House Robber
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, current

    return prev1


def demo():
    """Demo function for Fibonacci and related problems."""
    print("Fibonacci and DP Patterns Demo")
    print("=" * 40)

    n = 10
    print(f"Computing Fibonacci({n}) with different methods:")

    # Compare different approaches
    methods = [
        ("Memoized", fibonacci_memoized),
        ("LRU Cache", fibonacci_lru_cache),
        ("Bottom-up", fibonacci_bottom_up),
        ("Optimized", fibonacci_optimized),
        ("Matrix Power", fibonacci_matrix_power),
    ]

    for name, func in methods:
        result = func(n)
        print(f"  {name:12}: {result}")

    print()

    # Show first few Fibonacci numbers
    sequence = fibonacci_sequence(15)
    print(f"First 15 Fibonacci numbers: {sequence}")
    print()

    # Tribonacci
    print("Tribonacci sequence:")
    trib_seq = [tribonacci(i) for i in range(10)]
    print(f"First 10 Tribonacci numbers: {trib_seq}")
    print()

    # Related problems
    stairs = 5
    ways = climbing_stairs(stairs)
    print(f"Ways to climb {stairs} stairs: {ways}")

    houses = [2, 7, 9, 3, 1]
    max_money = house_robber(houses)
    print(f"House robber with {houses}: ${max_money}")

    print()

    # Performance comparison for larger n
    print("Performance comparison for larger values:")
    large_n = 35

    import time

    # Only test fast methods for large n
    fast_methods = [("Optimized", fibonacci_optimized), ("Matrix Power", fibonacci_matrix_power)]

    for name, func in fast_methods:
        start_time = time.time()
        result = func(large_n)
        end_time = time.time()
        print(f"  {name:12}: F({large_n}) = {result} (took {end_time - start_time:.6f}s)")


if __name__ == "__main__":
    demo()
