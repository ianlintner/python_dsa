"""
Permutations (LeetCode 46)

Given a collection of distinct numbers, return all possible permutations.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []

        def backtrack(start=0):
            if start == len(nums):
                res.append(nums[:])
                return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        backtrack()
        return res


def demo():
    s = Solution()
    result = s.permute([1, 2, 3])
    return str(result)


register_problem(
    id=46,
    slug="permutations",
    title="Permutations",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["backtracking"],
    url="https://leetcode.com/problems/permutations/",
    notes="",
)
