"""
Two Sum II - Input Array Is Sorted (LeetCode 167)

Given a 1-indexed array of integers `numbers` that is already sorted in
non-decreasing order, find two numbers such that they add up to a specific
target number. Return the indices of the two numbers (1-indexed).
The solution must use only constant extra space.

https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
"""


class Solution:
    def solve(self, *args):
        """Finds indices of two numbers whose sum equals target using two pointers."""
        numbers, target = args
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target:
                return [l + 1, r + 1]
            elif s < target:
                l += 1
            else:
                r -= 1
        return []


def demo():
    """Deterministic demo for Two Sum II problem."""
    numbers = [2, 7, 11, 15]
    target = 9
    result = Solution().solve(numbers, target)
    return str(result)


from src.interview_workbook.leetcode._runner import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


register_problem(
    id=167,
    slug="two-sum-ii-input-array-is-sorted",
    title="Two Sum II - Input Array Is Sorted",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags=["Array", "Two Pointers", "Binary Search"],
    url="https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
    notes="Classic two-pointer sum search on sorted array.",
)
