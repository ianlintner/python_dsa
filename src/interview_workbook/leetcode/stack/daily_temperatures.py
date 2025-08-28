"""
LeetCode 739: Daily Temperatures

Given an array of integers temperatures representing the daily temperatures, return an array answer
such that answer[i] is the number of days you have to wait after the ith day to get a warmer
temperature. If there is no future day for which this is possible, keep answer[i] == 0.

URL: https://leetcode.com/problems/daily-temperatures/
Difficulty: Medium
Category: Stack

Patterns:
- Monotonic Stack (decreasing)
- Index tracking for distance calculation

Complexity:
- Time: O(n) - each element is pushed and popped at most once
- Space: O(n) - stack can contain up to n indices in worst case

Pitfalls:
- Forgetting to handle remaining elements in stack (no warmer day found)
- Using values instead of indices in stack (need indices for distance calculation)
- Not maintaining stack in decreasing order of temperatures

Follow-ups:
- What if we need to find previous warmer temperature instead?
- How would you modify for finding next cooler temperature?
- Can you solve this with O(1) extra space? (No, need stack for optimal solution)
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        Find number of days to wait for next warmer temperature using monotonic stack.

        Algorithm:
        1. Use stack to store indices of temperatures in decreasing order
        2. For each temperature, pop stack while current temp is warmer
        3. For each popped index, calculate days difference and store result
        4. Push current index to maintain decreasing order
        5. Remaining indices in stack have no warmer future day (result = 0)

        Args:
            temperatures: List of daily temperatures

        Returns:
            List of days to wait for next warmer temperature (0 if none)
        """
        n = len(temperatures)
        result = [0] * n  # Initialize all to 0 (no warmer day found)
        stack = []  # Store indices in decreasing order of temperatures

        for i, temp in enumerate(temperatures):
            # While stack not empty and current temp is warmer than temp at stack top
            while stack and temperatures[stack[-1]] < temp:
                prev_index = stack.pop()
                result[prev_index] = i - prev_index  # Days difference

            stack.append(i)  # Add current index to stack

        # Remaining indices in stack have no warmer future day (already 0)
        return result


# Test cases
test_cases = [
    TestCase(
        ([73, 74, 75, 71, 69, 72, 76, 73],),
        [1, 1, 4, 2, 1, 1, 0, 0],
        "Example 1: Mixed temperatures with warmer days",
    ),
    TestCase(([30, 40, 50, 60],), [1, 1, 1, 0], "Example 2: Strictly increasing temperatures"),
    TestCase(([30, 60, 90],), [1, 1, 0], "Example 3: Each day warmer than previous"),
    TestCase(([90, 60, 30],), [0, 0, 0], "Decreasing temperatures - no warmer days"),
    TestCase(([75],), [0], "Single temperature - no future day"),
    TestCase(([75, 75],), [0, 0], "Equal temperatures - neither is warmer"),
    TestCase(([70, 70, 70, 75],), [3, 2, 1, 0], "Equal temps then warmer"),
    TestCase(([80, 70, 60, 70, 90],), [4, 3, 1, 1, 0], "Complex pattern with dips and peaks"),
    TestCase(([60, 70, 65, 75],), [1, 2, 1, 0], "Up-down-up pattern"),
    TestCase(
        ([100, 99, 98, 97, 96, 95],), [0, 0, 0, 0, 0, 0], "Strictly decreasing - no warmer days"
    ),
]


def demo() -> str:
    """Run Daily Temperatures demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.dailyTemperatures, test_cases, "LeetCode 739: Daily Temperatures"
    )

    return create_demo_output(
        "Daily Temperatures",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use monotonic stack to efficiently find next greater element
2. Store indices (not values) in stack for distance calculation
3. Maintain decreasing order of temperatures in stack
4. Each element pushed/popped exactly once → O(n) time complexity

Algorithm steps:
- Initialize result array with zeros
- Use stack to track indices of unresolved temperatures
- For each temperature, resolve all smaller temperatures in stack
- Push current index to maintain monotonic decreasing order
        """.strip(),
    )


# Register the problem
register_problem(
    id=739,
    slug="daily_temperatures",
    title="Daily Temperatures",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "stack", "monotonic_stack"],
    url="https://leetcode.com/problems/daily-temperatures/",
    notes="Classic monotonic stack problem for finding next greater element with distance calculation",
)
