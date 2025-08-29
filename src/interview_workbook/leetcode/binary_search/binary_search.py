"""
Binary Search

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        """Standard binary search implementation."""
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1


def demo():
    """Run a demo for the Binary Search problem."""
    solver = Solution()
    nums = [-1, 0, 3, 5, 9, 12]
    target = 9
    result = solver.search(nums, target)
    return str(result)


# Register the problem with correct parameters
register_problem(
    id=704,
    slug="binary_search",
    title="Binary Search",
    category="binary_search",
    difficulty="Medium",
    tags=["binary-search"],
    url="https://leetcode.com/problems/binary-search/",
    notes="Classic binary search implementation.",
)
