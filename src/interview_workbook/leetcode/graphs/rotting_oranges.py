"""
LeetCode 994: Rotting Oranges
https://leetcode.com/problems/rotting-oranges/

You are given an m x n grid where each cell can have one of three values:
- 0 representing an empty cell,
- 1 representing a fresh orange, or
- 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange.
If this is impossible, return -1.
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def orangesRotting_bfs_multi_source(self, grid: list[list[int]]) -> int:
        """
        Multi-source BFS approach: Start BFS from all rotten oranges simultaneously.

        Strategy:
        1. Add all initially rotten oranges to queue
        2. Count fresh oranges
        3. BFS level by level (each level = 1 minute)
        4. Track minutes and remaining fresh oranges

        Time: O(m*n) - visit each cell at most once
        Space: O(m*n) - queue can contain all cells in worst case
        """
        if not grid or not grid[0]:
            return 0

        from collections import deque

        m, n = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0

        # Initialize queue with all rotten oranges and count fresh ones
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 2:
                    queue.append((row, col, 0))  # (row, col, time)
                elif grid[row][col] == 1:
                    fresh_count += 1

        # If no fresh oranges, no time needed
        if fresh_count == 0:
            return 0

        # BFS from all rotten oranges
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        max_time = 0

        while queue:
            row, col, time = queue.popleft()
            max_time = max(max_time, time)

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                # Check bounds and if cell has fresh orange
                if 0 <= new_row < m and 0 <= new_col < n and grid[new_row][new_col] == 1:
                    # Rot the orange
                    grid[new_row][new_col] = 2
                    fresh_count -= 1
                    queue.append((new_row, new_col, time + 1))

        # Return time if all oranges rotted, -1 otherwise
        return max_time if fresh_count == 0 else -1

    def orangesRotting_bfs_level_order(self, grid: list[list[int]]) -> int:
        """
        Level-order BFS: Process all oranges at current level before moving to next.

        Time: O(m*n) - each cell processed once
        Space: O(m*n) - queue size
        """
        if not grid or not grid[0]:
            return 0

        from collections import deque

        m, n = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0

        # Initialize
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 2:
                    queue.append((row, col))
                elif grid[row][col] == 1:
                    fresh_count += 1

        if fresh_count == 0:
            return 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        minutes = 0

        while queue and fresh_count > 0:
            minutes += 1
            # Process current level (all currently rotten oranges)
            level_size = len(queue)

            for _ in range(level_size):
                row, col = queue.popleft()

                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc

                    if 0 <= new_row < m and 0 <= new_col < n and grid[new_row][new_col] == 1:
                        grid[new_row][new_col] = 2
                        fresh_count -= 1
                        queue.append((new_row, new_col))

        return minutes if fresh_count == 0 else -1

    def orangesRotting_simulation(self, grid: list[list[int]]) -> int:
        """
        Simulation approach: Simulate the rotting process minute by minute.

        Time: O(k*m*n) - where k is the number of minutes
        Space: O(1) - in-place modification
        """
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        minutes = 0

        while True:
            # Find all fresh oranges adjacent to rotten ones
            to_rot = []

            for row in range(m):
                for col in range(n):
                    if grid[row][col] == 1:  # Fresh orange
                        # Check if adjacent to rotten orange
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            new_row, new_col = row + dr, col + dc
                            if (
                                0 <= new_row < m
                                and 0 <= new_col < n
                                and grid[new_row][new_col] == 2
                            ):
                                to_rot.append((row, col))
                                break

            # If no oranges to rot, we're done
            if not to_rot:
                break

            # Rot all oranges that should rot this minute
            for row, col in to_rot:
                grid[row][col] = 2

            minutes += 1

        # Check if any fresh oranges remain
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 1:
                    return -1

        return minutes

    def orangesRotting(self, grid: list[list[int]]) -> int:
        """Main solution using multi-source BFS"""
        # Create copy to avoid modifying original
        grid_copy = [row[:] for row in grid]
        return self.orangesRotting_bfs_multi_source(grid_copy)


def create_demo_output() -> str:
    """Generate demonstration output for Rotting Oranges problem"""

    def grid_to_string(grid):
        return "\n".join(" ".join(str(cell) for cell in row) for row in grid)

    examples = [
        {
            "input": [[2, 1, 1], [1, 1, 0], [0, 1, 1]],
            "description": "Standard case - all oranges can rot",
        },
        {
            "input": [[2, 1, 1], [0, 1, 1], [1, 0, 1]],
            "description": "Blocked path - some oranges can't be reached",
        },
        {"input": [[0, 2]], "description": "Only rotten orange, no fresh oranges"},
        {"input": [[2, 2], [1, 1], [0, 0]], "description": "Multiple rotten sources"},
    ]

    output = ["=== Rotting Oranges (LeetCode 994) ===\n"]
    output.append("Find minimum minutes for all oranges to rot\n")

    solution = Solution()

    for i, example in enumerate(examples, 1):
        original_grid = [row[:] for row in example["input"]]

        output.append(f"Example {i}: {example['description']}")
        output.append("Original grid:")
        output.append(grid_to_string(original_grid))

        # Test multi-source BFS approach
        grid_bfs = [row[:] for row in original_grid]
        result_bfs = solution.orangesRotting_bfs_multi_source(grid_bfs)
        output.append(f"Multi-source BFS result: {result_bfs} minutes")
        output.append("Final grid:")
        output.append(grid_to_string(grid_bfs))

        # Test level-order BFS approach
        grid_level = [row[:] for row in original_grid]
        result_level = solution.orangesRotting_bfs_level_order(grid_level)
        output.append(f"Level-order BFS result: {result_level} minutes (should match)")

        # Test simulation approach
        grid_sim = [row[:] for row in original_grid]
        result_sim = solution.orangesRotting_simulation(grid_sim)
        output.append(f"Simulation result: {result_sim} minutes (should match)")
        output.append("")

    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. Multi-source BFS:")
    output.append("   - Time: O(m*n), Space: O(m*n)")
    output.append("   - Start from all rotten oranges simultaneously")
    output.append("   - Most efficient for this problem")

    output.append("2. Level-order BFS:")
    output.append("   - Time: O(m*n), Space: O(m*n)")
    output.append("   - Process level by level explicitly")
    output.append("   - Clear minute tracking")

    output.append("3. Simulation:")
    output.append("   - Time: O(k*m*n), Space: O(k)")
    output.append("   - Simulate minute by minute")
    output.append("   - Less efficient but intuitive")

    output.append("\nKey Insight: Multi-source BFS is perfect for this problem")
    output.append("Pattern: Spreading from multiple sources simultaneously")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_args=[[2, 1, 1], [1, 1, 0], [0, 1, 1]],
        expected=4,
        description="Standard case - all oranges rot in 4 minutes",
    ),
    TestCase(
        input_args=[[2, 1, 1], [0, 1, 1], [1, 0, 1]],
        expected=-1,
        description="Blocked path - bottom-left orange can't be reached",
    ),
    TestCase(
        input_args=[[0, 2]],
        expected=0,
        description="Only rotten orange, no fresh ones",
    ),
    TestCase(
        input_args=[[2, 2], [1, 1], [0, 0]],
        expected=1,
        description="Multiple rotten sources rot all in 1 minute",
    ),
    TestCase(
        input_args=[[1]],
        expected=-1,
        description="Only fresh orange, no rotten ones",
    ),
    TestCase(
        input_args=[[0]],
        expected=0,
        description="Only empty cell",
    ),
    TestCase(
        input_args=[
            [2, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [2, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
        ],
        expected=4,
        description="Complex grid with multiple sources",
    ),
]


def test_solution():
    """Test function for Rotting Oranges"""
    solution = Solution()

    def test_oranges_rotting(grid, expected, description):
        # Test main orangesRotting method
        result = solution.orangesRotting(grid)
        return result == expected

    test_cases_formatted = [
        TestCase(
            input_args=tc.input_data,
            expected=tc.expected,
            description=tc.description,
        )
        for tc in TEST_CASES
    ]

    return run_test_cases(test_oranges_rotting, test_cases_formatted)


# Register the problem
register_problem(
    slug="rotting_oranges",
    leetcode_num=994,
    title="Rotting Oranges",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=Solution().orangesRotting,
    test_func=test_solution,
    demo_func=create_demo_output,
)
