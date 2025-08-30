"""LeetCode Problem 16: 3Sum Closest

Given an integer array nums of length n and an integer target, find three integers
in nums such that the sum is closest to target. Return the sum of the three integers.
You may assume that each input would have exactly one solution.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


def threeSumClosest(nums: List[int], target: int) -> int:
    """Find the sum of three integers in nums closest to target.

    Uses sorting and the two-pointer technique.
    Time complexity: O(n^2)
    """
    nums.sort()
    n = len(nums)
    closest_sum = nums[0] + nums[1] + nums[2]

    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum
            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                # Exact match
                return current_sum
    return closest_sum


def demo() -> str:
    """Headless demonstration of the 3Sum Closest algorithm."""
    nums = [-1, 2, 1, -4]
    target = 1
    result = threeSumClosest(nums, target)
    return str(result)


# Register this problem
register_problem(
    id=16,
    slug="3sum-closest",
    difficulty=Difficulty.MEDIUM,
    category=Category.TWO_POINTERS,
    func=threeSumClosest,
    url="https://leetcode.com/problems/3sum-closest/",
    tags=["Array", "Two Pointers", "Sorting"],
)
