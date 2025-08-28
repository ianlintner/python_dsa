"""
LeetCode 39: Combination Sum

Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen numbers sum to target.
You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.
Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to target
is less than 150 combinations for the given input.

Example 1:
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

Example 2:
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
Input: candidates = [2], target = 1
Output: []

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40
"""

from typing import List
from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations that sum to target using backtracking.

        Key insight: Since we can reuse elements, at each step we can either:
        1. Include the current element again (stay at same index)
        2. Move to the next element

        We sort candidates first to enable early termination when remaining
        target becomes smaller than current candidate.

        Time: O(N^(T/M)) where N = len(candidates), T = target, M = minimal candidate
        Space: O(T/M) for recursion depth, plus O(result_size) for output

        Args:
            candidates: Array of distinct positive integers
            target: Target sum to achieve

        Returns:
            List of all unique combinations that sum to target
        """
        result = []
        candidates.sort()  # Sort for early termination optimization

        def backtrack(start: int, current_combination: List[int], remaining: int) -> None:
            """Backtrack helper to find all combinations."""
            # Base case: found valid combination
            if remaining == 0:
                result.append(current_combination[:])
                return

            # Try each candidate starting from 'start' index
            for i in range(start, len(candidates)):
                candidate = candidates[i]

                # Early termination: if current candidate > remaining target,
                # all subsequent candidates will also be too large (since sorted)
                if candidate > remaining:
                    break

                # Choose: add current candidate
                current_combination.append(candidate)

                # Explore: recurse with same start index (can reuse same element)
                # and reduced remaining target
                backtrack(i, current_combination, remaining - candidate)

                # Unchoose: remove current candidate
                current_combination.pop()

        backtrack(0, [], target)
        return result

    def combinationSumDP(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find combinations using dynamic programming approach.

        Build up combinations for each target value from 1 to target.
        For each candidate, add it to all existing combinations that
        can accommodate it.

        Time: O(N * T * avg_combination_length)
        Space: O(T * total_combinations)
        """
        # dp[i] stores all combinations that sum to i
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]  # One way to make 0: empty combination

        # For each candidate, update all possible sums
        for candidate in candidates:
            for sum_val in range(candidate, target + 1):
                # Add current candidate to all combinations that sum to (sum_val - candidate)
                for combination in dp[sum_val - candidate]:
                    dp[sum_val].append(combination + [candidate])

        return dp[target]

    def combinationSumMemo(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find combinations using memoization (top-down DP).

        Cache results for each (start_index, remaining_target) pair to avoid
        recomputing the same subproblems.

        Time: O(N * T * avg_combination_length)
        Space: O(N * T) for memoization + recursion stack
        """
        from functools import lru_cache

        candidates.sort()

        @lru_cache(maxsize=None)
        def helper(start: int, remaining: int) -> List[tuple]:
            """Memoized helper returning combinations as tuples."""
            if remaining == 0:
                return [()]

            result = []
            for i in range(start, len(candidates)):
                candidate = candidates[i]
                if candidate > remaining:
                    break

                # Get all combinations for reduced problem
                sub_combinations = helper(i, remaining - candidate)

                # Add current candidate to each sub-combination
                for combo in sub_combinations:
                    result.append((candidate,) + combo)

            return result

        # Convert tuples back to lists
        return [list(combo) for combo in helper(0, target)]


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to combination sum.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 39: Combination Sum - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        ([2, 3, 6, 7], 7, "Classic example with multiple solutions"),
        ([2, 3, 5], 8, "Multiple ways to reach target"),
        ([2], 1, "Impossible case"),
        ([2, 7, 6, 3, 5, 1], 9, "Many candidates, medium target"),
        ([3, 5, 4], 8, "Simple case requiring multiple uses"),
    ]

    for candidates, target, description in test_cases:
        demo_parts.append(f"\nTest Case: {candidates}, target = {target}")
        demo_parts.append(f"Description: {description}")

        # Show different approaches
        result1 = solution.combinationSum(candidates, target)
        result2 = solution.combinationSumDP(candidates, target)
        result3 = solution.combinationSumMemo(candidates, target)

        # Sort results for consistent comparison
        result1_sorted = sorted([sorted(combo) for combo in result1])
        result2_sorted = sorted([sorted(combo) for combo in result2])
        result3_sorted = sorted([sorted(combo) for combo in result3])

        demo_parts.append(f"Backtracking result: {len(result1)} combinations")
        demo_parts.append(f"  {result1_sorted}")
        demo_parts.append(f"DP result: {len(result2)} combinations")
        demo_parts.append(f"  {result2_sorted}")
        demo_parts.append(f"Memoized result: {len(result3)} combinations")
        demo_parts.append(f"  {result3_sorted}")

        # Verify consistency
        consistent = result1_sorted == result2_sorted == result3_sorted
        demo_parts.append(f"All approaches consistent: {consistent}")

    # Algorithm analysis
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nBacktracking Approach:")
    demo_parts.append("  • Time: O(N^(T/M)) where N=candidates, T=target, M=min_candidate")
    demo_parts.append("  • Space: O(T/M) recursion depth")
    demo_parts.append("  • Pros: Intuitive, memory efficient during search")
    demo_parts.append("  • Cons: May recompute same subproblems")

    demo_parts.append("\nDynamic Programming Approach:")
    demo_parts.append("  • Time: O(N * T * avg_combination_length)")
    demo_parts.append("  • Space: O(T * total_combinations)")
    demo_parts.append("  • Pros: Bottom-up, clear state transitions")
    demo_parts.append("  • Cons: Higher memory usage, may generate duplicates")

    demo_parts.append("\nMemoized Approach:")
    demo_parts.append("  • Time: O(N * T * avg_combination_length)")
    demo_parts.append("  • Space: O(N * T) for cache + recursion stack")
    demo_parts.append("  • Pros: Avoids recomputation, cleaner than bottom-up DP")
    demo_parts.append("  • Cons: Overhead of memoization structure")

    # Mathematical insights
    demo_parts.append("\n=== Mathematical Insights ===")
    demo_parts.append("This problem is related to the 'Coin Change' problem but asks for")
    demo_parts.append("all combinations instead of just the count or minimum coins.")
    demo_parts.append("")
    demo_parts.append("Number of solutions grows exponentially with target size.")
    demo_parts.append(
        "For target T and minimum candidate M, worst case has O(N^(T/M)) combinations."
    )
    demo_parts.append("")
    demo_parts.append("Example: candidates=[1], target=4")
    demo_parts.append("Solutions: [1,1,1,1] - only 1 way")
    demo_parts.append("")
    demo_parts.append("Example: candidates=[1,2], target=4")
    demo_parts.append("Solutions: [1,1,1,1], [1,1,2], [2,2] - 3 ways")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. Currency/Coin Change: Find all ways to make change")
    demo_parts.append("2. Resource Allocation: Different ways to use available resources")
    demo_parts.append("3. Menu Combinations: Ways to reach price target with menu items")
    demo_parts.append("4. Knapsack Variations: All ways to fill knapsack to exact capacity")
    demo_parts.append("5. Chemistry: Different molecular combinations for target weight")
    demo_parts.append("6. Music: Different note combinations to create specific duration")

    # Edge cases and optimizations
    demo_parts.append("\n=== Edge Cases & Optimizations ===")
    demo_parts.append("Edge Cases:")
    demo_parts.append("  • target = 0: return [[]] (empty combination)")
    demo_parts.append("  • All candidates > target: return [] (no solution)")
    demo_parts.append("  • Single candidate that divides target: [candidate] * (target/candidate)")
    demo_parts.append("")
    demo_parts.append("Optimizations:")
    demo_parts.append("  • Sort candidates for early termination")
    demo_parts.append("  • Skip candidates larger than remaining target")
    demo_parts.append("  • Use memoization for overlapping subproblems")
    demo_parts.append("  • Consider pruning based on target/minimum_candidate ratio")

    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        input_data={"candidates": [2, 3, 6, 7], "target": 7},
        expected_output=[[2, 2, 3], [7]],
        description="Classic example with multiple solutions",
    ),
    TestCase(
        input_data={"candidates": [2, 3, 5], "target": 8},
        expected_output=[[2, 2, 2, 2], [2, 3, 3], [3, 5]],
        description="Multiple ways to reach target",
    ),
    TestCase(
        input_data={"candidates": [2], "target": 1},
        expected_output=[],
        description="Impossible case - target smaller than minimum candidate",
    ),
    TestCase(
        input_data={"candidates": [1], "target": 1},
        expected_output=[[1]],
        description="Single element exact match",
    ),
    TestCase(
        input_data={"candidates": [1], "target": 2},
        expected_output=[[1, 1]],
        description="Reusing single element multiple times",
    ),
    TestCase(
        input_data={"candidates": [3, 5, 4], "target": 8},
        expected_output=[[3, 5], [4, 4]],
        description="Simple case requiring multiple uses",
    ),
    TestCase(
        input_data={"candidates": [2, 7, 6, 3, 5, 1], "target": 9},
        expected_output=[
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 3],
            [1, 1, 1, 1, 1, 4],
            [1, 1, 1, 1, 5],
            [1, 1, 1, 2, 4],
            [1, 1, 1, 6],
            [1, 1, 2, 2, 3],
            [1, 1, 7],
            [1, 2, 2, 4],
            [1, 2, 6],
            [1, 3, 5],
            [1, 8],
            [2, 2, 2, 3],
            [2, 7],
            [3, 3, 3],
            [3, 6],
            [4, 5],
            [9],
        ],
        description="Many candidates with medium target",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def normalize_output(combinations):
        """Normalize output by sorting each combination and the list of combinations."""
        return sorted([sorted(combo) for combo in combinations])

    def test_function(candidates, target):
        solution = Solution()
        result = solution.combinationSum(candidates, target)
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
    slug="combination-sum",
    leetcode_num=39,
    title="Combination Sum",
    difficulty=Difficulty.MEDIUM,
    category=Category.BACKTRACKING,
    solution_func=Solution().combinationSum,
    test_func=test_solution,
    demo_func=create_demo_output,
)
