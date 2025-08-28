"""
LeetCode 417: Pacific Atlantic Water Flow

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean.
The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches
the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n integer
matrix heights where heights[r][c] represents the height above sea level of the cell at
coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring cells directly
north, south, east, or west if the neighboring cell's height is less than or equal to the
current cell's height. Water can flow from any cell adjacent to an ocean into that ocean.

Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain
water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.
"""

from collections import deque


class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        """
        Multi-source DFS approach - start from ocean borders and work inward.

        Key insight: Instead of checking if water can flow FROM each cell TO oceans,
        we check which cells can be reached FROM the oceans (reverse flow).

        Time: O(m*n) - visit each cell at most twice
        Space: O(m*n) - for the visited sets
        """
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])

        # Track cells that can reach each ocean
        pacific_reachable = set()
        atlantic_reachable = set()

        def dfs(r: int, c: int, reachable: set, prev_height: int) -> None:
            """DFS to find all cells reachable from ocean borders"""
            # Check bounds and if already visited
            if (
                r < 0
                or r >= m
                or c < 0
                or c >= n
                or (r, c) in reachable
                or heights[r][c] < prev_height
            ):
                return

            reachable.add((r, c))

            # Explore all 4 directions
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(r + dr, c + dc, reachable, heights[r][c])

        # Start DFS from Pacific Ocean borders (top and left edges)
        for i in range(m):
            dfs(i, 0, pacific_reachable, 0)  # Left edge
        for j in range(n):
            dfs(0, j, pacific_reachable, 0)  # Top edge

        # Start DFS from Atlantic Ocean borders (bottom and right edges)
        for i in range(m):
            dfs(i, n - 1, atlantic_reachable, 0)  # Right edge
        for j in range(n):
            dfs(m - 1, j, atlantic_reachable, 0)  # Bottom edge

        # Find intersection - cells reachable by both oceans
        return [[r, c] for r, c in pacific_reachable & atlantic_reachable]

    def pacificAtlanticBFS(self, heights: list[list[int]]) -> list[list[int]]:
        """
        Multi-source BFS approach using queues.

        Time: O(m*n)
        Space: O(m*n)
        """
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])

        pacific_visited = [[False] * n for _ in range(m)]
        atlantic_visited = [[False] * n for _ in range(m)]

        pacific_queue = deque()
        atlantic_queue = deque()

        # Initialize queues with border cells
        for i in range(m):
            pacific_queue.append((i, 0))  # Left border
            pacific_visited[i][0] = True
            atlantic_queue.append((i, n - 1))  # Right border
            atlantic_visited[i][n - 1] = True

        for j in range(n):
            pacific_queue.append((0, j))  # Top border
            pacific_visited[0][j] = True
            atlantic_queue.append((m - 1, j))  # Bottom border
            atlantic_visited[m - 1][j] = True

        def bfs(queue: deque, visited: list[list[bool]]) -> None:
            """BFS to find all reachable cells from ocean"""
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    if (
                        0 <= nr < m
                        and 0 <= nc < n
                        and not visited[nr][nc]
                        and heights[nr][nc] >= heights[r][c]
                    ):
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        # Run BFS from both oceans
        bfs(pacific_queue, pacific_visited)
        bfs(atlantic_queue, atlantic_visited)

        # Find cells reachable by both oceans
        result = []
        for i in range(m):
            for j in range(n):
                if pacific_visited[i][j] and atlantic_visited[i][j]:
                    result.append([i, j])

        return result

    def pacificAtlanticBruteForce(self, heights: list[list[int]]) -> list[list[int]]:
        """
        Brute force: For each cell, check if it can reach both oceans.

        Time: O(m*n * (m+n)) - potentially explore entire grid for each cell
        Space: O(m*n) - recursion stack
        """
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])
        result = []

        def can_reach_ocean(r: int, c: int, target: str, visited: set) -> bool:
            """Check if cell (r,c) can reach specified ocean"""
            if (r, c) in visited:
                return False

            # Check if reached ocean borders
            if target == "pacific" and (r == 0 or c == 0):
                return True
            if target == "atlantic" and (r == m - 1 or c == n - 1):
                return True

            visited.add((r, c))

            # Try all 4 directions - water flows to cells with <= height
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and heights[nr][nc] <= heights[r][c]:
                    if can_reach_ocean(nr, nc, target, visited):
                        visited.remove((r, c))
                        return True

            visited.remove((r, c))
            return False

        # Check each cell
        for i in range(m):
            for j in range(n):
                if can_reach_ocean(i, j, "pacific", set()) and can_reach_ocean(
                    i, j, "atlantic", set()
                ):
                    result.append([i, j])

        return result


def create_demo_output() -> str:
    """
    Comprehensive demo showing water flow analysis with different approaches.
    """
    solution = Solution()

    demo_cases = [
        {
            "name": "Example 1: Mixed Heights",
            "heights": [
                [1, 2, 2, 3, 5],
                [3, 2, 3, 4, 4],
                [2, 4, 5, 3, 1],
                [6, 7, 1, 4, 5],
                [5, 1, 1, 2, 4],
            ],
        },
        {"name": "Example 2: Uniform Heights", "heights": [[1, 1], [1, 1]]},
        {"name": "Example 3: Single Cell", "heights": [[1]]},
        {"name": "Example 4: Diagonal Gradient", "heights": [[1, 2, 3], [2, 3, 4], [3, 4, 5]]},
    ]

    output = ["=== Pacific Atlantic Water Flow Analysis ===\n"]

    for case in demo_cases:
        heights = case["heights"]
        output.append(f"📊 {case['name']}:")
        output.append("Grid:")
        for row in heights:
            output.append("  " + " ".join(f"{x:2d}" for x in row))

        # Get results from different approaches
        result_dfs = solution.pacificAtlantic(heights)
        result_bfs = solution.pacificAtlanticBFS(heights)

        output.append(f"✅ Cells reaching both oceans: {len(result_dfs)}")
        output.append(f"   Coordinates: {sorted(result_dfs)}")

        # Visualization
        if heights:
            m, n = len(heights), len(heights[0])
            grid_visual = [["." for _ in range(n)] for _ in range(m)]
            for r, c in result_dfs:
                grid_visual[r][c] = "✓"

            output.append("Visualization (✓ = can reach both oceans):")
            for row in grid_visual:
                output.append("  " + " ".join(f"{x:2s}" for x in row))

        output.append("")

    # Algorithm comparison
    output.append("🔍 Algorithm Analysis:")
    output.append("1. Multi-source DFS (Optimal):")
    output.append("   • Start from ocean borders, work inward")
    output.append("   • Time: O(m*n), Space: O(m*n)")
    output.append("   • Key insight: Reverse the problem direction")
