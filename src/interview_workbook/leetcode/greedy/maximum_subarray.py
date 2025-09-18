"""
Maximum Subarray

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, nums):
        """Kadane's algorithm to find maximum subarray sum."""
        max_sum = nums[0]
        current_sum = nums[0]
        for n in nums[1:]:
            current_sum = max(n, current_sum + n)
            max_sum = max(max_sum, current_sum)
        return max_sum


def demo() -> str:
    """Run a demo for the Maximum Subarray problem."""
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"Input nums: {nums}")
    s = Solution()
    result = s.solve(nums)
    print(f"Final result: {result}")
    return f"Maximum Subarray result for {nums} -> {result}"


if __name__ == "__main__":
    demo()


register_problem(
    id=53,
    slug="maximum_subarray",
    title="Maximum Subarray",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "divide_and_conquer", "dynamic_programming"],
    url="https://leetcode.com/problems/maximum-subarray/",
    notes="",
)
