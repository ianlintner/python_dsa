"""
Jump Game

Problem: Jump Game
LeetCode link: https://leetcode.com/problems/jump-game/
Description: Determine if it is possible to reach the last index of an array, given maximum jump lengths at each position.
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> bool:
        """
        Greedy solution to Jump Game.
        Returns True if last index is reachable, otherwise False.
        """
        nums = args[0]
        max_reach = 0
        for i, num in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + num)
        return True


def demo():
    """Run a demo for the Jump Game problem."""
    solver = Solution()
    nums = [2,3,1,1,4]
    result = solver.solve(nums)
    return str(result)


register_problem(
    id=55,
    slug="jump_game",
    title="Jump Game",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dynamic_programming", "greedy"],
    url="https://leetcode.com/problems/jump-game/",
    notes="",
)
