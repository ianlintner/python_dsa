"""
Surrounded Regions

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, board):
        """Capture surrounded regions (flip O not connected to border)."""
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != "O":
                return
            board[r][c] = "E"
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Mark border-connected O's
        for r in range(rows):
            dfs(r, 0)
            dfs(r, cols - 1)
        for c in range(cols):
            dfs(0, c)
            dfs(rows - 1, c)

        # Flip and restore
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "E":
                    board[r][c] = "O"
        return board


def demo() -> str:
    """Run a demo for the Surrounded Regions problem."""
    board = [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"]
    ]
    print("Initial board:")
    for row in board:
        print("".join(row))
    s = Solution()
    s.solve(board)
    print("Board after solve:")
    for row in board:
        print("".join(row))
    return "Surrounded Regions demo executed"


if __name__ == "__main__":
    demo()
    


register_problem(
    id=130,
    slug="surrounded_regions",
    title="Surrounded Regions",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "dfs", "bfs", "union_find"],
    url="https://leetcode.com/problems/surrounded-regions/",
    notes="",
)
