"""
Valid Sudoku - LeetCode Problem

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated
according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

Note:
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
- Only the filled cells need to be validated according to the mentioned rules.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """
        Validate sudoku board using hash sets for rows, columns, and sub-boxes.

        Time Complexity: O(1) - fixed 9x9 grid size
        Space Complexity: O(1) - fixed number of hash sets

        Args:
            board: 9x9 sudoku board with digits 1-9 or '.'

        Returns:
            bool: True if valid sudoku, False otherwise
        """
        # Track seen digits for each row, column, and 3x3 box
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for i in range(9):
            for j in range(9):
                cell = board[i][j]

                # Skip empty cells
                if cell == ".":
                    continue

                # Calculate which 3x3 box this cell belongs to
                box_index = (i // 3) * 3 + j // 3

                # Check if digit already exists in row, column, or box
                if cell in rows[i] or cell in cols[j] or cell in boxes[box_index]:
                    return False

                # Add digit to tracking sets
                rows[i].add(cell)
                cols[j].add(cell)
                boxes[box_index].add(cell)

        return True

    def isValidSudokuSingleSet(self, board: List[List[str]]) -> bool:
        """
        Alternative using single set with encoded strings.

        Time Complexity: O(1) - fixed 9x9 grid size
        Space Complexity: O(1) - single set with at most 243 elements
        """
        seen = set()

        for i in range(9):
            for j in range(9):
                cell = board[i][j]

                if cell == ".":
                    continue

                # Create unique identifiers for row, column, and box
                row_key = f"{cell} in row {i}"
                col_key = f"{cell} in col {j}"
                box_key = f"{cell} in box {i // 3}-{j // 3}"

                # Check if any identifier already exists
                if row_key in seen or col_key in seen or box_key in seen:
                    return False

                # Add all identifiers
                seen.add(row_key)
                seen.add(col_key)
                seen.add(box_key)

        return True

    def isValidSudokuBruteForce(self, board: List[List[str]]) -> bool:
        """
        Brute force approach checking each constraint separately.

        Time Complexity: O(1) - fixed 9x9 grid size, but higher constant factor
        Space Complexity: O(1) - no extra data structures
        """

        def is_valid_unit(unit):
            """Check if a row, column, or box contains valid digits."""
            digits = [cell for cell in unit if cell != "."]
            return len(digits) == len(set(digits))

        # Check all rows
        for row in board:
            if not is_valid_unit(row):
                return False

        # Check all columns
        for j in range(9):
            column = [board[i][j] for i in range(9)]
            if not is_valid_unit(column):
                return False

        # Check all 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row * 3 + i][box_col * 3 + j])
                if not is_valid_unit(box):
                    return False

        return True


def demo():
    """Demonstrate Valid Sudoku solution with test cases."""
    solution = Solution()

    # Helper function to create test boards
    def create_board(rows):
        return [list(row) for row in rows]

    test_cases = [
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        "53..7....",
                        "6..195...",
                        ".98....6.",
                        "8...6...3",
                        "4..8.3..1",
                        "7...2...6",
                        ".6....28.",
                        "...419..5",
                        "....8..79",
                    ],
    ),
            ),
            expected=True,
            description="Valid sudoku board",
        ),
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        "83..7....",
                        "6..195...",
                        ".98....6.",
                        "8...6...3",
                        "4..8.3..1",
                        "7...2...6",
                        ".6....28.",
                        "...419..5",
                        "....8..79",
                    ],
    ),
            ),
            expected=False,
            description="Invalid - duplicate 8 in first row",
        ),
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                    ],
    ),
            ),
            expected=True,
            description="Empty board",
        ),
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        "1........",
                        ".1.......",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                    ],
    ),
            ),
            expected=False,
            description="Invalid - duplicate 1 in first column",
        ),
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        "12.......",
                        "34.......",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                    ],
    ),
            ),
            expected=False,
            description="Invalid - duplicate in 3x3 box (1,2,3,4 all in top-left)",
        ),
        TestCase(
        input_args=input_args=(
                create_board(
                    [
                        "123456789",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                        ".........",
                    ],
    ),
            ),
            expected=True,
            description="Valid single row filled",
        ),
    ]

    results = run_test_cases(solution.isValidSudoku, test_cases)

    return create_demo_output(
        problem_title="Valid Sudoku",
        test_results=results,
        time_complexity="O(1) - fixed 9x9 grid size (81 cells)",
        space_complexity="O(1) - fixed number of hash sets (27 sets total)",
        approach_notes="Use separate hash sets for rows, columns, and 3x3 boxes",
    )


# Register this problem
register_problem(
    id=36,
    slug="valid-sudoku",
    title="Valid Sudoku",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hash-table"],
    url="https://leetcode.com/problems/valid-sudoku/",
    notes="Hash set validation of sudoku constraints for rows, columns, and boxes",
)
