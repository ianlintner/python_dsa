"""
Find Peak Element

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        """Find a peak element and return its index using binary search."""
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < nums[mid + 1]:
                left = mid + 1
            else:
                right = mid
        return left

    def findPeakElementLinear(self, nums: list[int]) -> int:
        """Simpler O(n) scan to find a peak element index."""
        for i in range(len(nums)):
            if (i == 0 or nums[i] > nums[i - 1]) and (i == len(nums) - 1 or nums[i] > nums[i + 1]):
                return i
        return 0

    def findPeakElementRecursive(self, nums: list[int]) -> int:
        """Recursive binary search variant to find a peak element index."""

        def search(left: int, right: int) -> int:
            if left == right:
                return left
            mid = (left + right) // 2
            if nums[mid] < nums[mid + 1]:
                return search(mid + 1, right)
            else:
                return search(left, mid)

        return search(0, len(nums) - 1)


test_cases = [
    TestCase(([1, 2, 3, 1],), 2, "Peak in the middle"),
    TestCase(([1, 2, 1, 3, 5, 6, 4],), 5, "Peak towards right"),
    TestCase(([1],), 0, "Single element is peak"),
]


def demo():
    """Run simple test cases for Find Peak Element."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.findPeakElement(*case.input_args)
        outputs.append(
            f"Find Peak Element | Input: {case.input_args} -> Output: {res}, Expected: {case.expected}"
        )
    return "\n".join(outputs)


register_problem(
    id=162,
    slug="find_peak_element",
    title="Find Peak Element",
    category=Category.BINARY_SEARCH,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "binary_search"],
    url="https://leetcode.com/problems/find-peak-element/",
    notes="",
)
