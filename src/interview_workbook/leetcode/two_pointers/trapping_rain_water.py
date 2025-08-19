"""
Trapping Rain Water - LeetCode Problem

Given n non-negative integers representing an elevation map where the width of each bar is 1,
compute how much water it can trap after raining.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def trap(self, height: List[int]) -> int:
        """
        Calculate trapped rainwater using two pointers technique.

        Time Complexity: O(n) - single pass through array
        Space Complexity: O(1) - only using pointer variables

        Args:
            height: List of non-negative integers representing elevation map

        Returns:
            int: Total amount of trapped water
        """
        if not height or len(height) < 3:
            return 0

        left = 0
        right = len(height) - 1
        left_max = 0
        right_max = 0
        water_trapped = 0

        while left < right:
            if height[left] < height[right]:
                # Process left side
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water_trapped += left_max - height[left]
                left += 1
            else:
                # Process right side
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water_trapped += right_max - height[right]
                right -= 1

        return water_trapped

    def trapBruteForce(self, height: List[int]) -> int:
        """
        Brute force approach checking max height on both sides for each position.

        Time Complexity: O(n²) - for each position, scan left and right
        Space Complexity: O(1) - constant extra space
        """
        if not height:
            return 0

        n = len(height)
        water_trapped = 0

        for i in range(1, n - 1):  # Skip first and last positions
            # Find max height to the left
            left_max = 0
            for j in range(i):
                left_max = max(left_max, height[j])

            # Find max height to the right
            right_max = 0
            for j in range(i + 1, n):
                right_max = max(right_max, height[j])

            # Water level at position i
            water_level = min(left_max, right_max)
            if water_level > height[i]:
                water_trapped += water_level - height[i]

        return water_trapped

    def trapDynamicProgramming(self, height: List[int]) -> int:
        """
        Dynamic programming approach with left and right max arrays.

        Time Complexity: O(n) - three passes through array
        Space Complexity: O(n) - two additional arrays
        """
        if not height:
            return 0

        n = len(height)
        left_max = [0] * n
        right_max = [0] * n
        water_trapped = 0

        # Fill left_max array
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # Fill right_max array
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Calculate trapped water
        for i in range(n):
            water_level = min(left_max[i], right_max[i])
            if water_level > height[i]:
                water_trapped += water_level - height[i]

        return water_trapped

    def trapStack(self, height: List[int]) -> int:
        """
        Stack-based approach (educational alternative).

        Time Complexity: O(n) - each element pushed and popped at most once
        Space Complexity: O(n) - stack storage
        """
        if not height:
            return 0

        stack = []
        water_trapped = 0

        for i, h in enumerate(height):
            while stack and height[stack[-1]] < h:
                top = stack.pop()
                if not stack:
                    break

                distance = i - stack[-1] - 1
                bounded_height = min(h, height[stack[-1]]) - height[top]
                water_trapped += distance * bounded_height

            stack.append(i)

        return water_trapped


def demo():
    """Demonstrate Trapping Rain Water solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],),
            expected=6,
            description="Classic example with multiple valleys",
        ),
        TestCase(input_args=([4, 2, 0, 3, 2, 5],), expected=9, description="Deep valley in middle"),
        TestCase(input_args=([3, 0, 2, 0, 4],), expected=10, description="Multiple valleys"),
        TestCase(
            input_args=([1, 2, 3, 4, 5],),
            expected=0,
            description="Ascending heights - no water trapped",
        ),
        TestCase(
            input_args=([5, 4, 3, 2, 1],),
            expected=0,
            description="Descending heights - no water trapped",
        ),
        TestCase(input_args=([2, 0, 2],), expected=2, description="Simple valley"),
        TestCase(input_args=([3, 2, 0, 4],), expected=7, description="Wide valley"),
        TestCase(input_args=([1, 1, 1]), expected=0, description="Flat surface"),
        TestCase(input_args=([]), expected=0, description="Empty array"),
        TestCase(input_args=([1]), expected=0, description="Single element"),
    ]

    results = run_test_cases(solution.trap, test_cases)

    return create_demo_output(
        title="Trapping Rain Water",
        description="Calculate trapped rainwater using two pointers technique",
        results=results,
        complexity_analysis={
            "time": "O(n) - single pass through array with two pointers",
            "space": "O(1) - only using pointer variables and counters",
        },
        key_insights=[
            "Water level at any position = min(left_max, right_max)",
            "Two pointers approach processes smaller side first",
            "Always move pointer with smaller max height",
            "Alternative DP approach uses O(n) space for left/right max arrays",
        ],
        common_pitfalls=[
            "Handle edge cases: empty array, arrays with < 3 elements",
            "Water can only be trapped between taller bars on both sides",
            "Don't forget to update max heights as you traverse",
            "Stack approach is valid but more complex than two pointers",
        ],
        follow_up_questions=[
            "How would you handle 2D version of this problem?",
            "What if heights could be negative?",
            "Can you visualize the water trapping process?",
            "How would you optimize for very sparse arrays?",
        ],
    )


# Register this problem
register_problem(
    id=42,
    slug="trapping-rain-water",
    title="Trapping Rain Water",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.HARD,
    tags={"array", "two-pointers", "dynamic-programming", "stack", "monotonic-stack"},
    module="src.interview_workbook.leetcode.two_pointers.trapping_rain_water",
    url="https://leetcode.com/problems/trapping-rain-water/",
    notes="Two pointers technique for O(1) space solution to rainwater trapping",
)
