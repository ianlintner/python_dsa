"""
Largest Rectangle In Histogram

Given a histogram represented by an array of bar heights,
find the area of the largest rectangle in it.
"""


class Solution:
    def solve(self, heights) -> int:
        """Return maximum area of a rectangle in the histogram."""
        stack = []
        max_area = 0
        heights.append(0)
        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)
        heights.pop()
        return max_area


def demo():
    return str(Solution().solve([2,1,5,6,2,3]))


from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty

register_problem(
    id=84,
    slug="largest_rectangle_in_histogram",
    title="Largest Rectangle In Histogram",
    category=Category.STACK,
    difficulty=Difficulty.HARD,
    tags=["stack", "monotonic stack"],
    url="https://leetcode.com/problems/largest-rectangle-in-histogram/",
    notes="Monotonic increasing stack to compute max rectangle area.",
)
