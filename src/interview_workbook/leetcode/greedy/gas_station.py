"""
Gas Station

Problem: Gas Station
LeetCode link: https://leetcode.com/problems/gas-station/
Description: Given two integer arrays gas and cost, determine if there exists a starting gas station index from which you can travel around the circuit once in the clockwise direction. Return -1 if not possible.
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """
        Greedy solution to the Gas Station problem.
        Returns the starting index if possible, otherwise -1.
        """
        gas, cost = args
        if sum(gas) < sum(cost):
            return -1

        start = 0
        tank = 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:
                start = i + 1
                tank = 0
        return start


def demo() -> str:
    """Run a demo for the Gas Station problem."""
    gas = [1,2,3,4,5]
    cost = [3,4,5,1,2]
    print(f"Gas: {gas}, Cost: {cost}")
    s = Solution()
    result = s.solve(gas, cost)
    print(f"Final result: {result}")
    return f"Gas Station result with gas {gas} and cost {cost} -> {result}"


if __name__ == "__main__":
    demo()
    


register_problem(
    id=134,
    slug="gas_station",
    title="Gas Station",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "greedy"],
    url="https://leetcode.com/problems/gas-station/",
    notes="",
)
