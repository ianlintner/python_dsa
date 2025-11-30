"""
Combination Sum (LeetCode 39)

Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen
numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times.

All solutions must be unique and use only numbers from the given candidate set.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []

        def backtrack(start: int, path: List[int], total: int):
            if total == target:
                res.append(path[:])
                return
            if total > target:
                return
            for i in range(start, len(candidates)):
                path.append(candidates[i])
                backtrack(i, path, total + candidates[i])
                path.pop()

        backtrack(0, [], 0)
        return res


# Example test cases
test_cases = [
    TestCase(([2, 3, 6, 7], 7), [[2, 2, 3], [7]], "Standard case"),
    TestCase(([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]], "Multiple solutions"),
    TestCase(([2], 1), [], "No solution possible"),
]


def demo() -> str:
    """Run test cases for Combination Sum."""
    sol = Solution()
    outputs = []
    outputs.append("Combination Sum | LeetCode 39")
    outputs.append("=" * 50)
    outputs.append("Time: O(2^target/min) | Space: O(target/min)")
    outputs.append("Technique: Backtracking with pruning\n")

    for case in test_cases:
        res = sol.combinationSum(*case.input_args)
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
    id=39,
    slug="combination_sum",
    title="Combination Sum",
    category=Category.BACKTRACKING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "backtracking"],
    url="https://leetcode.com/problems/combination-sum/",
    notes="",
)
