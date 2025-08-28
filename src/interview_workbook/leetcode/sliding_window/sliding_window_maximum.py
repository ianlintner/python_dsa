"""
LeetCode 239: Sliding Window Maximum

You are given an array of integers nums, there is a sliding window of size k which is moving
from the very left of the array to the very right. You can only see the k numbers in the window.
Each time the sliding window moves right by one position.

Return the max sliding window.

URL: https://leetcode.com/problems/sliding-window-maximum/
Difficulty: Hard
Category: Sliding Window

Patterns:
- Monotonic deque for maintaining maximum in sliding window
- Deque stores indices, not values, for position tracking
- Remove elements outside window and smaller elements

Complexity:
- Time: O(n) - each element added and removed at most once
- Space: O(k) - deque stores at most k elements

Key Insights:
- Use deque to maintain decreasing order of elements
- Store indices instead of values to track window boundaries
- Remove indices outside current window from front
- Remove smaller elements from back before adding new element
- Front of deque always contains index of maximum element

Edge Cases:
- Window size equals array length (single maximum)
- Array with duplicate maximum values
- Strictly increasing/decreasing arrays
- Single element array
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty
from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Find maximum in each sliding window of size k.

        Args:
            nums: Array of integers
            k: Window size

        Returns:
            Array of maximum values for each window position
        """
        if not nums or k == 0:
            return []

        result = []
        # Deque stores indices in decreasing order of their values
        dq = deque()

        for i in range(len(nums)):
            # Remove indices outside current window
            while dq and dq[0] <= i - k:
                dq.popleft()

            # Remove indices whose values are smaller than current element
            # (they can never be maximum while current element is in window)
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()

            # Add current index
            dq.append(i)

            # Add maximum to result when window size is reached
            if i >= k - 1:
                result.append(nums[dq[0]])

        return result

    def maxSlidingWindowBruteForce(self, nums: List[int], k: int) -> List[int]:
        """
        Brute force solution for comparison - O(nk) time complexity.

        Args:
            nums: Array of integers
            k: Window size

        Returns:
            Array of maximum values for each window position
        """
        if not nums or k == 0:
            return []

        result = []
        for i in range(len(nums) - k + 1):
            window_max = max(nums[i : i + k])
            result.append(window_max)

        return result


# Test cases
test_cases = [
    TestCase(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7], "Basic sliding window"),
    TestCase(([1], 1), [1], "Single element"),
    TestCase(([1, -1], 1), [1, -1], "Window size 1"),
    TestCase(([9, 11], 2), [11], "Two elements, window size 2"),
    TestCase(
        ([4, -2, -3, 4, -1, 2, 1, -5, 4], 3), [4, 4, 4, 4, 2, 2, 1, 4], "Mixed positive/negative"
    ),
    TestCase(([1, 2, 3, 4, 5], 3), [3, 4, 5], "Increasing sequence"),
    TestCase(([5, 4, 3, 2, 1], 3), [5, 4, 3], "Decreasing sequence"),
    TestCase(([7, 2, 4], 2), [7, 4], "Simple case"),
]


def demo() -> str:
    """Run Sliding Window Maximum demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.maxSlidingWindow, test_cases, "LeetCode 239: Sliding Window Maximum"
    )

    return create_demo_output(
        "Sliding Window Maximum",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(k)",
        approach_notes="""
Key insights:
1. Use monotonic decreasing deque to efficiently track window maximum
2. Store indices instead of values to handle window boundary checks
3. Remove indices outside current window from front of deque
4. Remove indices with smaller values from back before adding new index
5. Front of deque always contains index of current window maximum

Algorithm steps:
- For each element, remove outdated indices from front
- Remove smaller elements from back (they can't be maximum)
- Add current index to back
- Record maximum (front of deque) when window is complete

This achieves O(n) time complexity because each element is added and removed
from deque at most once, compared to O(nk) brute force approach.
        """.strip(),
    )


# Register the problem
register_problem(
    id=239,
    slug="sliding_window_maximum",
    title="Sliding Window Maximum",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.HARD,
    tags=["array", "sliding_window", "queue", "monotonic_stack"],
    url="https://leetcode.com/problems/sliding-window-maximum/",
    notes="Advanced sliding window problem using monotonic deque for efficient maximum tracking",
)
