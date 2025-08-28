"""
LeetCode 130: Surrounded Regions
https://leetcode.com/problems/surrounded-regions/

Given an m x n matrix board containing 'X' and 'O', capture all regions that are 4-directionally 
surrounded by 'X'. A region is captured by flipping all 'O's into 'X's in that surrounded region.
"""

from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def solve_dfs_border_escape(self, board: list[list[str]]) -> None:
        """
        DFS approach: Mark all 'O's connected to border as "safe", then flip remaining 'O's.
        
        Strategy:
        1. Start DFS from all border 'O's and mark them as safe (can't be captured)
        2. All 'O's not connected to border are surrounded and should be flipped
        3. Restore safe 'O's and flip surrounded ones to 'X'
        
        Time: O(m*n) - visit each cell at most once
        Space: O(m*n) - recursion stack in worst case
        """
        if not board or not board[0]:
            return
        
        m, n = len(board), len(board[0])
        
        def dfs(row: int, col: int) -> None:
            """Mark all 'O's connected to border as safe ('S')"""
            if (row < 0 or row >= m or col < 0 or col >= n or 
                board[row][col] != 'O'):
                return
                
            board[row][col] = 'S'  # Mark as safe
            
            # Explore 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(row + dr, col + dc)
        
        # 1. Mark all border-connected 'O's as safe
        # Top and bottom rows
        for col in range(n):
            if board[0][col] == 'O':
                dfs(0, col)
            if board[m-1][col] == 'O':
                dfs(m-1, col)
        
        # Left and right columns
        for row in range(m):
            if board[row][0] == 'O':
                dfs(row, 0)
            if board[row][n-1] == 'O':
                dfs(row, n-1)
        
        # 2. Process the board: flip surrounded 'O's, restore safe ones
        for row in range(m):
            for col in range(n):
                if board[row][col] == 'O':
                    board[row][col] = 'X'  # Surrounded, flip to X
                elif board[row][col] == 'S':
                    board[row][col] = 'O'  # Safe, restore to O

    def solve_bfs_border_escape(self, board: list[list[str]]) -> None:
        """
        BFS approach: Same strategy as DFS but using queue for iterative processing.
        
        Time: O(m*n) - each cell visited at most once
        Space: O(min(m,n)) - queue size bounded by border cells
        """
        if not board or not board[0]:
            return
        
        from collections import deque
        
        m, n = len(board), len(board[0])
        queue = deque()
        
        # Add all border 'O's to queue
        for row in range(m):
            for col in range(n):
                if ((row == 0 or row == m-1 or col == 0 or col == n-1) and 
                    board[row][col] == 'O'):
                    queue.append((row, col))
                    board[row][col] = 'S'  # Mark as safe
        
        # BFS to mark all connected 'O's as safe
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while queue:
            row, col = queue.popleft()
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < m and 0 <= new_col < n and 
                    board[new_row][new_col] == 'O'):
                    board[new_row][new_col] = 'S'
                    queue.append((new_row, new_col))
        
        # Finalize board
        for row in range(m):
            for col in range(n):
                if board[row][col] == 'O':
                    board[row][col] = 'X'
                elif board[row][col] == 'S':
                    board[row][col] = 'O'

    def solve_union_find(self, board: list[list[str]]) -> None:
        """
        Union-Find approach: Union all border-connected 'O's with a dummy border node.
        
        Time: O(m*n*α(m*n)) - where α is inverse Ackermann function
        Space: O(m*n) - for Union-Find structure
        """
        if not board or not board[0]:
            return
        
        m, n = len(board), len(board[0])
        
        class UnionFind:
            def __init__(self, size):
                self.parent = list(range(size))
                self.rank = [0] * size
            
            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])
                return self.parent[x]
            
            def union(self, x, y):
                px, py = self.find(x), self.find(y)
                if px == py:
                    return
                if self.rank[px] < self.rank[py]:
                    px, py = py, px
                self.parent[py] = px
                if self.rank[px] == self.rank[py]:
                    self.rank[px] += 1
        
        # Create Union-Find with extra node for border
        uf = UnionFind(m * n + 1)
        border_node = m * n
        
        def get_index(row, col):
            return row * n + col
        
        # Union all 'O's with their neighbors and border if applicable
        for row in range(m):
            for col in range(n):
                if board[row][col] == 'O':
                    idx = get_index(row, col)
                    
                    # If on border, union with border node
                    if row == 0 or row == m-1 or col == 0 or col == n-1:
                        uf.union(idx, border_node)
                    
                    # Union with adjacent 'O's
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < m and 0 <= new_col < n and 
                            board[new_row][new_col] == 'O'):
                            uf.union(idx, get_index(new_row, new_col))
        
        # Flip 'O's not connected to border
        for row in range(m):
            for col in range(n):
                if board[row][col] == 'O':
                    idx = get_index(row, col)
                    if uf.find(idx) != uf.find(border_node):
                        board[row][col] = 'X'

    def solve(self, board: list[list[str]]) -> None:
        """Main solution using DFS border escape approach"""
        self.solve_dfs_border_escape(board)


def create_demo_output() -> str:
    """Generate demonstration output for Surrounded Regions problem"""
    
    def board_to_string(board):
        return '\n'.join(''.join(row) for row in board)
    
    examples = [
        {
            "input": [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]],
            "description": "Classic example with internal surrounded region"
        },
        {
            "input": [["X"]],
            "description": "Single cell edge case"
        },
        {
            "input": [["O","O","O"],["O","O","O"],["O","O","O"]],
            "description": "All O's connected to border - none captured"
        },
        {
            "input": [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","O","X"]],
            "description": "Bottom row connected to border"
        }
    ]
    
    output = ["=== Surrounded Regions (LeetCode 130) ===\n"]
    output.append("Capture regions surrounded by 'X' by flipping 'O' to 'X'\n")
    
    solution = Solution()
    
    for i, example in enumerate(examples, 1):
        board_original = [row[:] for row in example["input"]]
        
        output.append(f"Example {i}: {example['description']}")
        output.append(f"Original board:")
        output.append(board_to_string(board_original))
        
        # Test DFS approach
        board_dfs = [row[:] for row in board_original]
        solution.solve_dfs_border_escape(board_dfs)
        output.append(f"After DFS solution:")
        output.append(board_to_string(board_dfs))
        
        # Test BFS approach
        board_bfs = [row[:] for row in board_original]
        solution.solve_bfs_border_escape(board_bfs)
        output.append(f"BFS result (should match): {board_to_string(board_bfs) == board_to_string(board_dfs)}")
        
        # Test Union-Find approach
        board_uf = [row[:] for row in board_original]
        solution.solve_union_find(board_uf)
        output.append(f"Union-Find result (should match): {board_to_string(board_uf) == board_to_string(board_dfs)}")
        output.append("")
    
    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. DFS Border Escape:")
    output.append("   - Time: O(m*n), Space: O(m*n) recursion")
    output.append("   - Most intuitive: escape from border")
    
    output.append("2. BFS Border Escape:")
    output.append("   - Time: O(m*n), Space: O(min(m,n)) queue")
    output.append("   - Iterative, better space for deep boards")
    
    output.append("3. Union-Find:")
    output.append("   - Time: O(m*n*α(m*n)), Space: O(m*n)")
    output.append("   - Good for connectivity problems")
    output.append("   - Overkill for this specific problem")
    
    output.append("\nKey Insight: 'Surrounded' means no path to border")
    output.append("Strategy: Find all border-connected regions first")
    
    return '\n'.join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data=[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]],
        expected=[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]],
        description="Standard case with surrounded region"
    ),
    TestCase(
        input_data=[["X"]],
        expected=[["X"]],
        description="Single cell X"
    ),
    TestCase(
        input_data=[["O"]],
        expected=[["O"]],
        description="Single cell O on border"
    ),
    TestCase(
        input_data=[["O","O","O"],["O","O","O"],["O","O","O"]],
        expected=[["O","O","O"],["O","O","O"],["O","O","O"]],
        description="All O's connected to border"
    ),
    TestCase(
        input_data=[["X","O","X"],["O","X","O"],["X","O","X"]],
        expected=[["X","O","X"],["O","X","O"],["X","O","X"]],
        description="Cross pattern - all O's on border"
    ),
    TestCase(
        input_data=[["X","X","X","X"],["X","O","O","X"],["X","O","O","X"],["X","X","X","X"]],
        expected=[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","X","X","X"]],
        description="2x2 surrounded region"
    )
]


def test_solution():
    """Test function for Surrounded Regions"""
    solution = Solution()
    
    def test_solve(board_input, expected, description):
        # Test main solve method
        board = [row[:] for row in board_input]  # Deep copy
        solution.solve(board)
        return board == expected
    
    test_cases_formatted = [
        TestCase(
            input_data=tc.input_data,
            expected=tc.expected,
            description=tc.description
        ) for tc in TEST_CASES
    ]
    
    return run_test_cases(test_solve, test_cases_formatted)


# Register the problem
register_problem(
    slug="surrounded_regions",
    leetcode_num=130,
    title="Surrounded Regions",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=Solution().solve,
    test_func=test_solution,
    demo_func=create_demo_output
)
