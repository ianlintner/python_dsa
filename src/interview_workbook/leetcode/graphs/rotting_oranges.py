"""
Rotting Oranges

TODO: Add problem description
"""
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


from collections import deque

class Solution:
    def solve(self, grid):
        """Return minutes until all oranges rot or -1 if impossible."""
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        while queue and fresh > 0:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == 1
                    ):
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1


def demo():
    """Run a demo for the Rotting Oranges problem."""
    solver = Solution()
    grid = [
        [2,1,1],
        [1,1,0],
        [0,1,1],
    ]
    result = solver.solve(grid)
    return str(result)


register_problem(
    id=994,
    slug="rotting_oranges",
    title="Rotting Oranges",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "bfs"],
    url="https://leetcode.com/problems/rotting-oranges/",
    notes="",
)
