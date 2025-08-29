"""
Subsets II (LeetCode 90)

Given an integer array nums that may contain duplicates, return all possible
subsets (the power set). The solution set must not contain duplicate subsets.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        nums.sort()

        def backtrack(start: int, path: List[int]) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()

        backtrack(0, [])
        return res


def demo() -> str:
    s = Solution()
    result = s.subsetsWithDup([1, 2, 2])
    return str(result)


register_problem(
    id=90,
    slug="subsets-ii",
    title="Subsets II",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["backtracking"],
    url="https://leetcode.com/problems/subsets-ii/",
    notes="Handles duplicates by skipping identical consecutive elements during backtracking.",
)
