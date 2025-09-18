"""
Find Median From Data Stream

TODO: Add problem description
"""

import heapq

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    """Maintain two heaps to find streaming median in O(log n) time."""

    def __init__(self) -> None:
        self.small = []  # max-heap (store as negative values)
        self.large = []  # min-heap

    def add_num(self, num: int) -> None:
        # Push onto max-heap
        heapq.heappush(self.small, -num)

        # Balance so that every num in small <= every num in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Rebalance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

    def solve(self, nums: list[int]) -> float:
        """Compute median by sequentially adding numbers from list."""
        for n in nums:
            self.add_num(n)
        return self.find_median()


def demo() -> str:
    """Demo for Find Median From Data Stream."""
    nums = [41, 35, 62, 4, 97, 108]
    print(f"Initial stream: {nums}")
    s = Solution()
    for num in nums:
        s.add_num(num)
        print(f"Added {num}, current median: {s.find_median()}")
    result = s.find_median()
    print(f"Final median: {result}")
    return f"Median of {nums} -> {result}"


register_problem(
    id=295,
    slug="find_median_from_data_stream",
    title="Find Median from Data Stream",
    category=Category.HEAP,
    difficulty=Difficulty.HARD,
    tags=["heap", "design"],
    url="https://leetcode.com/problems/find-median-from-data-stream/",
    notes="",
)

if __name__ == "__main__":
    print(demo())
