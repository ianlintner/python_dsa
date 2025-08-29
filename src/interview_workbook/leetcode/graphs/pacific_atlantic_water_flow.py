"""
Pacific Atlantic Water Flow

TODO: Add problem description
"""


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


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="pacific_atlantic_water_flow",
#     title="Pacific Atlantic Water Flow",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
