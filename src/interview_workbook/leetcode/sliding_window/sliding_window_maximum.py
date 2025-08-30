"""
Sliding Window Maximum

TODO: Add problem description
"""

from collections import deque

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args):
        """Return list of max values in each sliding window."""
        nums, k = args
        if not nums or k == 0:
            return []
        q = deque()
        res = []
        for i, n in enumerate(nums):
            while q and q[0] <= i - k:
                q.popleft()
            while q and nums[q[-1]] < n:
                q.pop()
            q.append(i)
            if i >= k - 1:
                res.append(nums[q[0]])
        return res


def demo():
    """Run a simple demonstration for Sliding Window Maximum."""
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    result = Solution().solve(nums, k)
    return f"Input: nums={nums}, k={k} -> Sliding window maximums: {result}"


register_problem(
    id=239,
    slug="sliding_window_maximum",
    title="Sliding Window Maximum",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.HARD,
    tags=["array", "deque", "sliding window", "heap"],
    url="https://leetcode.com/problems/sliding-window-maximum/",
    notes="Use deque to maintain indices of useful elements for O(n) processing.",
)
