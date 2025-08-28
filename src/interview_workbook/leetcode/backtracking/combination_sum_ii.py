"""
LeetCode 40: Combination Sum II

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used ONCE in the combination.

Note: The solution set must not contain duplicate combinations.

Example 1:
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

Example 2:
Input: candidates = [2,5,2,1,2], target = 5
Output: [[1,2,2],[5]]

Constraints:
- 1 <= candidates.length <= 100
- 1 <= candidates[i] <= 50
- 1 <= target <= 30
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase
from .._types import Category, Difficulty


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations that sum to target, using each element at most once.

        Key insight: Sort array first, then skip duplicates at same recursion level.
        Unlike combination_sum, we move to next index after using an element since
        we can't reuse the same element.

        Time: O(2^n * k) where n = len(candidates), k = avg combination length
        Space: O(k) for recursion depth, plus O(result_size) for output

        Args:
            candidates: Array of positive integers (may contain duplicates)
            target: Target sum to achieve

        Returns:
            List of all unique combinations that sum to target
        """
        result = []
        candidates.sort()  # Sort to handle duplicates and enable early termination

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

                # Skip duplicates: if current element equals previous element
                # and we're not at the start position, skip it
                # This ensures we only use duplicates in first occurrence
                if i > start and candidates[i] == candidates[i - 1]:
                    continue

                # Choose: add current candidate
                current_combination.append(candidate)

                # Explore: recurse with NEXT index (can't reuse same element)
                # and reduced remaining target
                backtrack(i + 1, current_combination, remaining - candidate)

                # Unchoose: remove current candidate
                current_combination.pop()

        backtrack(0, [], target)
        return result

    def combinationSum2Iterative(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find combinations using iterative approach with duplicate handling.

        Build combinations level by level, avoiding duplicates by tracking
        the range of newly added combinations in previous iteration.

        Time: O(2^n * k) where k is average combination length
        Space: O(2^n * k) for storing all combinations
        """
        candidates.sort()
        result = [[]]  # Start with empty combination

        i = 0
        while i < len(candidates):
            # Count consecutive duplicates
            count = 1
            while i + count < len(candidates) and candidates[i + count] == candidates[i]:
                count += 1

            # Get the range of combinations from previous iteration
            prev_len = len(result)

            # For each count of current element (1 to count), add to existing combinations
            for c in range(1, count + 1):
                # Only add to combinations that were created in previous iterations
                # to avoid duplicate combinations
                for j in range(prev_len):
                    combination = result[j]
                    new_sum = sum(combination) + candidates[i] * c

                    # Only add if we don't exceed target
                    if new_sum <= target:
                        result.append(combination + [candidates[i]] * c)

            i += count

        # Filter to only combinations that sum to target
        return [combo for combo in result if sum(combo) == target]

    def combinationSum2DP(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find combinations using dynamic programming with duplicate counting.

        Use frequency count of each unique candidate to avoid duplicates
        while building up solutions for each target value.

        Time: O(n * target * avg_combination_length)
        Space: O(target * total_combinations)
        """
        from collections import Counter

        # Count frequency of each candidate
        counter = Counter(candidates)
        unique_candidates = list(counter.keys())

        # dp[i] stores all combinations that sum to i
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]  # One way to make 0: empty combination

        # For each unique candidate
        for candidate in unique_candidates:
            max_count = counter[candidate]

            # Process in reverse order to avoid using updated values
            for sum_val in range(target, candidate - 1, -1):
                # Try using 1, 2, ..., max_count of current candidate
                for count in range(1, min(max_count, sum_val // candidate) + 1):
                    needed_sum = sum_val - candidate * count

                    # Add current candidate 'count' times to combinations that sum to needed_sum
                    for combination in dp[needed_sum]:
                        dp[sum_val].append(combination + [candidate] * count)

        return dp[target]


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to combination sum II.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 40: Combination Sum II - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        ([10, 1, 2, 7, 6, 1, 5], 8, "Classic example with duplicates"),
        ([2, 5, 2, 1, 2], 5, "Multiple duplicates of same element"),
        ([1], 1, "Single element exact match"),
        (
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            27,
            "Many duplicates, impossible target",
        ),
        ([3, 1, 3, 5, 1, 1], 8, "Mixed duplicates"),
    ]

    for candidates, target, description in test_cases:
        demo_parts.append(f"\nTest Case: {candidates}, target = {target}")
        demo_parts.append(f"Description: {description}")

        # Show different approaches
        result1 = solution.combinationSum2(candidates, target)
        result2 = solution.combinationSum2Iterative(candidates, target)
        result3 = solution.combinationSum2DP(candidates, target)

        # Sort results for consistent comparison
        result1_sorted = sorted([sorted(combo) for combo in result1])
        result2_sorted = sorted([sorted(combo) for combo in result2])
        result3_sorted = sorted([sorted(combo) for combo in result3])

        demo_parts.append(f"Backtracking result: {len(result1)} combinations")
        demo_parts.append(f"  {result1_sorted}")
        demo_parts.append(f"Iterative result: {len(result2)} combinations")
        demo_parts.append(f"  {result2_sorted}")
        demo_parts.append(f"DP result: {len(result3)} combinations")
        demo_parts.append(f"  {result3_sorted}")

        # Verify consistency
        consistent = result1_sorted == result2_sorted == result3_sorted
        demo_parts.append(f"All approaches consistent: {consistent}")

    # Algorithm comparison
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nBacktracking Approach:")
    demo_parts.append("  • Time: O(2^n * k) where n=candidates, k=avg combination length")
    demo_parts.append("  • Space: O(k) recursion depth")
    demo_parts.append("  • Pros: Intuitive, efficient pruning, memory efficient")
    demo_parts.append("  • Cons: Recursion overhead")

    demo_parts.append("\nIterative Approach:")
    demo_parts.append("  • Time: O(2^n * k)")
    demo_parts.append("  • Space: O(2^n * k) for storing all intermediate combinations")
    demo_parts.append("  • Pros: No recursion, clear state progression")
    demo_parts.append("  • Cons: Higher memory usage, more complex duplicate handling")

    demo_parts.append("\nDynamic Programming Approach:")
    demo_parts.append("  • Time: O(unique_candidates * target * avg_combination_length)")
    demo_parts.append("  • Space: O(target * total_combinations)")
    demo_parts.append("  • Pros: Handles duplicates via frequency counting")
    demo_parts.append("  • Cons: Memory intensive, may not be faster for sparse solutions")

    # Key differences from Combination Sum I
    demo_parts.append("\n=== Differences from Combination Sum I ===")
    demo_parts.append("1. Each element can be used AT MOST ONCE (not unlimited)")
    demo_parts.append("2. Input array may contain duplicates")
    demo_parts.append("3. Must avoid duplicate combinations in result")
    demo_parts.append("4. Backtracking advances to next index (i+1), not same index (i)")
    demo_parts.append("5. Duplicate skipping logic at same recursion level")

    # Duplicate handling strategy
    demo_parts.append("\n=== Duplicate Handling Strategy ===")
    demo_parts.append("Sort input array: [1,1,2,5,6,7,10]")
    demo_parts.append("At each recursion level:")
    demo_parts.append("  • Use first occurrence of any duplicate value")
    demo_parts.append("  • Skip subsequent duplicates at SAME level")
    demo_parts.append("  • Allow duplicates at DIFFERENT levels (deeper recursion)")
    demo_parts.append("")
    demo_parts.append("Example: candidates=[1,1,2], target=3")
    demo_parts.append("  Level 0: Try first 1, skip second 1, try 2")
    demo_parts.append("  Level 1: Can use remaining 1 and 2")
    demo_parts.append("  Result: [1,2] - no [1,1,1] since target too small")

    # Mathematical insights
    demo_parts.append("\n=== Mathematical Insights ===")
    demo_parts.append("This is the 0/1 knapsack variation of combination problems:")
    demo_parts.append("  • Each item (candidate) can be chosen at most once")
    demo_parts.append("  • Goal is to find all ways to achieve exact target weight")
    demo_parts.append("")
    demo_parts.append("With duplicates, we effectively have multiple copies of same item.")
    demo_parts.append("The key insight is treating duplicates as a group and deciding")
    demo_parts.append("how many from that group to use (0, 1, 2, ..., count).")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. Resource Selection: Choose from available resources (each used once)")
    demo_parts.append("2. Team Formation: Select people with specific skills for project")
    demo_parts.append("3. Investment Portfolio: Select from available stocks/bonds")
    demo_parts.append("4. Course Scheduling: Choose courses to meet credit requirements")
    demo_parts.append("5. Recipe Planning: Select ingredients from pantry inventory")
    demo_parts.append("6. Package Selection: Choose items for shipping with weight limit")

    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        description="Classic example with duplicates",
        input_args=input_args=([10, 1, 2, 7, 6, 1, 5], 8,
    ),
        expected=[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]],
        description="Classic example with duplicates",
    ),
    TestCase(
        description="Multiple duplicates of same element",
        input_args=input_args=([2, 5, 2, 1, 2], 5,
    ),
        expected=[[1, 2, 2], [5]],
        description="Multiple duplicates of same element",
    ),
    TestCase(
        description="Single element exact match",
        input_args=input_args=([1], 1,
    ),
        expected=[[1]],
        description="Single element exact match",
    ),
    TestCase(
        description="Single element impossible target",
        input_args=input_args=([1], 2,
    ),
        expected=[],
        description="Single element, impossible target",
    ),
    TestCase(
        description="Mixed duplicates",
        input_args=input_args=([3, 1, 3, 5, 1, 1], 8,
    ),
        expected=[[1, 1, 1, 5], [1, 1, 3, 3], [3, 5]],
        description="Mixed duplicates",
    ),
    TestCase(
        description="Many duplicates achievable target",
        input_args=input_args=([1, 1, 1, 1, 1], 3,
    ),
        expected=[[1, 1, 1]],
        description="Many duplicates, achievable target",
    ),
    TestCase(
        description="Complex duplicate pattern",
        input_args=input_args=([4, 4, 2, 1, 4, 2, 2, 1, 3], 6,
    ),
        expected=[[1, 1, 4], [1, 2, 3], [2, 4]],
        description="Complex duplicate pattern",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def normalize_output(combinations):
        """Normalize output by sorting each combination and the list of combinations."""
        return sorted([sorted(combo) for combo in combinations])

    solution = Solution()

    for test_case in TEST_CASES:
        candidates, target = test_case.input_args
        result = solution.combinationSum2(candidates, target)
        normalized_result = normalize_output(result)
        normalized_expected = normalize_output(test_case.expected)

        if normalized_result == normalized_expected:
            print(f"✓ {test_case.name}: PASS")
        else:
            print(f"✗ {test_case.name}: FAIL")
            print(f"  Expected: {normalized_expected}")
            print(f"  Got: {normalized_result}")


# Register the problem
register_problem(
    slug="combination-sum-ii",
    leetcode_num=40,
    title="Combination Sum II",
    difficulty=Difficulty.MEDIUM,
    category=Category.BACKTRACKING,
    solution_func=lambda args: Solution().combinationSum2(args[0], args[1]),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["backtracking", "array", "recursion"],
    notes="Find all unique combinations that sum to target using each element at most once",
)
