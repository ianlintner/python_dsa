"""LeetCode 42 - Trapping Rain Water (Two Pointers)."""

from typing import List

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


def trap(height: List[int]) -> int:
    """
    Compute how much water can be trapped after raining.

    Uses two-pointer technique with left/right max tracking.
    Runs in O(n) time and O(1) extra space.

    Args:
        height: List of non-negative integers representing elevation map.

    Returns:
        Total units of water trapped.
    """
    n = len(height)
    if n == 0:
        return 0

    left, right = 0, n - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += max(0, right_max - height[right])

    return water


def demo() -> str:
    """Headless demonstration for deterministic testing."""
    example = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    result = trap(example)
    return str(result)


# Register problem metadata
register_problem(
    id=42,
    title="Trapping Rain Water",
    slug="trapping-rain-water",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.HARD,
    tags=["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
    url="https://leetcode.com/problems/trapping-rain-water/",
    function=trap,
    demo=demo,
)
