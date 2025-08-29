"""
Jump Game Ii

TODO: Add problem description
"""


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
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="jump_game_ii",
#     title="Jump Game Ii",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
