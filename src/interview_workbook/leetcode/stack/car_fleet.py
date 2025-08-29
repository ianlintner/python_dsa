"""
Car Fleet

TODO: Add problem description
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, target, position, speed) -> int:
        """Return the number of car fleets that will arrive at the target."""
        cars = sorted(zip(position, speed), reverse=True)
        stack = []
        for pos, spd in cars:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:
                stack.append(time)
        return len(stack)


def demo():
    return str(Solution().solve(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))


# TODO: Register the problem with correct parameters
register_problem(
    slug="car_fleet",
    title="Car Fleet",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack"],
    url="https://leetcode.com/problems/car-fleet/",
    notes="Greedy with sorting and stack",
)
