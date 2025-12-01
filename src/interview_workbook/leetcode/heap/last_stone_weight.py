"""
Last Stone Weight

Problem: Last Stone Weight
LeetCode link: https://leetcode.com/problems/last-stone-weight/
Description: Given an array of stones, repeatedly smash the two heaviest stones together. If they are equal, both are destroyed; otherwise the difference remains as a new stone. Return the last stone weight or 0 if none remain.
"""

import heapq
import random

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    """Simulate smashing stones using a max-heap."""

    def lastStoneWeight(self, stones: list[int]) -> int:
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


# Example test cases
test_cases = [
    TestCase(([2, 7, 4, 1, 8, 1],), 1, "Standard case"),
    TestCase(([1],), 1, "Single stone"),
    TestCase(([2, 2],), 0, "Two equal stones"),
    TestCase(([1, 3],), 2, "Two different stones"),
]


def demo() -> str:
    """Run test cases for Last Stone Weight."""
    random.seed(0)
    sol = Solution()
    outputs = []
    outputs.append("Last Stone Weight | LeetCode 1046")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log n) | Space: O(n)")
    outputs.append("Technique: Max-heap simulation\n")

    for case in test_cases:
        stones = list(case.input_args[0])
        res = sol.lastStoneWeight(stones)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: stones={list(case.input_args[0])}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


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

if __name__ == "__main__":
    demo()
