"""
Longest Increasing Subsequence

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> int:
        """Return the length of the longest increasing subsequence."""
        if not args:
            return 0
        nums = args[0]
        import bisect

        sub = []
        for x in nums:
            i = bisect.bisect_left(sub, x)
            if i == len(sub):
                sub.append(x)
            else:
                sub[i] = x
        return len(sub)


def demo():
    """Run a demo for the Longest Increasing Subsequence problem."""
    solver = Solution()
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    result = solver.solve(nums)
    print(f"Input nums: {nums}")
    print(f"Final result: {result}")
    return str(result)


register_problem(
    id=300,
    slug="longest_increasing_subsequence",
    title="Longest Increasing Subsequence",
    category=Category.DP_1D,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "binary_search", "dynamic_programming"],
    url="https://leetcode.com/problems/longest-increasing-subsequence/",
    notes="",
)
