"""
LeetCode 55: Jump Game

You are given an integer array nums. You are initially positioned at the array's
first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """
        Greedy approach: Track the maximum reachable index.

        At each position, we update the maximum index we can reach.
        If we can reach the current position and it extends our reach,
        we update our maximum reach. If at any point we can't reach
        the current position, we return False.

        Time: O(n) - Single pass through array
        Space: O(1) - Only using constant extra space
        """
        max_reach = 0

        for i in range(len(nums)):
            # If current position is beyond our reach, we can't continue
            if i > max_reach:
                return False

            # Update maximum reach from current position
            max_reach = max(max_reach, i + nums[i])

            # Early termination: if we can reach the end, return True
            if max_reach >= len(nums) - 1:
                return True

        return True

    def canJumpBacktrack(self, nums: List[int]) -> bool:
        """
        Alternative: Backtracking approach (less efficient).

        This explores all possible jump paths but has exponential time complexity.
        Included for educational purposes to show the brute force approach.

        Time: O(2^n) - Exponential due to exploring all paths
        Space: O(n) - Recursion stack depth
        """

        def backtrack(position):
            if position >= len(nums) - 1:
                return True

            for jump in range(1, nums[position] + 1):
                if backtrack(position + jump):
                    return True

            return False

        return backtrack(0)


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different jump game scenarios.
    """
    solution = Solution()

    demos = []

    # Test case 1: Can reach end
    nums1 = [2, 3, 1, 1, 4]
    result1 = solution.canJump(nums1)
    demos.append(f"Input: {nums1}")
    demos.append(f"Can jump to end: {result1}")
    demos.append("Path: 0→1→4 or 0→2→3→4")
    demos.append("")

    # Test case 2: Cannot reach end
    nums2 = [3, 2, 1, 0, 4]
    result2 = solution.canJump(nums2)
    demos.append(f"Input: {nums2}")
    demos.append(f"Can jump to end: {result2}")
    demos.append("Analysis: Get stuck at index 3 (value 0)")
    demos.append("")

    # Test case 3: Single element
    nums3 = [0]
    result3 = solution.canJump(nums3)
    demos.append(f"Input: {nums3}")
    demos.append(f"Can jump to end: {result3}")
    demos.append("Analysis: Already at the end")
    demos.append("")

    # Test case 4: Large jumps
    nums4 = [5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0]
    result4 = solution.canJump(nums4)
    demos.append(f"Input: {nums4}")
    demos.append(f"Can jump to end: {result4}")
    demos.append("Analysis: Can make large jumps to skip obstacles")
    demos.append("")

    # Algorithm analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Greedy Strategy:")
    demos.append("1. Track maximum reachable index at each step")
    demos.append("2. If current position > max_reach, return False")
    demos.append("3. Update max_reach = max(max_reach, i + nums[i])")
    demos.append("4. Early termination when max_reach >= len(nums) - 1")
    demos.append("")

    # Performance comparison
    import time

    large_array = [1] * 1000 + [0, 1000]  # Can reach end with big jump at end

    # Time greedy approach
    start_time = time.time()
    for _ in range(1000):
        solution.canJump(large_array)
    greedy_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Greedy approach (1000 runs): {greedy_time:.6f}s")
    demos.append("Time Complexity: O(n)")
    demos.append("Space Complexity: O(1)")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Game AI pathfinding with jump mechanics")
    demos.append("- Resource allocation with capacity constraints")
    demos.append("- Network routing with hop limits")
    demos.append("- Memory allocation with segment sizes")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(
        input=[[2, 3, 1, 1, 4]], expected=True, description="Can reach end with multiple paths"
    ),
    TestCase(input=[[3, 2, 1, 0, 4]], expected=False, description="Cannot pass zero barrier"),
    TestCase(input=[[0]], expected=True, description="Single element array - already at end"),
    TestCase(input=[[2, 0, 0]], expected=True, description="Can jump over zeros"),
    TestCase(
        input=[[1, 0, 1, 0]], expected=False, description="Cannot reach end due to zero barrier"
    ),
    TestCase(
        input=[[5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0]],
        expected=True,
        description="Large jumps can skip obstacles",
    ),
    TestCase(input=[[1, 1, 1, 1, 1]], expected=True, description="All ones - can always advance"),
    TestCase(
        input=[[4, 3, 2, 1, 0]], expected=True, description="Decreasing sequence that still works"
    ),
]


def test_solution():
    """Test the jump game solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.canJump, TEST_CASES)


# Register the problem
register_problem(
    slug="jump_game",
    leetcode_num=55,
    title="Jump Game",
    difficulty=Difficulty.MEDIUM,
    category=Category.GREEDY,
    solution_func=Solution().canJump,
    test_func=test_solution,
    demo_func=create_demo_output,
)
