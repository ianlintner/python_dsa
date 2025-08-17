def solve_n_queens(n: int) -> list[list[str]]:
    """
    N-Queens backtracking.

    Time: O(n!) worst-case
    Space: O(n) for recursion + O(n) for sets

    Returns boards as list of strings.
    """
    res: list[list[str]] = []
    board = ["." * n for _ in range(n)]
    cols: set[int] = set()
    diag1: set[int] = set()  # r - c
    diag2: set[int] = set()  # r + c

    def place(r: int):
        if r == n:
            res.append(board.copy())
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            board[r] = board[r][:c] + "Q" + board[r][c + 1 :]
            place(r + 1)
            board[r] = board[r][:c] + "." + board[r][c + 1 :]
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)

    place(0)
    return res


def solve_sudoku(board: list[list[str]]) -> bool:
    """
    Sudoku solver (9x9) with backtracking.
    Mutates board in-place; returns True if solved.

    Empty cell = '.'
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties: list[tuple[int, int]] = []

    def box_id(r: int, c: int) -> int:
        return (r // 3) * 3 + (c // 3)

    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == ".":
                empties.append((r, c))
            else:
                rows[r].add(ch)
                cols[c].add(ch)
                boxes[box_id(r, c)].add(ch)

    def dfs(i: int) -> bool:
        if i == len(empties):
            return True
        r, c = empties[i]
        b = box_id(r, c)
        for d in map(str, range(1, 10)):
            if d in rows[r] or d in cols[c] or d in boxes[b]:
                continue
            rows[r].add(d)
            cols[c].add(d)
            boxes[b].add(d)
            board[r][c] = d
            if dfs(i + 1):
                return True
            board[r][c] = "."
            rows[r].remove(d)
            cols[c].remove(d)
            boxes[b].remove(d)
        return False

    return dfs(0)


def exist_word(board: list[list[str]], word: str) -> bool:
    """
    Word Search (LeetCode 79): Check if word exists in board scanning 4-dir.

    Time: O(n*m*len(word))
    Space: O(len(word)) recursion
    """
    if not board or not board[0]:
        return False
    R, C = len(board), len(board[0])

    def dfs(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if r < 0 or r >= R or c < 0 or c >= C or board[r][c] != word[i]:
            return False
        ch = board[r][c]
        board[r][c] = "#"  # mark
        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )
        board[r][c] = ch
        return found

    for r in range(R):
        for c in range(C):
            if dfs(r, c, 0):
                return True
    return False


def demo():
    print("Backtracking Patterns Demo")
    print("=" * 40)

    # N-Queens
    n = 4
    solutions = solve_n_queens(n)
    print(f"N-Queens n={n}, solutions={len(solutions)}")
    for sol in solutions[:2]:
        for row in sol:
            print(row)
        print()
    if len(solutions) > 2:
        print(f"... and {len(solutions) - 2} more solutions")
    print()

    # Sudoku
    sudoku = [
        list("53..7...."),
        list("6..195..."),
        list(".98....6."),
        list("8...6...3"),
        list("4..8.3..1"),
        list("7...2...6"),
        list(".6....28."),
        list("...419..5"),
        list("....8..79"),
    ]
    print("Sudoku solving (partial board):")
    solved = solve_sudoku(sudoku)
    print(f"Solved: {solved}")
    for row in sudoku:
        print("".join(row))
    print()

    # Word Search
    board = [
        list("ABCE"),
        list("SFCS"),
        list("ADEE"),
    ]
    word = "ABCCED"
    print(f"Word Search for '{word}': {exist_word([row[:] for row in board], word)}")
    print()


if __name__ == "__main__":
    demo()
