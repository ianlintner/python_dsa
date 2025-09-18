"""
Pacific Atlantic Water Flow

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, heights):
        """Return coordinates from which water can flow to both Pacific and Atlantic."""
        if not heights:
            return []
        rows, cols = len(heights), len(heights[0])

        def dfs(r, c, visited, prevHeight):
            if (
                r < 0
                or c < 0
                or r >= rows
                or c >= cols
                or (r, c) in visited
                or heights[r][c] < prevHeight
            ):
                return
            visited.add((r, c))
            dfs(r + 1, c, visited, heights[r][c])
            dfs(r - 1, c, visited, heights[r][c])
            dfs(r, c + 1, visited, heights[r][c])
            dfs(r, c - 1, visited, heights[r][c])

        pacific, atlantic = set(), set()
        for c in range(cols):
            dfs(0, c, pacific, heights[0][c])
            dfs(rows - 1, c, atlantic, heights[rows - 1][c])
        for r in range(rows):
            dfs(r, 0, pacific, heights[r][0])
            dfs(r, cols - 1, atlantic, heights[r][cols - 1])

        return list(pacific & atlantic)


def demo() -> str:
    """Run a demo for the Pacific Atlantic Water Flow problem."""
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    print("Initial heights matrix:")
    for row in heights:
        print(row)
    s = Solution()
    result = s.solve(heights)
    print(f"Final result: {result}")
    return f"Pacific Atlantic Water Flow result -> {result}"


if __name__ == "__main__":
    demo()


register_problem(
    id=417,
    slug="pacific_atlantic_water_flow",
    title="Pacific Atlantic Water Flow",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dfs", "bfs"],
    url="https://leetcode.com/problems/pacific-atlantic-water-flow/",
    notes="",
)
