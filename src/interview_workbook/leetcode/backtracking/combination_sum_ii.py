"""
Combination Sum II (LeetCode 40)

Given a collection of candidate numbers (candidates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.
The solution set must not contain duplicate combinations.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
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


# Example test cases
test_cases = [
    TestCase(
        ([10, 1, 2, 7, 6, 1, 5], 8),
        [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]],
        "Standard case with duplicates",
    ),
    TestCase(([2, 5, 2, 1, 2], 5), [[1, 2, 2], [5]], "Multiple ways to reach target"),
    TestCase(([1, 1, 1, 1], 2), [[1, 1]], "All same elements"),
]


def demo() -> str:
    """Run test cases for Combination Sum II."""
    sol = Solution()
    outputs = []
    outputs.append("Combination Sum II | LeetCode 40")
    outputs.append("=" * 50)
    outputs.append("Time: O(2^n) | Space: O(n)")
    outputs.append("Technique: Backtracking with duplicate skipping\n")

    for case in test_cases:
        res = sol.combinationSum2(*case.input_args)
        # Sort for comparison since order may vary
        res_sorted = sorted([sorted(x) for x in res])
        expected_sorted = sorted([sorted(x) for x in case.expected])
        passed = res_sorted == expected_sorted
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: candidates={case.input_args[0]}, target={case.input_args[1]}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


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
