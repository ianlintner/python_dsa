"""
LeetCode 198: House Robber

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        Dynamic programming approach with space optimization.

        At each house, we have two choices:
        1. Rob current house: get nums[i] + max money from houses up to i-2
        2. Skip current house: get max money from houses up to i-1

        We take the maximum of these two options.

        Space optimization: Only need to track the last two optimal values.

        Time: O(n) - Single pass through all houses
        Space: O(1) - Only using constant extra space
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        # prev2: max money up to house i-2
        # prev1: max money up to house i-1
        prev2 = nums[0]
        prev1 = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            current = max(
                nums[i] + prev2,  # Rob current house
                prev1             # Skip current house
            )
            prev2 = prev1
            prev1 = current

        return prev1

    def robDP(self, nums: List[int]) -> int:
        """
        Standard DP approach with memoization array.

        More explicit about the recurrence relation but uses O(n) space.

        Time: O(n) - Fill array of size n
        Space: O(n) - DP array
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            dp[i] = max(
                nums[i] + dp[i - 2],  # Rob current house
                dp[i - 1]             # Skip current house
            )

        return dp[n - 1]

    def robRecursive(self, nums: List[int]) -> int:
        """
        Recursive approach with memoization.

        This shows the recursive structure but is less efficient
        due to function call overhead.

        Time: O(n) - Each subproblem solved once
        Space: O(n) - Recursion stack + memoization
        """
        if not nums:
            return 0

        memo = {}

        def rob_from(index):
            if index >= len(nums):
                return 0
            if index in memo:
                return memo[index]

            # Choice 1: Rob current house and move to index+2
            rob_current = nums[index] + rob_from(index + 2)
            
            # Choice 2: Skip current house and move to index+1
            skip_current = rob_from(index + 1)

            result = max(rob_current, skip_current)
            memo[index] = result
            return result

        return rob_from(0)

    def robBruteForce(self, nums: List[int]) -> int:
        """
        Brute force recursive approach without memoization.

        This demonstrates the exponential nature of the problem
        but is too slow for large inputs.

        Time: O(2^n) - Explores all possible combinations
        Space: O(n) - Recursion stack depth
        """
        if not nums:
            return 0

        def rob_from(index):
            if index >= len(nums):
                return 0

            # Choice 1: Rob current house
            rob_current = nums[index] + rob_from(index + 2)
            
            # Choice 2: Skip current house
            skip_current = rob_from(index + 1)

            return max(rob_current, skip_current)

        return rob_from(0)


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different robbing scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([2, 1, 1, 2], 4),
        ([5], 5),
        ([1, 2], 2),
        ([2, 1], 2),
        ([1, 3, 1, 3, 100], 103),
    ]

    for nums, expected in test_cases:
        result = solution.rob(nums)
        demos.append(f"Houses: {nums}")
        demos.append(f"Max money: {result}")

        # Show decision process for smaller arrays
        if len(nums) <= 5:
            demos.append("Decision analysis:")
            n = len(nums)
            dp = [0] * max(n, 2)
            if n >= 1:
                dp[0] = nums[0]
                demos.append(f"  House 0: Rob {nums[0]} → total = {dp[0]}")
            if n >= 2:
                dp[1] = max(nums[0], nums[1])
                action = "rob" if nums[1] > nums[0] else "skip"
                demos.append(f"  House 1: {action} (max of {nums[0]} vs {nums[1]}) → total = {dp[1]}")

            for i in range(2, n):
                rob_current = nums[i] + dp[i - 2]
                skip_current = dp[i - 1]
                dp[i] = max(rob_current, skip_current)
                action = "rob" if rob_current > skip_current else "skip"
                demos.append(f"  House {i}: {action} (max of {rob_current} vs {skip_current}) → total = {dp[i]}")
        
        demos.append("")

    # Pattern analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Recurrence Relation:")
    demos.append("dp[i] = max(nums[i] + dp[i-2], dp[i-1])")
    demos.append("")
    demos.append("Intuition:")
    demos.append("- At each house, choose between:")
    demos.append("  1. Rob it: get current money + max from non-adjacent houses")
    demos.append("  2. Skip it: get max money from previous house")
    demos.append("- Cannot rob adjacent houses due to security system")
    demos.append("- Greedy approach doesn't work: need to consider global optimum")
    demos.append("")

    # Show different patterns
    demos.append("=== Pattern Examples ===")
    
    # Increasing sequence
    increasing = [1, 2, 3, 4, 5]
    result_inc = solution.rob(increasing)
    demos.append(f"Increasing: {increasing} → {result_inc}")
    demos.append("  Optimal: rob houses 0, 2, 4 (1+3+5=9)")
    demos.append("")

    # Decreasing sequence  
    decreasing = [5, 4, 3, 2, 1]
    result_dec = solution.rob(decreasing)
    demos.append(f"Decreasing: {decreasing} → {result_dec}")
    demos.append("  Optimal: rob houses 0, 2, 4 (5+3+1=9)")
    demos.append("")

    # Alternating high-low
    alternating = [10, 1, 10, 1, 10]
    result_alt = solution.rob(alternating)
    demos.append(f"Alternating: {alternating} → {result_alt}")
    demos.append("  Optimal: rob all odd positions (10+10+10=30)")
    demos.append("")

    # Mixed pattern
    mixed = [2, 1, 4, 9]
    result_mix = solution.rob(mixed)
    demos.append(f"Mixed: {mixed} → {result_mix}")
    demos.append("  Optimal: rob houses 0, 3 (2+9=11) vs 1,3 (1+9=10)")
    demos.append("")

    # Performance comparison
    import time

    large_array = [i % 100 + 1 for i in range(1000)]

    # Time space-optimized approach
    start_time = time.time()
    for _ in range(1000):
        solution.rob(large_array)
    optimized_time = time.time() - start_time

    # Time standard DP approach
    start_time = time.time()
    for _ in range(1000):
        solution.robDP(large_array)
    dp_time = time.time() - start_time

    # Time recursive approach (smaller array)
    small_array = [i % 10 + 1 for i in range(20)]
    start_time = time.time()
    for _ in range(100):
        solution.robRecursive(small_array)
    recursive_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Space-optimized DP (1000 runs, 1000 houses): {optimized_time:.6f}s")
    demos.append(f"Standard DP (1000 runs, 1000 houses): {dp_time:.6f}s")
    demos.append(f"Recursive with memo (100 runs, 20 houses): {recursive_time:.6f}s")
    demos.append("")
    demos.append("Space-optimized: O(n) time, O(1) space")
    demos.append("Standard DP: O(n) time, O(n) space")
    demos.append("Recursive: O(n) time, O(n) space + call overhead")
    demos.append("")

    # Edge cases
    demos.append("=== Edge Cases ===")
    demos.append("- Empty array: 0 (no houses to rob)")
    demos.append("- Single house: rob it")
    demos.append("- Two houses: rob the one with more money")
    demos.append("- All same values: rob every other house")
    demos.append("- Large single value: changes optimal strategy")
    demos.append("")

    # Problem variations
    demos.append("=== Problem Variations ===")
    demos.append("- House Robber II: houses arranged in circle")
    demos.append("- House Robber III: houses arranged as binary tree")
    demos.append("- Paint House: minimize cost with adjacent color constraint")
    demos.append("- Stock trading: cooldown period between transactions")
    demos.append("- Jump Game: minimum jumps with constraints")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Resource scheduling with conflict constraints")
    demos.append("- Investment planning with mutually exclusive options")
    demos.append("- Task scheduling with dependencies")
    demos.append("- Network security: maximize coverage without interference")
    demos.append("- Facility location: optimal placement with distance constraints")
    demos.append("- Game theory: optimal strategy selection")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input=[[1, 2, 3, 1]], expected=4, description="Standard case: rob houses 0 and 2"),
    TestCase(input=[[2, 7, 9, 3, 1]], expected=12, description="Rob houses 0, 2, 4 for max money"),
    TestCase(input=[[2, 1, 1, 2]], expected=4, description="Rob houses 0 and 3"),
    TestCase(input=[[5]], expected=5, description="Single house - rob it"),
    TestCase(input=[[1, 2]], expected=2, description="Two houses - rob the richer one"),
    TestCase(input=[[2, 1]], expected=2, description="Two houses - rob the first one"),
    TestCase(input=[[]], expected=0, description="Empty array - no houses to rob"),
    TestCase(input=[[1, 3, 1, 3, 100]], expected=103, description="Large final house changes strategy"),
    TestCase(input=[[10, 5, 2, 7, 8]], expected=19, description="Rob houses 0, 3 for optimal result"),
    TestCase(input=[[1, 1, 1, 1, 1]], expected=3, description="All equal - rob every other house"),
]


def test_solution():
    """Test the house robber solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.rob, TEST_CASES)


# Register the problem
register_problem(
    slug="house_robber",
    leetcode_num=198,
    title="House Robber",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_1D,
    solution_func=Solution().rob,
    test_func=test_solution,
    demo_func=create_demo_output,
)
