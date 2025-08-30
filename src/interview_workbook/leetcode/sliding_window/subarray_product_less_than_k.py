"""
Subarray Product Less Than K

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return count of subarrays where product < k."""
        nums, k = args
        if k <= 1:
            return 0
        prod = 1
        res = 0
        l = 0
        for r, n in enumerate(nums):
            prod *= n
            while prod >= k:
                prod //= nums[l]
                l += 1
            res += r - l + 1
        return res


def demo():
    """Run a simple demonstration for Subarray Product Less Than K."""
    nums = [10, 5, 2, 6]
    k = 100
    result = Solution().solve(nums, k)
    return f"Input: nums={nums}, k={k} -> Count of subarrays: {result}"


register_problem(
    id=713,
    slug="subarray_product_less_than_k",
    title="Subarray Product Less Than K",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "sliding window"],
    url="https://leetcode.com/problems/subarray-product-less-than-k/",
    notes="Two-pointer sliding window. Expand right, shrink left until product < k.",
)
