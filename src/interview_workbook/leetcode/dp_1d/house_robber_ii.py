"""
LeetCode 213: House Robber II

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last house. Meanwhile, adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

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
        Dynamic programming approach adapted for circular arrangement.

        Key insight: Since houses are in a circle, we cannot rob both the first
        and last house. This gives us two scenarios:
        1. Rob houses 0 to n-2 (exclude last house)
        2. Rob houses 1 to n-1 (exclude first house)

        We solve both scenarios using the linear house robber algorithm
        and return the maximum result.

        Time: O(n) - Two passes through the array
        Space: O(1) - Only using constant extra space
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])

        # Scenario 1: Rob houses 0 to n-2 (can include first, exclude last)
        max_excluding_last = self._rob_linear(nums[:-1])

        # Scenario 2: Rob houses 1 to n-1 (exclude first, can include last)
        max_excluding_first = self._rob_linear(nums[1:])

        return max(max_excluding_last, max_excluding_first)

    def _rob_linear(self, nums: List[int]) -> int:
        """
        Helper function: solve linear house robber problem.

        This is the same algorithm from House Robber I.
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        prev2 = nums[0]
        prev1 = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            current = max(
                nums[i] + prev2,  # Rob current house
                prev1,  # Skip current house
            )
            prev2 = prev1
            prev1 = current

        return prev1

    def robDP(self, nums: List[int]) -> int:
        """
        Alternative implementation using explicit DP arrays.

        More verbose but shows the logic clearly.

        Time: O(n) - Two linear scans
        Space: O(n) - Two DP arrays
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])

        n = len(nums)

        # Scenario 1: houses 0 to n-2
        dp1 = [0] * (n - 1)
        dp1[0] = nums[0]
        dp1[1] = max(nums[0], nums[1])

        for i in range(2, n - 1):
            dp1[i] = max(nums[i] + dp1[i - 2], dp1[i - 1])

        # Scenario 2: houses 1 to n-1
        dp2 = [0] * (n - 1)
        dp2[0] = nums[1]
        if n > 2:
            dp2[1] = max(nums[1], nums[2])

        for i in range(2, n - 1):
            dp2[i] = max(nums[i + 1] + dp2[i - 2], dp2[i - 1])

        return max(dp1[n - 2], dp2[n - 2])

    def robRecursive(self, nums: List[int]) -> int:
        """
        Recursive approach with memoization.

        Demonstrates the problem structure but less efficient.

        Time: O(n) - Each subproblem solved once (per scenario)
        Space: O(n) - Recursion stack + memoization (per scenario)
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])

        # Try both scenarios and take the maximum
        scenario1 = self._rob_recursive_helper(nums[:-1])
        scenario2 = self._rob_recursive_helper(nums[1:])

        return max(scenario1, scenario2)

    def _rob_recursive_helper(self, nums: List[int]) -> int:
        """Helper function for recursive approach."""
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


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing circular house robbing scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        ([2, 3, 2], 3),
        ([1, 2, 3, 1], 4),
        ([1, 2, 3], 3),
        ([5], 5),
        ([1, 2], 2),
        ([2, 7, 9, 3, 1], 11),
        ([1, 1, 1, 2], 3),
    ]

    for nums, _expected in test_cases:
        result = solution.rob(nums)
        demos.append(f"Houses (circular): {nums}")
        demos.append(f"Max money: {result}")

        # Show both scenarios for smaller arrays
        if len(nums) <= 5 and len(nums) > 2:
            # Scenario 1: exclude last house
            scenario1 = nums[:-1]
            max1 = solution._rob_linear(scenario1)
            demos.append(f"  Scenario 1 (exclude last): {scenario1} → {max1}")

            # Scenario 2: exclude first house
            scenario2 = nums[1:]
            max2 = solution._rob_linear(scenario2)
            demos.append(f"  Scenario 2 (exclude first): {scenario2} → {max2}")

            demos.append(f"  Optimal choice: {'Scenario 1' if max1 >= max2 else 'Scenario 2'}")

        demos.append("")

    # Circular vs Linear comparison
    demos.append("=== Circular vs Linear Comparison ===")

    linear_examples = [[2, 3, 2], [1, 2, 3, 1], [2, 7, 9, 3, 1]]

    for nums in linear_examples:
        circular_result = solution.rob(nums)
        linear_result = solution._rob_linear(nums)

        demos.append(f"Houses: {nums}")
        demos.append(f"Linear arrangement: {linear_result}")
        demos.append(f"Circular arrangement: {circular_result}")
        demos.append(f"Difference: {linear_result - circular_result}")
        demos.append("")

    # Algorithm analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Circular Constraint Impact:")
    demos.append("- Cannot rob both first and last house (they're adjacent)")
    demos.append("- Two scenarios to consider:")
    demos.append("  1. Include first house, exclude last house")
    demos.append("  2. Exclude first house, include last house")
    demos.append("- Solve both scenarios independently using linear algorithm")
    demos.append("- Return maximum of both scenarios")
    demos.append("")

    demos.append("Why This Works:")
    demos.append("- Any optimal solution either includes house 0 or doesn't")
    demos.append("- If it includes house 0, it cannot include house n-1")
    demos.append("- If it doesn't include house 0, we can consider house n-1")
    demos.append("- These scenarios are mutually exclusive and exhaustive")
    demos.append("")

    # Edge cases
    demos.append("=== Edge Cases ===")
    demos.append("- Single house: rob it (no circular constraint)")
    demos.append("- Two houses: rob the one with more money")
    demos.append("- Three houses: can rob either middle house or one end house")
    demos.append("- All equal values: pattern depends on array length")
    demos.append("")

    # Show detailed analysis for 3-house case
    demos.append("=== Three-House Analysis ===")
    three_house_cases = [[1, 2, 3], [5, 1, 2], [2, 7, 8], [10, 1, 1]]

    for nums in three_house_cases:
        result = solution.rob(nums)
        demos.append(f"Houses: {nums}")
        demos.append("Options:")
        demos.append(f"  - Rob house 0: {nums[0]} (cannot rob houses 1 or 2)")
        demos.append(f"  - Rob house 1: {nums[1]} (cannot rob houses 0 or 2)")
        demos.append(f"  - Rob house 2: {nums[2]} (cannot rob houses 0 or 1)")
        demos.append("  - Rob houses 0,2: NOT ALLOWED (circular constraint)")
        demos.append(f"Best choice: rob house with value {result}")
        demos.append("")

    # Performance comparison
    import time

    large_array = [i % 100 + 1 for i in range(1000)]

    # Time optimized approach
    start_time = time.time()
    for _ in range(1000):
        solution.rob(large_array)
    optimized_time = time.time() - start_time

    # Time DP approach
    start_time = time.time()
    for _ in range(1000):
        solution.robDP(large_array)
    dp_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Space-optimized approach (1000 runs, 1000 houses): {optimized_time:.6f}s")
    demos.append(f"DP array approach (1000 runs, 1000 houses): {dp_time:.6f}s")
    demos.append("")
    demos.append("Space-optimized: O(n) time, O(1) space")
    demos.append("DP arrays: O(n) time, O(n) space")
    demos.append("")

    # Problem variations
    demos.append("=== Problem Variations ===")
    demos.append("- House Robber III: houses arranged as binary tree")
    demos.append("- Paint House: minimize cost with color constraints")
    demos.append("- Maximum sum circular subarray: similar circular constraint")
    demos.append("- Stock trading with cooldown: transaction constraints")
    demos.append("- Circular array maximum subarray problems")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Circular buffer optimization problems")
    demos.append("- Round-robin scheduling with constraints")
    demos.append("- Circular facility placement with interference zones")
    demos.append("- Time-slot allocation in circular schedules")
    demos.append("- Network topology optimization in ring networks")
    demos.append("- Game theory on circular boards/graphs")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input_args=([2, 3, 2],), expected=3, description="Cannot rob first and last together"),
    TestCase(input_args=([1, 2, 3, 1],), expected=4, description="Rob houses 1 and 3 (0-indexed)"),
    TestCase(
        input_args=([1, 2, 3],), expected=3, description="Three houses - rob the maximum single house"
    ),
    TestCase(input_args=([5],), expected=5, description="Single house - no circular constraint"),
    TestCase(input_args=([1, 2],), expected=2, description="Two houses - rob the larger one"),
    TestCase(input_args=([2, 1],), expected=2, description="Two houses - rob the first one"),
    TestCase(
        input_args=([2, 7, 9, 3, 1],),
        expected=11,
        description="Circular constraint reduces max from 12 to 11",
    ),
    TestCase(
        input_args=([1, 1, 1, 2],),
        expected=3,
        description="Rob house with value 2 and one house with value 1",
    ),
    TestCase(
        input_args=([4, 1, 2, 7, 5, 3, 1],),
        expected=14,
        description="Larger example with circular constraint",
    ),
    TestCase(
        input_args=([1, 1, 1, 1, 1],), expected=2, description="All equal - can rob at most 2 houses"
    ),
]


def test_solution():
    """Test the circular house robber solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.rob, TEST_CASES)


# Register the problem
register_problem(
    slug="house_robber_ii",
    leetcode_num=213,
    title="House Robber II",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_1D,
    solution_func=Solution().rob,
    test_func=test_solution,
    demo_func=create_demo_output,
)
