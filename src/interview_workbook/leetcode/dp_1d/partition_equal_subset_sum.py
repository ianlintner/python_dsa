"""
LeetCode 416: Partition Equal Subset Sum

Given a non-empty array nums containing only positive integers, find if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal.

Time Complexity: O(n * sum)
Space Complexity: O(sum)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        """
        Optimized DP approach using space-optimized subset sum.

        Key insight: If we can partition the array into two equal subsets,
        then each subset must have sum = total_sum / 2.

        This reduces to the subset sum problem: can we find a subset
        with sum = total_sum / 2?

        Space optimization: We only need to track which sums are possible,
        not how to achieve them.

        Time: O(n * sum) - For each number, update all possible sums
        Space: O(sum) - Boolean array for possible sums
        """
        total = sum(nums)

        # If total sum is odd, cannot partition into two equal subsets
        if total % 2 != 0:
            return False

        target = total // 2

        # dp[i] = True if sum i is achievable
        dp = [False] * (target + 1)
        dp[0] = True  # Base case: sum 0 is always achievable (empty subset)

        for num in nums:
            # Traverse backwards to avoid using the same element multiple times
            for j in range(target, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]

        return dp[target]

    def canPartitionDP2D(self, nums: List[int]) -> bool:
        """
        2D DP approach for clearer understanding.

        dp[i][j] = True if we can achieve sum j using first i elements

        Time: O(n * sum) - Fill 2D table
        Space: O(n * sum) - 2D DP array
        """
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        n = len(nums)

        # dp[i][j] = can achieve sum j using nums[0...i-1]
        dp = [[False] * (target + 1) for _ in range(n + 1)]

        # Base case: sum 0 is achievable with any number of elements
        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            for j in range(1, target + 1):
                # Don't include current element
                dp[i][j] = dp[i - 1][j]

                # Include current element if possible
                if nums[i - 1] <= j:
                    dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]

        return dp[n][target]

    def canPartitionRecursive(self, nums: List[int]) -> bool:
        """
        Recursive approach with memoization.

        For each element, we have two choices: include it or not.
        We recursively check if we can achieve the target sum.

        Time: O(n * sum) - Each subproblem solved once
        Space: O(n * sum) - Recursion stack + memoization
        """
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        memo = {}

        def can_achieve_sum(index, remaining_sum):
            if remaining_sum == 0:
                return True
            if index >= len(nums) or remaining_sum < 0:
                return False

            if (index, remaining_sum) in memo:
                return memo[(index, remaining_sum)]

            # Choice 1: Include current element
            include = can_achieve_sum(index + 1, remaining_sum - nums[index])

            # Choice 2: Exclude current element
            exclude = can_achieve_sum(index + 1, remaining_sum)

            result = include or exclude
            memo[(index, remaining_sum)] = result
            return result

        return can_achieve_sum(0, target)

    def canPartitionBitset(self, nums: List[int]) -> bool:
        """
        Bitset optimization approach.

        Use bit manipulation to represent possible sums.
        For each number, shift the bitset to include new possible sums.

        Time: O(n * sum / w) where w is word size (typically 64)
        Space: O(sum / w) - Bitset representation
        """
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2

        # Use integer as bitset (Python supports arbitrary precision)
        possible = 1  # Bit 0 set (sum 0 is possible)

        for num in nums:
            # For each existing possible sum, we can also achieve sum + num
            possible |= possible << num

        # Check if bit at position 'target' is set
        return (possible >> target) & 1


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different partition scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        ([1, 5, 11, 5], True),
        ([1, 2, 3, 5], False),
        ([1, 2, 5], False),
        ([1, 1], True),
        ([1, 1, 1, 1], True),
        ([2, 2, 1, 1], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([100], False),
    ]

    for nums, _expected in test_cases:
        result = solution.canPartition(nums)
        total = sum(nums)

        demos.append(f"Array: {nums}")
        demos.append(f"Total sum: {total}")
        demos.append(f"Can partition: {result}")

        if total % 2 == 0:
            target = total // 2
            demos.append(f"Target sum per subset: {target}")

            if result:
                # Try to find one possible partition
                demos.append("Analysis: Partition is possible")
                # For demonstration, we could show one valid partition
                # but this would require additional logic
            else:
                demos.append("Analysis: No valid partition exists")
        else:
            demos.append("Analysis: Odd total sum → impossible to partition")

        demos.append("")

    # Show DP table construction for small example
    demos.append("=== DP Table Construction Example ===")
    example_nums = [1, 5, 11, 5]
    example_total = sum(example_nums)
    example_target = example_total // 2

    demos.append(f"Array: {example_nums}")
    demos.append(f"Target sum: {example_target}")
    demos.append("")

    # Build DP table step by step
    dp = [False] * (example_target + 1)
    dp[0] = True

    demos.append("Initial DP state: dp[0] = True")
    demos.append(f"DP array: {dp}")
    demos.append("")

    for _i, num in enumerate(example_nums):
        old_dp = dp.copy()

        # Update DP array
        for j in range(example_target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]

        demos.append(f"After processing num = {num}:")
        demos.append(f"  Old DP: {old_dp}")
        demos.append(f"  New DP: {dp}")

        # Show which new sums became possible
        new_possible = [j for j in range(len(dp)) if dp[j] and not old_dp[j]]
        if new_possible:
            demos.append(f"  New possible sums: {new_possible}")
        demos.append("")

    # Algorithm comparison
    demos.append("=== Algorithm Analysis ===")
    demos.append("Problem Reduction:")
    demos.append("- Partition into two equal subsets ↔ Subset sum = total/2")
    demos.append("- This transforms the problem into classic subset sum")
    demos.append("- Much easier to reason about and implement")
    demos.append("")

    demos.append("DP State Definition:")
    demos.append("- dp[j] = True if sum j is achievable")
    demos.append("- Recurrence: dp[j] = dp[j] OR dp[j-num] (if j >= num)")
    demos.append("- Base case: dp[0] = True (empty subset has sum 0)")
    demos.append("- Process elements one by one, updating possible sums")
    demos.append("")

    demos.append("Space Optimization:")
    demos.append("- 2D DP: O(n * sum) space")
    demos.append("- 1D DP: O(sum) space")
    demos.append("- Bitset: O(sum/w) space where w = word size")
    demos.append("- Key insight: only need previous row to compute current row")
    demos.append("")

    # Show why we traverse backwards
    demos.append("=== Why Traverse Backwards? ===")
    demos.append("When updating dp[j] = dp[j] OR dp[j-num]:")
    demos.append("- Forward traversal: might use same element multiple times")
    demos.append("- Backward traversal: ensures each element used at most once")
    demos.append("")
    demos.append("Example with num = 3:")
    demos.append("Forward (WRONG): dp[3] = dp[0] → True, then dp[6] = dp[3] → True")
    demos.append("  This uses element 3 twice to get sum 6")
    demos.append("Backward (CORRECT): dp[6] = dp[3], then dp[3] = dp[0]")
    demos.append("  Each sum computed using current element at most once")
    demos.append("")

    # Performance comparison
    import time

    medium_nums = [i for i in range(1, 21)]  # Sum = 210, target = 105 (possible)

    # Time 1D DP approach
    start_time = time.time()
    for _ in range(1000):
        solution.canPartition(medium_nums)
    dp_time = time.time() - start_time

    # Time 2D DP approach
    start_time = time.time()
    for _ in range(100):
        solution.canPartitionDP2D(medium_nums)
    dp2d_time = time.time() - start_time

    # Time bitset approach
    start_time = time.time()
    for _ in range(1000):
        solution.canPartitionBitset(medium_nums)
    bitset_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"1D DP (1000 runs): {dp_time:.6f}s")
    demos.append(f"2D DP (100 runs): {dp2d_time:.6f}s")
    demos.append(f"Bitset (1000 runs): {bitset_time:.6f}s")
    demos.append("")
    demos.append("Time Complexity: O(n * sum) for all approaches")
    demos.append("Space Complexity:")
    demos.append("- 1D DP: O(sum)")
    demos.append("- 2D DP: O(n * sum)")
    demos.append("- Bitset: O(sum/w) where w is word size")
    demos.append("")

    # Edge cases and considerations
    demos.append("=== Edge Cases ===")
    demos.append("- Empty array: False (cannot partition nothing)")
    demos.append("- Single element: False (need two non-empty subsets)")
    demos.append("- Odd total sum: False (cannot split odd sum evenly)")
    demos.append("- All zeros: True (both subsets have sum 0)")
    demos.append("- Large numbers: may cause memory issues with large target")
    demos.append("")

    # Problem variations
    demos.append("=== Problem Variations ===")
    demos.append("- Subset Sum: find subset with exact sum")
    demos.append("- Partition to K Equal Sum Subsets: generalization")
    demos.append("- Minimum Subset Sum Difference: minimize |sum1 - sum2|")
    demos.append("- Target Sum: assign +/- to achieve target")
    demos.append("- 0/1 Knapsack: maximize value within weight limit")
    demos.append("- Coin Change: minimum coins to make amount")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Load balancing: distribute tasks equally across servers")
    demos.append("- Resource allocation: divide resources fairly")
    demos.append("- Game theory: fair division of assets")
    demos.append("- Scheduling: balance workload across time periods")
    demos.append("- Portfolio management: balance investment categories")
    demos.append("- Sports: create balanced teams")
    demos.append("- Manufacturing: optimize production line balancing")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(
        input_args=([1, 5, 11, 5],),
        expected=True,
        description="Can partition into [1,5,5] and [11]",
    ),
    TestCase(input_args=([1, 2, 3, 5],), expected=False, description="Cannot partition evenly"),
    TestCase(input_args=([1, 2, 5],), expected=False, description="Odd sum cannot be partitioned"),
    TestCase(input_args=([1, 1],), expected=True, description="Simple equal elements"),
    TestCase(input_args=([1, 1, 1, 1],), expected=True, description="Four equal elements"),
    TestCase(
        input_args=([2, 2, 1, 1],), expected=True, description="Can partition into [2,1] and [2,1]"
    ),
    TestCase(
        input_args=([1, 2, 3, 4, 5, 6, 7],),
        expected=True,
        description="Sum=28, can partition into sum=14 each",
    ),
    TestCase(
        input_args=([100],), expected=False, description="Single element cannot be partitioned"
    ),
    TestCase(
        input_args=(
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
        ),
        expected=True,
        description="100 ones - even count",
    ),
    TestCase(
        input_args=([3, 3, 3, 4, 5],),
        expected=True,
        description="Can partition into [3,3,4] and [3,5]",
    ),
]


def test_solution():
    """Test the partition equal subset sum solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.canPartition, TEST_CASES)


# Register the problem
register_problem(
    slug="partition_equal_subset_sum",
    leetcode_num=416,
    title="Partition Equal Subset Sum",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_1D,
    solution_func=Solution().canPartition,
    test_func=test_solution,
    demo_func=create_demo_output,
)
