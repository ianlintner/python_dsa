"""
Rotting Oranges

TODO: Add problem description
"""


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
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="rotting_oranges",
#     title="Rotting Oranges",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
