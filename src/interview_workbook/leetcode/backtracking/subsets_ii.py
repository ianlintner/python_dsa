"""
Subsets II (LeetCode 90)

Given an integer array nums that may contain duplicates, return all possible
subsets (the power set). The solution set must not contain duplicate subsets.
"""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
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


# Example test cases
test_cases = [
    TestCase(
        ([1, 2, 2],),
        [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]],
        "Array with duplicates",
    ),
    TestCase(([0],), [[], [0]], "Single element"),
    TestCase(
        ([4, 4, 4, 1, 4],),
        [
            [],
            [1],
            [1, 4],
            [1, 4, 4],
            [1, 4, 4, 4],
            [1, 4, 4, 4, 4],
            [4],
            [4, 4],
            [4, 4, 4],
            [4, 4, 4, 4],
        ],
        "Multiple duplicates",
    ),
]


def demo() -> str:
    """Run test cases for Subsets II."""
    sol = Solution()
    outputs = []
    outputs.append("Subsets II | LeetCode 90")
    outputs.append("=" * 50)
    outputs.append("Time: O(n * 2^n) | Space: O(n)")
    outputs.append("Technique: Backtracking with duplicate skipping\n")

    for case in test_cases:
        res = sol.subsetsWithDup(list(case.input_args[0]))
        # Sort for comparison since order may vary
        res_sorted = sorted([tuple(sorted(x)) for x in res])
        expected_sorted = sorted([tuple(sorted(x)) for x in case.expected])
        passed = res_sorted == expected_sorted
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: nums={list(case.input_args[0])}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


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
