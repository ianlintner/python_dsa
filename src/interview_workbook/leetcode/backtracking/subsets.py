"""
LeetCode 78: Subsets

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Examples:
    Input: nums = [1,2,3]
    Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

    Input: nums = [0]
    Output: [[],[0]]

Constraints:
    1 <= nums.length <= 10
    -10 <= nums[i] <= 10
    All the numbers of nums are unique.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase
from .._types import Category, Difficulty


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all subsets using backtracking.

        Algorithm:
        1. Start with empty subset
        2. For each number, choose to include or exclude
        3. Use backtracking to explore both choices
        4. Build subsets incrementally

        Time Complexity: O(2^n) - 2^n subsets to generate
        Space Complexity: O(n) - recursion depth
        """
        result = []

        def backtrack(start: int, current_subset: List[int]):
            # Add current subset to result (copy to avoid reference issues)
            result.append(current_subset[:])

            # Try adding each remaining number
            for i in range(start, len(nums)):
                # Choose: add nums[i] to current subset
                current_subset.append(nums[i])

                # Explore: recurse with next index
                backtrack(i + 1, current_subset)

                # Unchoose: remove nums[i] (backtrack)
                current_subset.pop()

        backtrack(0, [])
        return result

    def subsetsIterative(self, nums: List[int]) -> List[List[int]]:
        """
        Generate subsets iteratively by building up from empty set.

        Algorithm:
        1. Start with empty subset
        2. For each number, create new subsets by adding it to existing ones
        3. Keep accumulating subsets

        Time Complexity: O(2^n)
        Space Complexity: O(2^n) - store all subsets
        """
        result = [[]]  # Start with empty subset

        for num in nums:
            # For each existing subset, create new subset by adding current number
            new_subsets = []
            for subset in result:
                new_subsets.append(subset + [num])
            result.extend(new_subsets)

        return result

    def subsetsBitManipulation(self, nums: List[int]) -> List[List[int]]:
        """
        Generate subsets using bit manipulation.

        Algorithm:
        1. Each bit position represents whether to include nums[i]
        2. Iterate through all possible bit patterns (0 to 2^n - 1)
        3. For each pattern, include nums[i] if bit i is set

        Time Complexity: O(n * 2^n) - n work for each of 2^n subsets
        Space Complexity: O(1) excluding output space
        """
        result = []
        n = len(nums)

        # Generate all possible bit patterns (0 to 2^n - 1)
        for i in range(1 << n):  # 1 << n is 2^n
            subset = []

            # Check each bit position
            for j in range(n):
                if i & (1 << j):  # If bit j is set
                    subset.append(nums[j])

            result.append(subset)

        return result


def create_demo_output() -> str:
    """Create comprehensive demo showing different subset generation approaches."""
    solution = Solution()

    # Test cases for demonstration
    test_cases = [
        ([1, 2, 3], "Classic 3-element example"),
        ([0], "Single element"),
        ([1, 2], "Two elements"),
        ([4, 5, 6], "Different numbers"),
    ]

    output = []
    output.append("=== LeetCode 78: Subsets ===\n")

    for nums, desc in test_cases:
        output.append(f"Test: {desc}")
        output.append(f"Input: nums = {nums}")

        # Test all approaches
        result1 = solution.subsets(nums)
        result2 = solution.subsetsIterative(nums)
        result3 = solution.subsetsBitManipulation(nums)

        # Sort for consistent comparison
        result1.sort()
        result2.sort()
        result3.sort()

        output.append(f"Backtracking: {result1}")
        output.append(f"Iterative: {result2}")
        output.append(f"Bit manipulation: {result3}")
        output.append(f"Total subsets: {len(result1)} (expected: {2 ** len(nums)})")
        output.append("")

    # Algorithm analysis
    output.append("=== Algorithm Analysis ===")
    output.append("Backtracking Approach:")
    output.append("  • Time: O(2^n) - generate 2^n subsets")
    output.append("  • Space: O(n) - recursion depth")
    output.append("  • Pattern: Choose, explore, unchoose")
    output.append("")

    output.append("Iterative Approach:")
    output.append("  • Time: O(2^n) - process each subset once")
    output.append("  • Space: O(2^n) - store all subsets")
    output.append("  • Pattern: Build incrementally")
    output.append("")

    output.append("Bit Manipulation:")
    output.append("  • Time: O(n * 2^n) - n work per subset")
    output.append("  • Space: O(1) - excluding output")
    output.append("  • Pattern: Enumerate all bit patterns")
    output.append("")

    # Key insights
    output.append("=== Key Insights ===")
    output.append("1. **Power Set Size**: n elements → 2^n subsets")
    output.append("2. **Backtracking Pattern**: Choose → Explore → Unchoose")
    output.append("3. **Bit Representation**: Each subset maps to unique bit pattern")
    output.append("4. **Incremental Building**: Add one element at a time to existing subsets")
    output.append("")

    # Mathematical properties
    output.append("=== Mathematical Properties ===")
    output.append("For array of length n:")
    output.append("• Total subsets: 2^n (including empty set)")
    output.append("• Subsets of size k: C(n,k) = n!/(k!(n-k)!)")
    output.append("• Empty set: 1, Size 1: n, Size 2: n(n-1)/2, ..., Size n: 1")
    output.append("• Sum of all subset sizes: n * 2^(n-1)")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_args={"nums": [1, 2, 3]},
        expected=[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]],
        description="Classic example with 3 elements",
    ),
    TestCase(
        input_args={"nums": [0]},
        expected=[[], [0]],
        description="Single element array",
    ),
    TestCase(
        input_args={"nums": [1, 2]},
        expected=[[], [1], [2], [1, 2]],
        description="Two elements",
    ),
    TestCase(
        input_args={"nums": []},
        expected=[[]],
        description="Empty array - only empty subset",
    ),
    TestCase(
        input_args={"nums": [4, 5, 6]},
        expected=[[], [4], [5], [4, 5], [6], [4, 6], [5, 6], [4, 5, 6]],
        description="Different numbers",
    ),
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()

    def normalize_result(result):
        """Sort result for consistent comparison."""
        return sorted([sorted(subset) for subset in result])

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_data["nums"])
            expected = test_case.expected

            # Normalize both for comparison
            result_norm = normalize_result(result)
            expected_norm = normalize_result(expected)

            status = "✓" if result_norm == expected_norm else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result_norm != expected_norm:
                print(f"    Expected: {expected_norm}")
                print(f"    Got: {result_norm}")

    run_tests("Backtracking", solution.subsets)
    run_tests("Iterative", solution.subsetsIterative)
    run_tests("Bit Manipulation", solution.subsetsBitManipulation)

    # Run standard test framework
    def test_func(tc):
        result = solution.subsets(tc.input_data["nums"])
        expected = tc.expected
        return normalize_result(result) == normalize_result(expected)

    for i, test_case in enumerate(TEST_CASES):
        status = "✓" if test_func(test_case) else "✗"
        print(f"Standard Test {i + 1}: {status} - {test_case.description}")


# Register the problem
register_problem(
    slug="subsets",
    leetcode_num=78,
    title="Subsets",
    difficulty=Difficulty.MEDIUM,
    category=Category.BACKTRACKING,
    solution_func=lambda nums: Solution().subsets(nums),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["array", "backtracking", "bit-manipulation"],
    notes="Classic backtracking problem for generating all possible subsets (power set)",
)
