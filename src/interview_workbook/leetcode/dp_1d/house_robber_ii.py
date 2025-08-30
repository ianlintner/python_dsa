"""
House Robber Ii

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Return the maximum amount you can rob without robbing adjacent houses in circular arrangement."""
        if not args:
            return 0
        nums = args[0]
        if len(nums) == 1:
            return nums[0]

        def rob_linear(houses):
            rob1, rob2 = 0, 0
            for n in houses:
                new_rob = max(rob2, rob1 + n)
                rob1, rob2 = rob2, new_rob
            return rob2

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def demo():
    """Run a demo for the House Robber II problem."""
    solver = Solution()
    nums = [2, 3, 2]
    result = solver.solve(nums)
    return str(result)


register_problem(
    id=213,
    slug="house_robber_ii",
    title="House Robber II",
    category=Category.DP_1D,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming"],
    url="https://leetcode.com/problems/house-robber-ii/",
    notes="",
)
