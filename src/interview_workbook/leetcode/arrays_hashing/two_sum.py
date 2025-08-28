"""
LeetCode 1: Two Sum

Given an array of integers `nums` and an integer `target`, return indices of the
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not
use the same element twice. You can return the answer in any order.

URL: https://leetcode.com/problems/two-sum/
Difficulty: Easy
Category: Arrays & Hashing

Patterns:
- Hash table for O(1) lookups
- Single-pass with complement checking
- Trade space for time optimization

Complexity:
- Time: O(n) - single pass through array
- Space: O(n) - hash table storage

Pitfalls:
- Don't use same element twice (check index != current)
- Ensure exactly one solution exists (problem guarantee)
- Handle negative numbers correctly

Follow-ups:
- What if no solution exists?
- What if multiple solutions exist?
- Can you do it in O(1) space? (Yes, with sorting + two pointers, but indices change)
- What if the input is sorted? (Two pointers approach)
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        Find two numbers in nums that add up to target.

        Args:
            nums: List of integers
            target: Target sum

        Returns:
            List of two indices [i, j] where nums[i] + nums[j] == target
        """
        # Hash map to store value -> index mapping
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            # Check if complement exists in our hash map
            if complement in seen:
                # Found our pair!
                return [seen[complement], i]

            # Store current number and its index
            seen[num] = i

        # Should never reach here given problem constraints
        return []


# Test cases
test_cases = [
    TestCase(
        input_args=(([2, 7, 11, 15], 9,
    )), [0, 1], "Basic case: first two elements"),
    TestCase(
        input_args=(([3, 2, 4], 6,
    )), [1, 2], "Target requires latter elements"),
    TestCase(
        input_args=(([3, 3], 6,
    )), [0, 1], "Duplicate elements"),
    TestCase(
        input_args=(([1, 5, 3, 7, 9, 2], 8,
    )), [1, 2], "Multiple possibilities, return first found"),
    TestCase(
        input_args=(([0, 4, 3, 0], 0,
    )), [0, 3], "Zero target with zero elements"),
    TestCase(
        input_args=(([-1, -2, -3, -4, -5], -8,
    )), [2, 4], "Negative numbers"),
]


def demo() -> str:
    """Run Two Sum demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.twoSum, test_cases, "LeetCode 1: Two Sum")

    return create_demo_output(
        "Two Sum",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use hashmap to store seen values and their indices
2. For each element, check if its complement (target - element) exists
3. Single pass solution is more efficient than nested loops O(n²)
4. Space-time tradeoff: O(n) space for O(n) time vs O(1) space for O(n²) time
        """.strip(),
    )


# Register the problem
register_problem(
    id=1,
    slug="two_sum",
    title="Two Sum",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["array", "hashmap"],
    url="https://leetcode.com/problems/two-sum/",
    notes="Classic hash table problem, fundamental pattern for complement searches",
)
