"""
Subsets (LeetCode 78)

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets, and the subsets may be returned in any order.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []

        def backtrack(start: int, path: List[int]) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return res


def demo():
    s = Solution()
    result = s.subsets([1, 2, 3])
    return str(result)


register_problem(
    id=78,
    slug="subsets",
    title="Subsets",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["backtracking"],
    url="https://leetcode.com/problems/subsets/",
    notes="",
)
