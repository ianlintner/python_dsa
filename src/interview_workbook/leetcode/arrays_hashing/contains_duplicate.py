"""
Contains Duplicate - LeetCode Problem

Given an integer array nums, return true if any value appears at least twice in the array,
and return false if every element is distinct.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """
        Check if array contains any duplicates using a hash set.

        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - hash set storage in worst case

        Args:
            nums: List of integers

        Returns:
            bool: True if duplicates exist, False otherwise
        """
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

    def containsDuplicateSort(self, nums: List[int]) -> bool:
        """
        Alternative solution using sorting.

        Time Complexity: O(n log n) - sorting dominates
        Space Complexity: O(1) - in-place sorting
        """
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False


def demo():
    """Demonstrate Contains Duplicate solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(input_args=([1, 2, 3, 1],), expected=True, description="Basic duplicate case"),
        TestCase(input_args=([1, 2, 3, 4],), expected=False, description="No duplicates"),
        TestCase(
            input_args=([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],),
            expected=True,
            description="Multiple duplicates",
        ),
        TestCase(input_args=([],), expected=False, description="Empty array"),
        TestCase(input_args=([1],), expected=False, description="Single element"),
        TestCase(input_args=([0, 0],), expected=True, description="Two zeros"),
    ]

    test_results = run_test_cases(solution.containsDuplicate, test_cases, "LeetCode 217: Contains Duplicate")

    approach_notes = """
Key Insights:
• Hash set provides O(1) average lookup time for duplicate detection
• Early termination when duplicate found improves performance
• Alternative O(n log n) sorting solution uses O(1) space
• Consider space vs time tradeoffs between hashmap and sorting approaches

Common Pitfalls:
• Remember that empty arrays have no duplicates
• Consider edge cases like single elements

Follow-up Questions:
• What if we cannot use extra space?
• How would you modify for duplicate count?
• Can you solve in O(1) space for specific constraints?
"""

    return create_demo_output(
        problem_title="LeetCode 217: Contains Duplicate",
        test_results=test_results,
        time_complexity="O(n) - single pass through array",
        space_complexity="O(n) - hash set storage in worst case",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=217,
    slug="contains-duplicate",
    title="Contains Duplicate",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.EASY,
    tags=["array", "hash-table"],
    url="https://leetcode.com/problems/contains-duplicate/",
    notes="Classic hash set problem for duplicate detection",
)
