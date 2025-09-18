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


def demo() -> str:
    """Run a demo for the Jump Game II problem."""
    nums = [2, 3, 1, 1, 4]
    print(f"Input nums: {nums}")
    s = Solution()
    result = s.solve(nums)
    print(f"Final result: {result}")
    return f"Jump Game II result for {nums} -> {result}"


if __name__ == "__main__":
    demo()


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
