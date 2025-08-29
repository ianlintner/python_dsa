"""
Surrounded Regions

TODO: Add problem description
"""


class Solution:
    def solve(self, board):
        """Capture surrounded regions (flip O not connected to border)."""
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            if (
                r < 0
                or c < 0
                or r >= rows
                or c >= cols
                or board[r][c] != "O"
            ):
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


def demo():
    """Run a demo for the Surrounded Regions problem."""
    solver = Solution()
    board = [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"],
    ]
    result = solver.solve(board)
    return str(result)


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="surrounded_regions",
#     title="Surrounded Regions",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
