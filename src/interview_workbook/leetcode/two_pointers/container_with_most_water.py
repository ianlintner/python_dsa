"""
Container With Most Water - LeetCode Problem

You are given an integer array height of length n. There are n vertical lines drawn such that
the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container that can hold the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Find maximum area using two pointers technique.

        Time Complexity: O(n) - single pass with two pointers
        Space Complexity: O(1) - only using pointer variables

        Args:
            height: List of heights representing vertical lines

        Returns:
            int: Maximum water area that can be contained
        """
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            # Calculate current area
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height
            max_area = max(max_area, current_area)

            # Move the pointer with smaller height
            # This is the key insight: moving the taller line inward
            # can never lead to a better solution
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area

    def maxAreaBruteForce(self, height: List[int]) -> int:
        """
        Brute force approach checking all pairs (not optimal).

        Time Complexity: O(n²) - nested loops
        Space Complexity: O(1) - constant extra space
        """
        max_area = 0
        n = len(height)

        for i in range(n):
            for j in range(i + 1, n):
                width = j - i
                current_height = min(height[i], height[j])
                area = width * current_height
                max_area = max(max_area, area)

        return max_area


def demo():
    """Demonstrate Container With Most Water solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=([1, 8, 6, 2, 5, 4, 8, 3, 7],),
            expected=49,
            description="Classic example - area between indices 1 and 8",
        ),
        TestCase(input_args=([1, 1],), expected=1, description="Two equal heights"),
        TestCase(
            input_args=([1, 2, 1],), expected=2, description="Mountain shape - use outer lines"
        ),
        TestCase(
            input_args=([2, 3, 4, 5, 18, 17, 6],), expected=17, description="High peak in middle"
        ),
        TestCase(input_args=([1, 2, 3, 4, 5],), expected=6, description="Ascending heights"),
        TestCase(input_args=([5, 4, 3, 2, 1],), expected=6, description="Descending heights"),
        TestCase(
            input_args=([1, 8, 100, 2, 100, 4, 8, 3, 7],),
            expected=200,
            description="High walls at positions 2 and 4",
        ),
        TestCase(input_args=([2, 1],), expected=1, description="Two elements, different heights"),
    ]

    results = run_test_cases(solution.maxArea, test_cases)

    return create_demo_output(
        title="Container With Most Water",
        description="Find maximum water area using two pointers technique",
        results=results,
        complexity_analysis={
            "time": "O(n) - single pass with two pointers",
            "space": "O(1) - only using pointer variables",
        },
        key_insights=[
            "Area is determined by width × min(left_height, right_height)",
            "Always move the pointer with the smaller height inward",
            "Moving the taller line can never improve the solution",
            "Two pointers start at extremes and converge toward center",
        ],
        common_pitfalls=[
            "Don't move both pointers at once - only move the shorter one",
            "Remember area = width × height, where height is the minimum",
            "The optimal solution may not use the tallest lines",
            "Consider edge cases with only 2 elements",
        ],
        follow_up_questions=[
            "What if you could slant the container?",
            "How would you find all pairs that give maximum area?",
            "Can you solve if heights can be negative?",
            "What about 3D version with rectangular containers?",
        ],
    )


# Register this problem
register_problem(
    id=11,
    slug="container-with-most-water",
    title="Container With Most Water",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags={"array", "two-pointers", "greedy"},
    module="src.interview_workbook.leetcode.two_pointers.container_with_most_water",
    url="https://leetcode.com/problems/container-with-most-water/",
    notes="Two pointers with greedy strategy - always move shorter line inward",
)
