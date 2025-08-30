"""
Last Stone Weight

Problem: Last Stone Weight
LeetCode link: https://leetcode.com/problems/last-stone-weight/
Description: Given an array of stones, repeatedly smash the two heaviest stones together. If they are equal, both are destroyed; otherwise the difference remains as a new stone. Return the last stone weight or 0 if none remain.
"""

import heapq
import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    """Simulate smashing stones using a max-heap."""

    def solve(self, stones: list[int]) -> int:
        """Return the weight of the last remaining stone, or 0."""
        if not stones:
            return 0
        # Use negative values for max-heap
        heap = [-s for s in stones]
        heapq.heapify(heap)

        while len(heap) > 1:
            y = -heapq.heappop(heap)
            x = -heapq.heappop(heap)
            if y != x:
                heapq.heappush(heap, -(y - x))

        return -heap[0] if heap else 0


def demo() -> str:
    """Demo for Last Stone Weight."""
    random.seed(0)
    stones = [2, 7, 4, 1, 8, 1]
    s = Solution()
    return f"Last stone weight from {stones} -> {s.solve(stones)}"


register_problem(
    id=1046,
    slug="last_stone_weight",
    title="Last Stone Weight",
    category=Category.HEAP,
    difficulty=Difficulty.EASY,
    tags=["array", "heap"],
    url="https://leetcode.com/problems/last-stone-weight/",
    notes="",
)
