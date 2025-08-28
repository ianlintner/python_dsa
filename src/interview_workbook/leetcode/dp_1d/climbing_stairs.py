"""
LeetCode 70: Climbing Stairs

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Time Complexity: O(n)
Space Complexity: O(1)
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def climbStairs(self, n: int) -> int:
        """
        Dynamic programming approach using space-optimized iteration.

        This is essentially the Fibonacci sequence:
        - ways[i] = ways[i-1] + ways[i-2]
        - Base cases: ways[1] = 1, ways[2] = 2

        We can optimize space by only keeping track of the last two values.

        Time: O(n) - Single pass through n steps
        Space: O(1) - Only using constant extra space
        """
        if n <= 2:
            return n

        # Only need to track last two values
        prev2 = 1  # ways to reach step 1
        prev1 = 2  # ways to reach step 2

        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current

        return prev1

    def climbStairsDP(self, n: int) -> int:
        """
        Standard DP approach with memoization array.

        More intuitive but uses O(n) space.

        Time: O(n) - Fill array of size n
        Space: O(n) - DP array
        """
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    def climbStairsRecursive(self, n: int) -> int:
        """
        Recursive approach with memoization.

        This demonstrates the recursive structure but is less efficient
        due to function call overhead.

        Time: O(n) - Each subproblem solved once
        Space: O(n) - Recursion stack + memoization
        """
        memo = {}

        def climb(steps_left):
            if steps_left in memo:
                return memo[steps_left]

            if steps_left <= 2:
                return steps_left

            result = climb(steps_left - 1) + climb(steps_left - 2)
            memo[steps_left] = result
            return result

        return climb(n)

    def climbStairsMath(self, n: int) -> int:
        """
        Mathematical approach using Binet's formula for Fibonacci numbers.

        This is the most efficient approach but less intuitive and can have
        floating-point precision issues for large n.

        Time: O(1) - Constant time calculation
        Space: O(1) - No extra space
        """
        import math

        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2
        psi = (1 - sqrt5) / 2

        # Fibonacci sequence starts: 1, 1, 2, 3, 5, 8, ...
        # Climbing stairs sequence: 1, 2, 3, 5, 8, 13, ...
        # So climbStairs(n) = fibonacci(n+1)
        return int((phi ** (n + 1) - psi ** (n + 1)) / sqrt5)


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different climbing scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with step-by-step analysis
    test_cases = [(1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)]

    for n, expected in test_cases:
        result = solution.climbStairs(n)
        demos.append(f"n = {n}: {result} ways")

        if n <= 4:  # Show detailed breakdown for small cases
            if n == 1:
                demos.append("  Ways: [1]")
            elif n == 2:
                demos.append("  Ways: [1+1], [2]")
            elif n == 3:
                demos.append("  Ways: [1+1+1], [1+2], [2+1]")
            elif n == 4:
                demos.append("  Ways: [1+1+1+1], [1+1+2], [1+2+1], [2+1+1], [2+2]")
        demos.append("")

    # Pattern analysis
    demos.append("=== Pattern Analysis ===")
    demos.append("This follows the Fibonacci sequence:")
    demos.append("f(n) = f(n-1) + f(n-2)")
    demos.append("")
    demos.append("Intuition:")
    demos.append("- To reach step n, you can come from step (n-1) with 1 step")
    demos.append("- Or from step (n-2) with 2 steps")
    demos.append("- Total ways = ways to reach (n-1) + ways to reach (n-2)")
    demos.append("")

    # Show sequence
    sequence_values = []
    for i in range(1, 16):
        sequence_values.append(str(solution.climbStairs(i)))

    demos.append("Sequence for n=1 to 15:")
    demos.append(", ".join(sequence_values))
    demos.append("")

    # Algorithm comparison
    demos.append("=== Algorithm Approaches ===")
    demos.append("1. Space-optimized DP: O(n) time, O(1) space")
    demos.append("2. Standard DP: O(n) time, O(n) space")
    demos.append("3. Recursive with memo: O(n) time, O(n) space")
    demos.append("4. Mathematical formula: O(1) time, O(1) space")
    demos.append("")

    # Performance comparison
    import time

    n_large = 40

    # Time space-optimized approach
    start_time = time.time()
    for _ in range(10000):
        solution.climbStairs(n_large)
    optimized_time = time.time() - start_time

    # Time standard DP approach
    start_time = time.time()
    for _ in range(10000):
        solution.climbStairsDP(n_large)
    dp_time = time.time() - start_time

    # Time mathematical approach
    start_time = time.time()
    for _ in range(10000):
        solution.climbStairsMath(n_large)
    math_time = time.time() - start_time

    demos.append("=== Performance Comparison (n=40, 10k runs) ===")
    demos.append(f"Space-optimized DP: {optimized_time:.6f}s")
    demos.append(f"Standard DP: {dp_time:.6f}s")
    demos.append(f"Mathematical formula: {math_time:.6f}s")
    demos.append("")

    # Edge cases and considerations
    demos.append("=== Edge Cases & Considerations ===")
    demos.append("- n=1: Only one way [1]")
    demos.append("- n=2: Two ways [1+1], [2]")
    demos.append("- Large n: Mathematical approach fastest but precision issues")
    demos.append("- Space-optimized DP: Best balance of efficiency and reliability")
    demos.append("")

    # Extensions and variations
    demos.append("=== Problem Variations ===")
    demos.append("- Climbing stairs with k-step jumps")
    demos.append("- Minimum cost to climb stairs (with step costs)")
    demos.append("- Count paths in grid (2D version)")
    demos.append("- House robber problem (adjacent constraint)")
    demos.append("- Decode ways (string to number mappings)")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Path counting in graphs/grids")
    demos.append("- Financial modeling (investment combinations)")
    demos.append("- Game theory (move possibilities)")
    demos.append("- Resource allocation (distribution methods)")
    demos.append("- Sequence generation (combinatorial problems)")
    demos.append("- Algorithm design (recursive decomposition)")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input=[1], expected=1, description="Single step"),
    TestCase(input=[2], expected=2, description="Two steps: [1+1] or [2]"),
    TestCase(input=[3], expected=3, description="Three ways to reach step 3"),
    TestCase(input=[4], expected=5, description="Five ways to reach step 4"),
    TestCase(input=[5], expected=8, description="Fibonacci sequence continues"),
    TestCase(input=[10], expected=89, description="Larger example"),
    TestCase(input=[20], expected=10946, description="Even larger example"),
    TestCase(input=[35], expected=14930352, description="Large n to test efficiency"),
]


def test_solution():
    """Test the climbing stairs solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.climbStairs, TEST_CASES)


# Register the problem
register_problem(
    slug="climbing_stairs",
    leetcode_num=70,
    title="Climbing Stairs",
    difficulty=Difficulty.EASY,
    category=Category.DP_1D,
    solution_func=Solution().climbStairs,
    test_func=test_solution,
    demo_func=create_demo_output,
)
