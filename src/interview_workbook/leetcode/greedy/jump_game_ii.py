"""
LeetCode 45: Jump Game II

You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
Each element nums[i] represents the maximum length of a forward jump from index i.

Return the minimum number of jumps to reach nums[n - 1].

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        Greedy approach: Track the farthest reachable position and current jump boundary.

        We maintain two pointers:
        - current_end: The farthest index we can reach with current number of jumps
        - farthest: The farthest index we can reach with one more jump

        When we reach current_end, we increment jumps and update current_end to farthest.

        Time: O(n) - Single pass through array
        Space: O(1) - Only using constant extra space
        """
        if len(nums) <= 1:
            return 0

        jumps = 0
        current_end = 0  # Boundary of current jump level
        farthest = 0  # Farthest reachable with one more jump

        # We don't need to consider the last index since we want to reach it
        for i in range(len(nums) - 1):
            # Update the farthest we can reach from current position
            farthest = max(farthest, i + nums[i])

            # If we've reached the end of current jump level
            if i == current_end:
                jumps += 1
                current_end = farthest

                # Early termination: if we can reach the end, no need to continue
                if current_end >= len(nums) - 1:
                    break

        return jumps

    def jumpBFS(self, nums: List[int]) -> int:
        """
        Alternative: BFS approach (less efficient but more intuitive).

        Treat each position as a node in a graph, and each possible jump as an edge.
        Use BFS to find the shortest path (minimum jumps) to the last index.

        Time: O(n²) - In worst case, we might visit all positions multiple times
        Space: O(n) - Queue can contain up to n positions
        """
        if len(nums) <= 1:
            return 0

        from collections import deque

        queue = deque([(0, 0)])  # (position, jumps)
        visited = set([0])

        while queue:
            pos, jumps = queue.popleft()

            # If we've reached the end
            if pos >= len(nums) - 1:
                return jumps

            # Try all possible jumps from current position
            for jump in range(1, nums[pos] + 1):
                next_pos = pos + jump
                if next_pos not in visited and next_pos < len(nums):
                    visited.add(next_pos)
                    queue.append((next_pos, jumps + 1))

        return -1  # Should never reach here if input is valid

    def jumpDP(self, nums: List[int]) -> int:
        """
        Alternative: Dynamic Programming approach.

        dp[i] represents minimum jumps needed to reach position i.
        For each position, try all possible jumps and update reachable positions.

        Time: O(n²) - For each position, we check all possible jumps
        Space: O(n) - DP array
        """
        if len(nums) <= 1:
            return 0

        dp = [float("inf")] * len(nums)
        dp[0] = 0

        for i in range(len(nums)):
            if dp[i] == float("inf"):
                continue

            # Try all possible jumps from position i
            for jump in range(1, nums[i] + 1):
                if i + jump < len(nums):
                    dp[i + jump] = min(dp[i + jump], dp[i] + 1)

        return dp[-1]


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different jump game scenarios.
    """
    solution = Solution()

    demos = []

    # Test case 1: Multiple optimal paths
    nums1 = [2, 3, 1, 1, 4]
    result1 = solution.jump(nums1)
    demos.append(f"Input: {nums1}")
    demos.append(f"Minimum jumps: {result1}")
    demos.append("Optimal path: 0→1→4 (2 jumps)")
    demos.append("")

    # Test case 2: Large jumps available
    nums2 = [2, 3, 0, 1, 4]
    result2 = solution.jump(nums2)
    demos.append(f"Input: {nums2}")
    demos.append(f"Minimum jumps: {result2}")
    demos.append("Optimal path: 0→1→4 (2 jumps)")
    demos.append("")

    # Test case 3: Single element
    nums3 = [0]
    result3 = solution.jump(nums3)
    demos.append(f"Input: {nums3}")
    demos.append(f"Minimum jumps: {result3}")
    demos.append("Analysis: Already at destination")
    demos.append("")

    # Test case 4: Greedy vs non-greedy choice
    nums4 = [
        5,
        6,
        4,
        4,
        6,
        9,
        4,
        4,
        7,
        4,
        4,
        8,
        2,
        6,
        8,
        1,
        5,
        9,
        6,
        5,
        2,
        7,
        9,
        7,
        9,
        6,
        9,
        4,
        1,
        6,
        8,
        8,
        4,
        4,
        2,
        0,
        3,
        8,
        5,
    ]
    result4 = solution.jump(nums4)
    demos.append(f"Input: Large array with {len(nums4)} elements")
    demos.append(f"Minimum jumps: {result4}")
    demos.append("Analysis: Greedy approach finds optimal solution efficiently")
    demos.append("")

    # Algorithm analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Greedy Strategy:")
    demos.append("1. Track current jump boundary (current_end)")
    demos.append("2. Track farthest reachable position (farthest)")
    demos.append("3. When reaching current_end, increment jumps")
    demos.append("4. Update current_end to farthest")
    demos.append("5. Early termination when farthest >= len(nums) - 1")
    demos.append("")

    demos.append("Key Insight:")
    demos.append("- At each level, we can reach all positions within current boundary")
    demos.append("- We only increment jumps when we must move to next level")
    demos.append("- This ensures minimum jumps while maintaining O(n) complexity")
    demos.append("")

    # Performance comparison
    import time

    large_array = [1] * 1000 + [1000]  # Large array where each position can jump 1 step

    # Time greedy approach
    start_time = time.time()
    for _ in range(1000):
        solution.jump(large_array)
    greedy_time = time.time() - start_time

    # Time DP approach (smaller array for reasonable runtime)
    small_array = [1] * 100
    start_time = time.time()
    for _ in range(100):
        solution.jumpDP(small_array)
    dp_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Greedy approach (1000 runs, 1001 elements): {greedy_time:.6f}s")
    demos.append(f"DP approach (100 runs, 100 elements): {dp_time:.6f}s")
    demos.append("Greedy: O(n) time, O(1) space")
    demos.append("DP: O(n²) time, O(n) space")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Network packet routing with minimum hops")
    demos.append("- Game speedrun optimization")
    demos.append("- Resource allocation with capacity constraints")
    demos.append("- Path planning in robotics")
    demos.append("- Compiler optimization for instruction scheduling")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input=[[2, 3, 1, 1, 4]], expected=2, description="Standard case with multiple paths"),
    TestCase(input=[[2, 3, 0, 1, 4]], expected=2, description="Large jump bypasses zero"),
    TestCase(input=[[0]], expected=0, description="Single element - no jumps needed"),
    TestCase(
        input=[[1, 1, 1, 1]], expected=3, description="All ones - need 3 jumps for 4 elements"
    ),
    TestCase(input=[[2, 1]], expected=1, description="Two elements - one jump"),
    TestCase(input=[[1, 2, 3]], expected=2, description="Increasing sequence"),
    TestCase(input=[[3, 2, 1]], expected=1, description="Can jump directly to end"),
    TestCase(input=[[1, 1, 1, 1, 1, 1]], expected=5, description="Long sequence of ones"),
    TestCase(input=[[4, 1, 1, 3, 1, 1, 1]], expected=2, description="Large initial jump"),
]


def test_solution():
    """Test the jump game II solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.jump, TEST_CASES)


# Register the problem
register_problem(
    slug="jump_game_ii",
    leetcode_num=45,
    title="Jump Game II",
    difficulty=Difficulty.MEDIUM,
    category=Category.GREEDY,
    solution_func=Solution().jump,
    test_func=test_solution,
    demo_func=create_demo_output,
)
