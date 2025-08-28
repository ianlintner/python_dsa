"""
LeetCode 200: Number of Islands

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count number of islands using DFS to mark connected land cells.

        Key insight: Each '1' cell that hasn't been visited represents a potential
        new island. Use DFS to mark all connected '1' cells as visited, then increment
        island count.

        Time: O(m * n) where m = rows, n = cols. Each cell visited at most once.
        Space: O(m * n) in worst case for recursion stack (if all cells are '1').

        Args:
            grid: 2D grid of '0' (water) and '1' (land) characters

        Returns:
            Number of separate islands
        """
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(r: int, c: int) -> None:
            """DFS to mark all connected land cells as visited."""
            # Base cases: out of bounds or water/already visited
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
                return

            # Mark current cell as visited by changing '1' to '0'
            grid[r][c] = "0"

            # Explore all 4 directions
            dfs(r + 1, c)  # down
            dfs(r - 1, c)  # up
            dfs(r, c + 1)  # right
            dfs(r, c - 1)  # left

        # Scan entire grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":  # Found unvisited land
                    islands += 1
                    dfs(r, c)  # Mark entire island as visited

        return islands

    def numIslandsBFS(self, grid: List[List[str]]) -> int:
        """
        Count islands using BFS instead of DFS.

        BFS explores level by level, which can be better for very deep islands
        to avoid stack overflow issues.

        Time: O(m * n)
        Space: O(min(m, n)) for BFS queue in worst case
        """
        from collections import deque

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    islands += 1

                    # BFS to mark entire island
                    queue = deque([(r, c)])
                    grid[r][c] = "0"  # Mark as visited

                    while queue:
                        curr_r, curr_c = queue.popleft()

                        for dr, dc in directions:
                            nr, nc = curr_r + dr, curr_c + dc

                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                                grid[nr][nc] = "0"  # Mark as visited
                                queue.append((nr, nc))

        return islands

    def numIslandsUnionFind(self, grid: List[List[str]]) -> int:
        """
        Count islands using Union-Find (Disjoint Set Union) data structure.

        This approach is overkill for this problem but demonstrates how
        Union-Find can be used for connectivity problems.

        Time: O(m * n * α(m*n)) where α is inverse Ackermann function
        Space: O(m * n) for parent and rank arrays
        """
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])

        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n))
                self.rank = [0] * n
                self.components = n

            def find(self, x):
                if self.parent[x] != x:
                    self.parent[x] = self.find(self.parent[x])  # Path compression
                return self.parent[x]

            def union(self, x, y):
                root_x, root_y = self.find(x), self.find(y)
                if root_x != root_y:
                    # Union by rank
                    if self.rank[root_x] < self.rank[root_y]:
                        root_x, root_y = root_y, root_x
                    self.parent[root_y] = root_x
                    if self.rank[root_x] == self.rank[root_y]:
                        self.rank[root_x] += 1
                    self.components -= 1

        # Convert 2D coordinates to 1D index
        def get_index(r, c):
            return r * cols + c

        # Count land cells and create Union-Find
        land_cells = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    land_cells += 1

        if land_cells == 0:
            return 0

        uf = UnionFind(rows * cols)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Union adjacent land cells
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                            uf.union(get_index(r, c), get_index(nr, nc))

        # Count unique components among land cells
        unique_roots = set()
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    unique_roots.add(uf.find(get_index(r, c)))

        return len(unique_roots)


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to counting islands.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 200: Number of Islands - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        (
            [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ],
            "Single large island",
        ),
        (
            [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ],
            "Multiple separate islands",
        ),
        ([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]], "Diagonal islands (not connected)"),
        ([["1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]], "All land - single island"),
        ([["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]], "All water - no islands"),
        ([[]], "Empty grid"),
        ([["1"]], "Single cell island"),
    ]

    for grid, description in test_cases:
        demo_parts.append(f"\nTest Case: {description}")
        demo_parts.append(f"Grid ({len(grid)}x{len(grid[0]) if grid else 0}):")
        for row in grid:
            demo_parts.append(f"  {row}")

        # Test different approaches (make copies since DFS modifies grid)
        grid_copy1 = [row[:] for row in grid] if grid else []
        grid_copy2 = [row[:] for row in grid] if grid else []
        grid_copy3 = [row[:] for row in grid] if grid else []

        result1 = solution.numIslands(grid_copy1) if grid else 0
        result2 = solution.numIslandsBFS(grid_copy2) if grid else 0
        result3 = solution.numIslandsUnionFind(grid_copy3) if grid else 0

        demo_parts.append(f"DFS result: {result1} islands")
        demo_parts.append(f"BFS result: {result2} islands")
        demo_parts.append(f"Union-Find result: {result3} islands")
        demo_parts.append(f"All approaches consistent: {result1 == result2 == result3}")

    # Algorithm analysis
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nDepth-First Search (DFS):")
    demo_parts.append("  • Time: O(m * n) - each cell visited once")
    demo_parts.append("  • Space: O(m * n) - recursion stack in worst case")
    demo_parts.append("  • Pros: Simple implementation, modifies grid in-place")
    demo_parts.append("  • Cons: Can cause stack overflow for large grids")

    demo_parts.append("\nBreadth-First Search (BFS):")
    demo_parts.append("  • Time: O(m * n) - each cell visited once")
    demo_parts.append("  • Space: O(min(m, n)) - queue size bounded by grid dimensions")
    demo_parts.append("  • Pros: Avoids recursion stack issues, level-by-level exploration")
    demo_parts.append("  • Cons: Slightly more complex implementation")

    demo_parts.append("\nUnion-Find:")
    demo_parts.append("  • Time: O(m * n * α(m*n)) - α is inverse Ackermann")
    demo_parts.append("  • Space: O(m * n) - parent and rank arrays")
    demo_parts.append("  • Pros: Useful for dynamic connectivity, doesn't modify input")
    demo_parts.append("  • Cons: Overkill for this static problem, more complex")

    # Problem patterns
    demo_parts.append("\n=== Common Patterns ===")
    demo_parts.append("This problem demonstrates several important graph concepts:")
    demo_parts.append("")
    demo_parts.append("1. **Connected Components**: Each island is a connected component")
    demo_parts.append("2. **Grid as Graph**: 2D array treated as implicit graph")
    demo_parts.append("3. **Marking Visited**: Modify grid or use separate visited array")
    demo_parts.append("4. **4-Directional Movement**: Up, down, left, right neighbors")
    demo_parts.append("5. **Flood Fill**: DFS/BFS spreads through connected cells")

    # Variations and extensions
    demo_parts.append("\n=== Problem Variations ===")
    demo_parts.append("1. **Max Area of Island**: Find size of largest island")
    demo_parts.append("2. **Number of Distinct Islands**: Count unique island shapes")
    demo_parts.append("3. **Making Islands**: Minimum flips to connect all islands")
    demo_parts.append("4. **Surrounded Regions**: Mark regions surrounded by different value")
    demo_parts.append("5. **Word Search**: DFS in grid with backtracking")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. **Geographic Analysis**: Counting land masses in satellite data")
    demo_parts.append("2. **Image Processing**: Connected component labeling")
    demo_parts.append("3. **Game Development**: Terrain analysis, region detection")
    demo_parts.append("4. **Network Analysis**: Finding clusters in adjacency matrices")
    demo_parts.append("5. **Social Networks**: Community detection algorithms")
    demo_parts.append("6. **Circuit Design**: Finding connected components in layouts")

    # Implementation tips
    demo_parts.append("\n=== Implementation Tips ===")
    demo_parts.append("1. **Boundary Checking**: Always validate indices before accessing")
    demo_parts.append(
        "2. **State Management**: Decide between in-place modification vs. visited array"
    )
    demo_parts.append(
        "3. **Direction Arrays**: Use [(1,0), (-1,0), (0,1), (0,-1)] for cleaner code"
    )
    demo_parts.append("4. **Stack Overflow**: Consider BFS for very large or dense grids")
    demo_parts.append("5. **Memory Optimization**: Reuse input grid to mark visited if allowed")

    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        input_data={
            "grid": [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ]
        },
        expected_output=1,
        description="Single large connected island",
    ),
    TestCase(
        input_data={
            "grid": [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ]
        },
        expected_output=3,
        description="Three separate islands",
    ),
    TestCase(
        input_data={"grid": [["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]},
        expected_output=5,
        description="Five single-cell islands (diagonal not connected)",
    ),
    TestCase(
        input_data={"grid": [["1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]]},
        expected_output=1,
        description="All land forms single island",
    ),
    TestCase(
        input_data={"grid": [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]},
        expected_output=0,
        description="All water - no islands",
    ),
    TestCase(input_data={"grid": [["1"]]}, expected_output=1, description="Single cell island"),
    TestCase(input_data={"grid": [["0"]]}, expected_output=0, description="Single cell water"),
]


def test_solution():
    """Test the solution with all test cases."""

    def test_function(grid):
        # Make a copy since the solution modifies the grid
        grid_copy = [row[:] for row in grid]
        solution = Solution()
        return solution.numIslands(grid_copy)

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="number-of-islands",
    leetcode_num=200,
    title="Number of Islands",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=lambda grid: Solution().numIslands(
        [row[:] for row in grid]
    ),  # Copy to avoid mutation
    test_func=test_solution,
    demo_func=create_demo_output,
)
