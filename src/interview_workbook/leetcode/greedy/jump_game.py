"""
Jump Game

Problem: Jump Game
LeetCode link: https://leetcode.com/problems/jump-game/
Description: Determine if it is possible to reach the last index of an array, given maximum jump lengths at each position.
"""


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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="jump_game",
#     title="Jump Game",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
