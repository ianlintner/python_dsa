"""
Partition Equal Subset Sum

Given a non-empty array nums containing only positive integers,
determine if the array can be partitioned into two subsets such
that the sum of elements in both subsets is equal.

This is the classic Subset Sum / 0-1 Knapsack variation.
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, nums: list[int]) -> bool:
        """Return True if nums can be partitioned into equal subset sums."""
        total = sum(nums)
        if total % 2 != 0:
            return False
        target = total // 2

        dp = [False] * (target + 1)
        dp[0] = True

        for num in nums:
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]
        return dp[target]


import random


def demo() -> str:
    """Demonstrate Partition Equal Subset Sum solution."""
    random.seed(0)
    examples = [
        [1, 5, 11, 5],
        [1, 2, 3, 5],
        [2, 2, 3, 5],
    ]
    out_lines = []
    sol = Solution()
    for nums in examples:
        out_lines.append(f"nums={nums}, can_partition={sol.solve(nums)}")
    return "\n".join(out_lines)


# Register the problem with correct parameters

register_problem(
    id=416,
    slug="partition_equal_subset_sum",
    title="Partition Equal Subset Sum",
    category=Category.DP_1D,
    difficulty=Difficulty.MEDIUM,
    tags=["dynamic-programming", "subset-sum"],
    url="https://leetcode.com/problems/partition-equal-subset-sum/",
    notes="Uses 1D DP for subset sum check",
)
