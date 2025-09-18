"""
Non-decreasing Array

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, nums):
        """Check if the array can be made non-decreasing by modifying at most one element."""
        modified = False
        for i in range(1, len(nums)):
            if nums[i] < nums[i - 1]:
                if modified:
                    return False
                modified = True
                if i < 2 or nums[i] >= nums[i - 2]:
                    nums[i - 1] = nums[i]
                else:
                    nums[i] = nums[i - 1]
        return True


def demo() -> str:
    """Run a demo for the Non-decreasing Array problem."""
    nums = [4,2,3]
    print(f"Input nums: {nums}")
    s = Solution()
    result = s.solve(nums)
    print(f"Final result: {result}")
    return f"Non-decreasing Array result for {nums} -> {result}"


if __name__ == "__main__":
    demo()
    

register_problem(
    id=665,
    slug="non_decreasing_array",
    title="Non-decreasing Array",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "greedy"],
    url="https://leetcode.com/problems/non-decreasing-array/",
    notes="",
)
