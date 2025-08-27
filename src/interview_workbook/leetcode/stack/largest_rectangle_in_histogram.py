"""
LeetCode 84: Largest Rectangle in Histogram

Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, 
return the area of the largest rectangle in the histogram.

URL: https://leetcode.com/problems/largest-rectangle-in-histogram/
Difficulty: Hard
Category: Stack

Patterns:
- Stack (monotonic increasing stack)
- Area calculation with boundaries
- Previous/Next smaller element

Complexity:
- Time: O(n) - each element pushed and popped at most once
- Space: O(n) - for the stack in worst case

Pitfalls:
- Forgetting to handle remaining elements in stack after iteration
- Incorrect boundary calculation when stack is empty
- Not handling edge cases (empty array, single element)
- Off-by-one errors in width calculation

Follow-ups:
- What if bars can have different widths?
- How to solve with O(1) space? (not possible optimally)
- Extension to 2D version (maximal rectangle in binary matrix)
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        Find the area of the largest rectangle in histogram.
        
        Algorithm:
        1. Use monotonic increasing stack to track indices of bars
        2. For each bar, if it's smaller than stack top, we found right boundary
        3. Pop from stack and calculate area using popped bar as height
        4. Left boundary is the bar after new stack top, right boundary is current bar
        5. Handle remaining bars in stack after iteration
        
        Args:
            heights: List of bar heights in histogram
            
        Returns:
            Maximum area of rectangle that can be formed
        """
        if not heights:
            return 0
            
        stack = []  # Stack to store indices of bars in increasing height order
        max_area = 0
        
        for i, height in enumerate(heights):
            # While current height is less than stack top, we've found right boundary
            while stack and heights[stack[-1]] > height:
                # Pop the bar and use it as the height of rectangle
                h = heights[stack.pop()]
                
                # Calculate width: right boundary (current i) - left boundary - 1
                # Left boundary is the bar after the new stack top (or -1 if stack empty)
                width = i if not stack else i - stack[-1] - 1
                
                # Update maximum area
                max_area = max(max_area, h * width)
            
            # Push current index to stack
            stack.append(i)
        
        # Handle remaining bars in stack (they extend to the end)
        while stack:
            h = heights[stack.pop()]
            width = len(heights) if not stack else len(heights) - stack[-1] - 1
            max_area = max(max_area, h * width)
        
        return max_area


# Test cases
test_cases = [
    TestCase(([2,1,5,6,2,3],), 10, 
             "Example 1: Heights [2,1,5,6,2,3] -> Rectangle of height 5, width 2 = 10"),
    TestCase(([2,4],), 4, 
             "Example 2: Heights [2,4] -> Rectangle of height 4, width 1 = 4"),
    TestCase(([1],), 1, 
             "Single bar"),
    TestCase(([2,2,2,2],), 8, 
             "All bars same height -> full width"),
    TestCase(([1,2,3,4,5],), 9, 
             "Increasing heights -> height 3, width 3 = 9"),
    TestCase(([5,4,3,2,1],), 9, 
             "Decreasing heights -> height 3, width 3 = 9"),
    TestCase(([0,2,0],), 2, 
             "Zero heights in between"),
    TestCase(([4,2,0,3,2,5],), 6, 
             "Complex case with zero -> height 3, width 2 = 6"),
    TestCase(([6,7,5,2,4,5,9,3],), 16, 
             "Complex histogram -> height 4, width 4 = 16"),
    TestCase(([],), 0, 
             "Empty array"),
]


def demo() -> str:
    """Run Largest Rectangle in Histogram demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.largestRectangleArea, test_cases, "LeetCode 84: Largest Rectangle in Histogram")

    return create_demo_output(
        "Largest Rectangle in Histogram",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use monotonic increasing stack to efficiently find boundaries
2. For each bar, stack contains previous smaller elements (left boundary info)
3. When we find a smaller bar, it serves as right boundary for bars in stack
4. Area calculation: height × width, where width = right_boundary - left_boundary - 1
5. Process remaining bars in stack after iteration (they extend to end of array)

Algorithm steps:
- Maintain stack of indices in increasing order of heights
- For each bar: pop taller bars from stack and calculate their maximum rectangles
- The popped bar's height × width from boundaries gives potential max area
- Handle remaining bars in stack that weren't bounded on the right
        """.strip(),
    )


# Register the problem
register_problem(
    id=84,
    slug="largest_rectangle_in_histogram",
    title="Largest Rectangle in Histogram",
    category=Category.STACK,
    difficulty=Difficulty.HARD,
    tags=['array', 'stack', 'monotonic_stack'],
    url="https://leetcode.com/problems/largest-rectangle-in-histogram/",
    notes="TODO: Add implementation notes",
)
