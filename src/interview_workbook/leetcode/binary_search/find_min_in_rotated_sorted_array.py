"""
Find Min In Rotated Sorted Array

TODO: Add problem description
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def findMin(self, nums: list[int]) -> int:
        """Find minimum in rotated sorted array."""
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return nums[left]


test_cases = [
    TestCase(([3, 4, 5, 1, 2],), 1, "Rotated with min in middle"),
    TestCase(([4, 5, 6, 7, 0, 1, 2],), 0, "Rotated with min near end"),
    TestCase(([11, 13, 15, 17],), 11, "Not rotated"),
]


def demo():
    """Run Find Minimum in Rotated Sorted Array demo."""

    def wrapper(nums):
        return Solution().findMin(nums)

    results = run_test_cases(
        wrapper, test_cases, "LeetCode 153: Find Minimum in Rotated Sorted Array"
    )

    return create_demo_output(
        "Find Minimum in Rotated Sorted Array",
        results,
        time_complexity="O(log n)",
        space_complexity="O(1)",
        approach_notes="Binary search compares mid with right to shrink interval until min found.",
    )


register_problem(
    id=153,
    slug="find_min_in_rotated_sorted_array",
    title="Find Minimum in Rotated Sorted Array",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["binary_search", "array"],
    url="https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
    notes="Uses binary search variant comparing mid with rightmost value.",
)
