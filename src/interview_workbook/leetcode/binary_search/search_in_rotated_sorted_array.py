"""
Search In Rotated Sorted Array

Problem: Search in Rotated Sorted Array
LeetCode link: https://leetcode.com/problems/search-in-rotated-sorted-array/
Description: Given a rotated sorted array of distinct integers, return the index of the target if it exists, otherwise return -1. Must run in O(log n) time.
"""


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


def demo():
    """Run a demo for the Search In Rotated Sorted Array problem."""
    solver = Solution()
    nums = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    result = solver.search(nums, target)
    return str(result)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="search_in_rotated_sorted_array",
#     title="Search In Rotated Sorted Array",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
