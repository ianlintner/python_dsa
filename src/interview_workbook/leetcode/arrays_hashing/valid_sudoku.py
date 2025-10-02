"""
Valid Sudoku

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, board: list[list[str]]) -> bool:
        """Check if a Sudoku board is valid."""
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == ".":
                    continue
                if (
                    val in rows[r]
                    or val in cols[c]
                    or val in boxes[(r // 3) * 3 + (c // 3)]
                ):
                    return False
                rows[r].add(val)
                cols[c].add(val)
                boxes[(r // 3) * 3 + (c // 3)].add(val)
        return True


def demo():
    """Demonstrate valid sudoku solution."""
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    sol = Solution()
    print(f"Input board:\n{board}")
    print(f"Is valid Sudoku? {sol.solve(board)}")
    assert sol.solve(board) is True
    return "Valid Sudoku demo passed."


register_problem(
    id=36,
    slug="valid_sudoku",
    title="Valid Sudoku",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hashmap"],
    url="https://leetcode.com/problems/valid-sudoku/",
    notes="",
)
