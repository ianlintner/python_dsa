"""
Combination Sum II (LeetCode 40)

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.
The solution set must not contain duplicate combinations.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        candidates.sort()

        def backtrack(start, path, remain):
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if candidates[i] > remain:
                    break
                path.append(candidates[i])
                backtrack(i + 1, path, remain - candidates[i])
                path.pop()

        backtrack(0, [], target)
        return res


def demo():
    s = Solution()
    result = s.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)
    return str(result)


register_problem(
    id=40,
    slug="combination_sum_ii",
    title="Combination Sum II",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "backtracking"],
    url="https://leetcode.com/problems/combination-sum-ii/",
    notes="",
)
