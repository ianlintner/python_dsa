"""
Car Fleet

There are `n` cars going to the same destination along a one-lane road.
The destination is `target` miles away. Each car `i` has a position and speed.
A car fleet forms when one catches up to another before the target.

Return how many car fleets will arrive at the destination.
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


register_problem(
    id=853,
    slug="car_fleet",
    title="Car Fleet",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "greedy", "sorting"],
    url="https://leetcode.com/problems/car-fleet/",
    notes="Sort cars by position and collapse fleets using a stack.",
)
