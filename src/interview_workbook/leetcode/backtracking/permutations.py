"""
LeetCode 46: Permutations

Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]

Example 3:
Input: nums = [1]
Output: [[1]]

Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.
"""

from typing import List
from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all permutations using backtracking.

        Key insight: At each position, try all unused elements. Use a set or
        boolean array to track which elements have been used in current permutation.

        Time: O(n! * n) where n = len(nums). There are n! permutations, each takes O(n) to copy.
        Space: O(n) for recursion depth and current permutation, plus O(n! * n) for output.

        Args:
            nums: Array of distinct integers

        Returns:
            List of all possible permutations
        """
        result = []

        def backtrack(current_permutation: List[int], used: set) -> None:
            """Backtrack helper to generate all permutations."""
            # Base case: permutation is complete
            if len(current_permutation) == len(nums):
                result.append(current_permutation[:])
                return

            # Try each unused number at current position
            for num in nums:
                if num not in used:
                    # Choose: add current number
                    current_permutation.append(num)
                    used.add(num)

                    # Explore: recurse to fill next position
                    backtrack(current_permutation, used)

                    # Unchoose: remove current number
                    current_permutation.pop()
                    used.remove(num)

        backtrack([], set())
        return result

    def permuteSwap(self, nums: List[int]) -> List[List[int]]:
        """
        Generate permutations using swap-based backtracking.

        More space-efficient approach: modify nums in-place by swapping elements.
        At position i, try placing each element from position i to end.

        Time: O(n! * n) - same as above
        Space: O(n) recursion depth only (not counting output)
        """
        result = []

        def backtrack(start: int) -> None:
            """Generate permutations by swapping elements."""
            # Base case: all positions filled
            if start == len(nums):
                result.append(nums[:])  # Copy current state
                return

            # Try placing each remaining element at position 'start'
            for i in range(start, len(nums)):
                # Choose: swap element at position i to position start
                nums[start], nums[i] = nums[i], nums[start]

                # Explore: recurse to fill next position
                backtrack(start + 1)

                # Unchoose: swap back to restore original order
                nums[start], nums[i] = nums[i], nums[start]

        backtrack(0)
        return result

    def permuteIterative(self, nums: List[int]) -> List[List[int]]:
        """
        Generate permutations iteratively.

        Build permutations level by level. For each existing permutation,
        insert the next element at every possible position.

        Time: O(n! * n^2) due to insertion operations
        Space: O(n! * n) for storing intermediate results
        """
        result = [[]]  # Start with empty permutation

        for num in nums:
            new_result = []
            # For each existing permutation
            for perm in result:
                # Insert current number at every possible position
                for i in range(len(perm) + 1):
                    new_perm = perm[:i] + [num] + perm[i:]
                    new_result.append(new_perm)
            result = new_result

        return result

    def permuteHeaps(self, nums: List[int]) -> List[List[int]]:
        """
        Generate permutations using Heap's algorithm.

        Heap's algorithm generates all permutations by making minimal changes
        (single swaps) between consecutive permutations.

        Time: O(n! * n) for generating and copying permutations
        Space: O(n) not counting output
        """
        result = []
        n = len(nums)

        def generate(k: int) -> None:
            """Generate permutations using Heap's algorithm."""
            if k == 1:
                result.append(nums[:])
                return

            generate(k - 1)

            for i in range(k - 1):
                # If k is even, swap i and k-1
                # If k is odd, swap 0 and k-1
                if k % 2 == 0:
                    nums[i], nums[k - 1] = nums[k - 1], nums[i]
                else:
                    nums[0], nums[k - 1] = nums[k - 1], nums[0]

                generate(k - 1)

        generate(n)
        return result


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to generating permutations.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 46: Permutations - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        ([1, 2, 3], "Classic 3-element example"),
        ([0, 1], "Simple 2-element case"),
        ([1], "Single element"),
        ([4, 3, 2, 1], "4 elements in reverse order"),
        ([-1, 0, 1], "Mix of negative, zero, positive"),
    ]

    for nums, description in test_cases:
        demo_parts.append(f"\nTest Case: {nums}")
        demo_parts.append(f"Description: {description}")

        # Show different approaches
        result1 = solution.permute(nums)
        result2 = solution.permuteSwap(nums[:])  # Pass copy since swap modifies input
        result3 = solution.permuteIterative(nums)
        result4 = solution.permuteHeaps(nums[:])  # Pass copy since Heap's modifies input

        # Sort results for consistent comparison (permutations can be in different orders)
        result1_sorted = sorted(result1)
        result2_sorted = sorted(result2)
        result3_sorted = sorted(result3)
        result4_sorted = sorted(result4)

        demo_parts.append(f"Backtracking result: {len(result1)} permutations")
        demo_parts.append(f"  {result1_sorted}")
        demo_parts.append(f"Swap-based result: {len(result2)} permutations")
        demo_parts.append(f"  {result2_sorted}")
        demo_parts.append(f"Iterative result: {len(result3)} permutations")
        demo_parts.append(f"  {result3_sorted}")
        demo_parts.append(f"Heap's algorithm result: {len(result4)} permutations")
        demo_parts.append(f"  {result4_sorted}")

        # Verify consistency
        consistent = result1_sorted == result2_sorted == result3_sorted == result4_sorted
        demo_parts.append(f"All approaches consistent: {consistent}")

        # Mathematical verification
        import math

        expected_count = math.factorial(len(nums))
        demo_parts.append(f"Expected permutations: {expected_count}")
        demo_parts.append(f"Actual permutations: {len(result1)}")
        demo_parts.append(f"Count correct: {len(result1) == expected_count}")

    # Algorithm analysis
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nBacktracking with Set:")
    demo_parts.append("  • Time: O(n! * n) - n! permutations, O(n) to copy each")
    demo_parts.append("  • Space: O(n) recursion + O(n) set + O(n! * n) output")
    demo_parts.append("  • Pros: Intuitive, easy to understand and debug")
    demo_parts.append("  • Cons: Extra space for tracking used elements")

    demo_parts.append("\nSwap-based Backtracking:")
    demo_parts.append("  • Time: O(n! * n) - same complexity")
    demo_parts.append("  • Space: O(n) recursion depth only (excluding output)")
    demo_parts.append("  • Pros: Space-efficient, in-place swapping")
    demo_parts.append("  • Cons: Modifies input array, slightly more complex logic")

    demo_parts.append("\nIterative Approach:")
    demo_parts.append("  • Time: O(n! * n^2) - quadratic due to list insertions")
    demo_parts.append("  • Space: O(n! * n) for storing all intermediate results")
    demo_parts.append("  • Pros: No recursion, clear step-by-step building")
    demo_parts.append("  • Cons: Higher time complexity, more memory usage")

    demo_parts.append("\nHeap's Algorithm:")
    demo_parts.append("  • Time: O(n! * n) - optimal for generating all permutations")
    demo_parts.append("  • Space: O(n) recursion depth")
    demo_parts.append("  • Pros: Minimal changes between permutations, classic algorithm")
    demo_parts.append("  • Cons: Less intuitive, specific to permutation generation")

    # Mathematical insights
    demo_parts.append("\n=== Mathematical Insights ===")
    demo_parts.append("Permutation count: n! = n × (n-1) × ... × 2 × 1")
    demo_parts.append("")
    demo_parts.append("Growth rate examples:")
    demo_parts.append("  • 3! = 6 permutations")
    demo_parts.append("  • 4! = 24 permutations")
    demo_parts.append("  • 5! = 120 permutations")
    demo_parts.append("  • 6! = 720 permutations")
    demo_parts.append("  • 10! = 3,628,800 permutations")
    demo_parts.append("")
    demo_parts.append("Factorial grows extremely rapidly - this is why the constraint")
    demo_parts.append("limits n ≤ 6 (keeping output size manageable).")

    # Permutation vs combination
    demo_parts.append("\n=== Permutations vs Combinations ===")
    demo_parts.append("Permutations: Order matters")
    demo_parts.append("  • [1,2,3] ≠ [3,2,1] (different permutations)")
    demo_parts.append("  • Count: P(n,k) = n!/(n-k)! for k-length permutations")
    demo_parts.append("  • Full permutations: P(n,n) = n!")
    demo_parts.append("")
    demo_parts.append("Combinations: Order doesn't matter")
    demo_parts.append("  • {1,2,3} = {3,2,1} (same combination)")
    demo_parts.append("  • Count: C(n,k) = n!/(k!(n-k)!) for k-element combinations")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. Task Scheduling: Different orders of executing tasks")
    demo_parts.append("2. Route Planning: All possible orderings of visiting locations")
    demo_parts.append("3. Password Generation: Permutations of characters")
    demo_parts.append("4. Tournament Brackets: Different matchup orders")
    demo_parts.append("5. Playlist Generation: All possible song orderings")
    demo_parts.append("6. Seating Arrangements: Different ways to seat people")
    demo_parts.append("7. Assembly Line: Different orders of production steps")

    # Optimization techniques
    demo_parts.append("\n=== Optimization Techniques ===")
    demo_parts.append("1. Early Termination: Stop when target found (if searching)")
    demo_parts.append("2. Pruning: Skip branches that can't lead to valid solutions")
    demo_parts.append("3. Memory Optimization: Use swap-based approach vs. extra space")
    demo_parts.append("4. Iterative vs Recursive: Trade stack space for explicit memory")
    demo_parts.append("5. Generator Pattern: Yield permutations one at a time vs. storing all")

    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        input_data={"nums": [1, 2, 3]},
        expected_output=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
        description="Classic 3-element example",
    ),
    TestCase(
        input_data={"nums": [0, 1]},
        expected_output=[[0, 1], [1, 0]],
        description="Simple 2-element case",
    ),
    TestCase(
        input_data={"nums": [1]},
        expected_output=[[1]],
        description="Single element - only one permutation",
    ),
    TestCase(
        input_data={"nums": [4, 3, 2, 1]},
        expected_output=[
            [1, 2, 3, 4],
            [1, 2, 4, 3],
            [1, 3, 2, 4],
            [1, 3, 4, 2],
            [1, 4, 2, 3],
            [1, 4, 3, 2],
            [2, 1, 3, 4],
            [2, 1, 4, 3],
            [2, 3, 1, 4],
            [2, 3, 4, 1],
            [2, 4, 1, 3],
            [2, 4, 3, 1],
            [3, 1, 2, 4],
            [3, 1, 4, 2],
            [3, 2, 1, 4],
            [3, 2, 4, 1],
            [3, 4, 1, 2],
            [3, 4, 2, 1],
            [4, 1, 2, 3],
            [4, 1, 3, 2],
            [4, 2, 1, 3],
            [4, 2, 3, 1],
            [4, 3, 1, 2],
            [4, 3, 2, 1],
        ],
        description="4 elements - 24 permutations",
    ),
    TestCase(
        input_data={"nums": [-1, 0, 1]},
        expected_output=[[-1, 0, 1], [-1, 1, 0], [0, -1, 1], [0, 1, -1], [1, -1, 0], [1, 0, -1]],
        description="Mix of negative, zero, positive",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def normalize_output(permutations):
        """Normalize output by sorting the list of permutations."""
        return sorted(permutations)

    def test_function(nums):
        solution = Solution()
        result = solution.permute(nums)
        return normalize_output(result)

    # Normalize expected outputs
    normalized_test_cases = []
    for case in TEST_CASES:
        normalized_case = TestCase(
            input_data=case.input_data,
            expected_output=normalize_output(case.expected_output),
            description=case.description,
        )
        normalized_test_cases.append(normalized_case)

    run_test_cases(test_function, normalized_test_cases)


# Register the problem
register_problem(
    slug="permutations",
    leetcode_num=46,
    title="Permutations",
    difficulty=Difficulty.MEDIUM,
    category=Category.BACKTRACKING,
    solution_func=Solution().permute,
    test_func=test_solution,
    demo_func=create_demo_output,
)
