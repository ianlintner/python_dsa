"""
Largest Rectangle In Histogram

TODO: Add problem description
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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="largest_rectangle_in_histogram",
#     title="Largest Rectangle In Histogram",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
