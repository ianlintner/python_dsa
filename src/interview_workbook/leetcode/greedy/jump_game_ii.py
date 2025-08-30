"""
Jump Game Ii

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """
        Greedy solution to Jump Game II.
        Returns the minimum number of jumps to reach the last index.
        """
        nums = args[0]
        jumps = 0
        current_end = 0
        farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = farthest
        return jumps


def demo():
    """Run a demo for the Jump Game II problem."""
    solver = Solution()
    nums = [2,3,1,1,4]
    result = solver.solve(nums)
    return str(result)


register_problem(
    id=45,
    slug="jump_game_ii",
    title="Jump Game II",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming", "greedy"],
    url="https://leetcode.com/problems/jump-game-ii/",
    notes="",
)
