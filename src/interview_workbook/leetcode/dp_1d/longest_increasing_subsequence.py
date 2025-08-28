"""
LeetCode 300: Longest Increasing Subsequence

Given an integer array nums, return the length of the longest strictly increasing subsequence.

Time Complexity: O(n log n) with binary search
Space Complexity: O(n)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Optimized approach using binary search and patience sorting.

        Key insight: Maintain an array where tails[i] is the smallest tail
        of all increasing subsequences of length i+1.

        For each number, find the position where it should be placed using
        binary search and update the tails array.

        Time: O(n log n) - Binary search for each element
        Space: O(n) - Tails array
        """
        if not nums:
            return 0

        # tails[i] = smallest tail of all increasing subsequences of length i+1
        tails = []

        for num in nums:
            # Binary search for the position to insert/replace
            left, right = 0, len(tails)

            while left < right:
                mid = (left + right) // 2
                if tails[mid] < num:
                    left = mid + 1
                else:
                    right = mid

            # If left == len(tails), we're extending the sequence
            if left == len(tails):
                tails.append(num)
            else:
                # Replace with smaller value to keep subsequence potential
                tails[left] = num

        return len(tails)

    def lengthOfLISDP(self, nums: List[int]) -> int:
        """
        Classic DP approach with O(n²) complexity.

        dp[i] = length of longest increasing subsequence ending at index i
        dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

        Time: O(n²) - Nested loops to check all previous elements
        Space: O(n) - DP array
        """
        if not nums:
            return 0

        n = len(nums)
        dp = [1] * n  # Each element forms a subsequence of length 1

        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    def lengthOfLISRecursive(self, nums: List[int]) -> int:
        """
        Recursive approach with memoization.

        For each position, we can either include or exclude the current element
        in our subsequence, depending on whether it maintains the increasing property.

        Time: O(n²) - Each subproblem solved once
        Space: O(n²) - Memoization table
        """
        if not nums:
            return 0

        memo = {}

        def lis_ending_at(i, prev_val):
            if i >= len(nums):
                return 0

            if (i, prev_val) in memo:
                return memo[(i, prev_val)]

            # Option 1: Skip current element
            exclude = lis_ending_at(i + 1, prev_val)

            # Option 2: Include current element (if possible)
            include = 0
            if nums[i] > prev_val:
                include = 1 + lis_ending_at(i + 1, nums[i])

            result = max(exclude, include)
            memo[(i, prev_val)] = result
            return result

        return lis_ending_at(0, float("-inf"))

    def lengthOfLISWithSequence(self, nums: List[int]) -> tuple[int, List[int]]:
        """
        Extended version that also returns the actual longest increasing subsequence.

        Uses the same binary search approach but tracks parent pointers
        to reconstruct the sequence.

        Time: O(n log n) - Binary search for each element
        Space: O(n) - Additional arrays for tracking
        """
        if not nums:
            return 0, []

        tails = []
        # Store the actual elements and their positions
        dp_indices = []  # dp_indices[i] stores the index in nums for tails[i]
        parent = [-1] * len(nums)  # parent[i] stores the previous element index in LIS

        for i, num in enumerate(nums):
            # Binary search for position
            left, right = 0, len(tails)
            while left < right:
                mid = (left + right) // 2
                if tails[mid] < num:
                    left = mid + 1
                else:
                    right = mid

            # Update parent pointer
            if left > 0:
                parent[i] = dp_indices[left - 1]

            # Update tails and dp_indices
            if left == len(tails):
                tails.append(num)
                dp_indices.append(i)
            else:
                tails[left] = num
                dp_indices[left] = i

        # Reconstruct the sequence
        lis_length = len(tails)
        if lis_length == 0:
            return 0, []

        # Start from the last element and trace back
        sequence = []
        current_idx = dp_indices[-1]

        while current_idx != -1:
            sequence.append(nums[current_idx])
            current_idx = parent[current_idx]

        sequence.reverse()
        return lis_length, sequence


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different LIS scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7, 7, 7, 7, 7, 7, 7], 1),
        ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),
        ([10, 2, 3], 2),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
    ]

    for nums, _expected in test_cases:
        result = solution.lengthOfLIS(nums)
        length, sequence = solution.lengthOfLISWithSequence(nums)

        demos.append(f"Array: {nums}")
        demos.append(f"LIS length: {result}")
        demos.append(f"One possible LIS: {sequence}")

        # Show DP table for smaller examples
        if len(nums) <= 8:
            dp = [1] * len(nums)
            for i in range(1, len(nums)):
                for j in range(i):
                    if nums[j] < nums[i]:
                        dp[i] = max(dp[i], dp[j] + 1)

            demos.append("DP values (length ending at each index):")
            demos.append(f"  {dp}")

        demos.append("")

    # Algorithm comparison and analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Binary Search Approach (Patience Sorting):")
    demos.append("1. Maintain array 'tails' where tails[i] = smallest ending value")
    demos.append("   of all increasing subsequences of length i+1")
    demos.append("2. For each number, find position using binary search")
    demos.append("3. Either extend sequence or replace to keep smaller tail")
    demos.append("4. Length of 'tails' array is the LIS length")
    demos.append("")

    demos.append("Why Binary Search Works:")
    demos.append("- tails array is always sorted (key invariant)")
    demos.append("- Replacing larger tail with smaller one never decreases optimal length")
    demos.append("- Smaller tails give more opportunities for future extensions")
    demos.append("- Binary search finds exact position to maintain sorted property")
    demos.append("")

    # Show step-by-step binary search process
    demos.append("=== Step-by-Step Example ===")
    example = [10, 9, 2, 5, 3, 7, 101, 18]
    demos.append(f"Array: {example}")

    tails = []
    for i, num in enumerate(example):
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid

        action = "append" if left == len(tails) else f"replace tails[{left}]"
        old_tails = tails.copy()

        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num

        demos.append(f"Step {i + 1}: num={num}")
        demos.append(f"  Before: tails = {old_tails}")
        demos.append(f"  Action: {action}")
        demos.append(f"  After:  tails = {tails}")
        demos.append("")

    # Performance comparison
    import time

    large_array = list(range(1000, 0, -1)) + list(range(1, 1001))  # Challenging case

    # Time binary search approach
    start_time = time.time()
    for _ in range(100):
        solution.lengthOfLIS(large_array)
    binary_time = time.time() - start_time

    # Time DP approach (smaller array to avoid timeout)
    medium_array = list(range(100, 0, -1)) + list(range(1, 101))
    start_time = time.time()
    for _ in range(100):
        solution.lengthOfLISDP(medium_array)
    dp_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Binary search O(n log n) (100 runs, 2000 elements): {binary_time:.6f}s")
    demos.append(f"DP O(n²) (100 runs, 200 elements): {dp_time:.6f}s")
    demos.append("")
    demos.append("Space complexity:")
    demos.append("- Binary search: O(n) - tails array")
    demos.append("- DP: O(n) - dp array")
    demos.append("- Recursive: O(n²) - memoization table")
    demos.append("")

    # Pattern analysis
    demos.append("=== Common Patterns ===")

    patterns = [
        ("Strictly increasing", [1, 2, 3, 4, 5]),
        ("Strictly decreasing", [5, 4, 3, 2, 1]),
        ("All equal", [3, 3, 3, 3, 3]),
        ("Mountain shape", [1, 2, 4, 3, 5, 6]),
        ("Random order", [3, 1, 4, 1, 5, 9, 2, 6]),
    ]

    for pattern_name, arr in patterns:
        lis_len, lis_seq = solution.lengthOfLISWithSequence(arr)
        demos.append(f"{pattern_name}: {arr}")
        demos.append(f"  LIS length: {lis_len}, sequence: {lis_seq}")

    demos.append("")

    # Applications and extensions
    demos.append("=== Applications & Extensions ===")
    demos.append("Core Applications:")
    demos.append("- Stock price analysis (longest increasing trend)")
    demos.append("- Sequence alignment in bioinformatics")
    demos.append("- Scheduling optimization (task ordering)")
    demos.append("- Box stacking problems")
    demos.append("- Russian doll envelope problem")
    demos.append("")

    demos.append("Problem Variations:")
    demos.append("- Longest decreasing subsequence (reverse array)")
    demos.append("- Longest non-decreasing subsequence (≤ instead of <)")
    demos.append("- Longest bitonic subsequence (increase then decrease)")
    demos.append("- Longest common subsequence (2D version)")
    demos.append("- Maximum sum increasing subsequence")
    demos.append("")

    demos.append("Advanced Extensions:")
    demos.append("- Count number of LIS (LeetCode 673)")
    demos.append("- Print all possible LIS")
    demos.append("- LIS in 2D (Russian doll envelopes)")
    demos.append("- Online LIS (elements arrive one by one)")
    demos.append("- LIS with constraints (bounded differences)")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input_args=([10, 9, 2, 5, 3, 7, 101, 18],), expected=4, description="Standard LIS example"),
    TestCase(input_args=([0, 1, 0, 3, 2, 3],), expected=4, description="LIS: [0,1,2,3]"),
    TestCase(input_args=([7, 7, 7, 7, 7, 7, 7],), expected=1, description="All equal elements"),
    TestCase(
        input_args=([1, 3, 6, 7, 9, 4, 10, 5, 6],), expected=6, description="LIS: [1,3,4,5,6] or similar"
    ),
    TestCase(input_args=([10, 2, 3],), expected=2, description="Simple case: [2,3]"),
    TestCase(input_args=([1, 2, 3, 4, 5],), expected=5, description="Already sorted increasing"),
    TestCase(input_args=([5, 4, 3, 2, 1],), expected=1, description="Decreasing sequence"),
    TestCase(input_args=([1],), expected=1, description="Single element"),
    TestCase(input_args=([],), expected=0, description="Empty array"),
    TestCase(input_args=([2, 2],), expected=1, description="Duplicate elements"),
    TestCase(input_args=([1, 3, 2, 4],), expected=3, description="LIS: [1,2,4] or [1,3,4]"),
]


def test_solution():
    """Test the longest increasing subsequence solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.lengthOfLIS, TEST_CASES)


# Register the problem
register_problem(
    slug="longest_increasing_subsequence",
    leetcode_num=300,
    title="Longest Increasing Subsequence",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_1D,
    solution_func=Solution().lengthOfLIS,
    test_func=test_solution,
    demo_func=create_demo_output,
)
