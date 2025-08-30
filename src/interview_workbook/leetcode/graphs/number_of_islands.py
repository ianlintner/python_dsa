"""
Number Of Islands

Problem: Number of Islands
LeetCode link: https://leetcode.com/problems/number-of-islands/
Description: Count the number of islands in a 2D grid where ‘1’ represents land and ‘0’ represents water. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
"""


class Solution:
    def solve(self, grid):
        """Count number of islands using DFS."""
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        visited = set()

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == "0" or (r, c) in visited:
                return
            visited.add((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        islands = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visited:
                    dfs(r, c)
                    islands += 1
        return islands


def demo():
    """Run demo for Number of Islands problem."""
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    solution = Solution()
    islands = solution.solve(grid)
    return f"Number of islands: {islands}"


# Register the problem with correct parameters
register_problem(
    id=200,
    slug="number_of_islands",
    title="Number Of Islands",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["dfs", "matrix"],
    url="https://leetcode.com/problems/number-of-islands/",
    notes="Classic flood fill DFS over 2D grid.",
)
