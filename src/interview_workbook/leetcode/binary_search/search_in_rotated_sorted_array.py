"""
Search In Rotated Sorted Array

Problem: Search in Rotated Sorted Array
LeetCode link: https://leetcode.com/problems/search-in-rotated-sorted-array/
Description: Given a rotated sorted array of distinct integers, return the index of the target if it exists, otherwise return -1. Must run in O(log n) time.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        """Search in rotated sorted array."""
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return -1


# Example test cases
test_cases = [
    TestCase(([4, 5, 6, 7, 0, 1, 2], 0), 4, "Target in right half after rotation"),
    TestCase(([4, 5, 6, 7, 0, 1, 2], 3), -1, "Target not found"),
    TestCase(([1], 0), -1, "Single element not found"),
    TestCase(([1], 1), 0, "Single element found"),
    TestCase(([3, 1], 1), 1, "Two elements rotated"),
]


def demo() -> str:
    """Run test cases for Search in Rotated Sorted Array."""
    sol = Solution()
    outputs = []
    outputs.append("Search in Rotated Sorted Array | LeetCode 33")
    outputs.append("=" * 50)
    outputs.append("Time: O(log n) | Space: O(1)")
    outputs.append("Technique: Modified binary search\n")

    for case in test_cases:
        nums, target = case.input_args
        res = sol.search(list(nums), target)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: nums={list(nums)}, target={target}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


register_problem(
    id=33,
    slug="search_in_rotated_sorted_array",
    title="Search in Rotated Sorted Array",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "binary_search"],
    url="https://leetcode.com/problems/search-in-rotated-sorted-array/",
    notes="",
)
