"""LeetCode Problem 11: Container With Most Water."""


from typing import List
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


def maxArea(height: List[int]) -> int:
    """Return the maximum amount of water a container can store.

    Uses the two-pointer approach in O(n) time.
    """
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        width = right - left
        curr_area = min(height[left], height[right]) * width
        max_area = max(max_area, curr_area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area


def demo() -> str:
    """Demonstrate the Container With Most Water problem in headless mode."""
    example = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    result = maxArea(example)
    return str(result)


register_problem(
    problem_id=11,
    slug="container-with-most-water",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags=["Array", "Two Pointers", "Greedy"],
    url="https://leetcode.com/problems/container-with-most-water/",
)
