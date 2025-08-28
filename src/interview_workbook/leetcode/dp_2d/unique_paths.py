"""
LeetCode 62: Unique Paths

There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

Time Complexity: O(m * n)
Space Complexity: O(n)
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Space-optimized DP approach using 1D array.

        Key insight: To reach any cell (i,j), robot must come from either
        (i-1,j) or (i,j-1). So paths[i][j] = paths[i-1][j] + paths[i][j-1]

        Space optimization: Since we only need the previous row to compute
        the current row, we can use a 1D array and update in place.

        Time: O(m * n) - Fill m*n cells
        Space: O(n) - Only need one row at a time
        """
        # dp[j] represents number of paths to reach column j in current row
        dp = [1] * n  # First row: all cells reachable by moving right only

        # For each row starting from row 1
        for i in range(1, m):
            # For each column starting from column 1  
            for j in range(1, n):
                # Current cell = paths from above + paths from left
                dp[j] += dp[j - 1]

        return dp[n - 1]

    def uniquePathsDP2D(self, m: int, n: int) -> int:
        """
        Standard 2D DP approach for clearer understanding.

        dp[i][j] = number of unique paths to reach cell (i,j)
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

        Time: O(m * n) - Fill 2D table
        Space: O(m * n) - 2D DP array
        """
        # Initialize DP table
        dp = [[0] * n for _ in range(m)]

        # Base cases: first row and first column
        # Only one way to reach any cell in first row (move right only)
        for j in range(n):
            dp[0][j] = 1

        # Only one way to reach any cell in first column (move down only)
        for i in range(m):
            dp[i][0] = 1

        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    def uniquePathsMath(self, m: int, n: int) -> int:
        """
        Mathematical approach using combinatorics.

        To reach (m-1, n-1) from (0, 0), robot must make:
        - (m-1) down moves
        - (n-1) right moves
        Total moves: (m-1) + (n-1) = m + n - 2

        This is equivalent to choosing (m-1) positions out of (m+n-2) 
        total positions for down moves: C(m+n-2, m-1)

        Time: O(min(m, n)) - Computing combination
        Space: O(1) - No extra space needed
        """
        # Total moves needed
        total_moves = m + n - 2
        down_moves = m - 1

        # Compute C(total_moves, down_moves) efficiently
        # Use the identity: C(n,k) = C(n,n-k) to minimize computation
        k = min(down_moves, total_moves - down_moves)

        result = 1
        for i in range(k):
            result = result * (total_moves - i) // (i + 1)

        return result

    def uniquePathsRecursive(self, m: int, n: int) -> int:
        """
        Recursive approach with memoization.

        Base cases: reaching first row or first column (only 1 path)
        Recursive case: paths(i,j) = paths(i-1,j) + paths(i,j-1)

        Time: O(m * n) - Each cell computed once
        Space: O(m * n) - Memoization + recursion stack
        """
        memo = {}

        def count_paths(i, j):
            # Base cases
            if i == 0 or j == 0:
                return 1

            if (i, j) in memo:
                return memo[(i, j)]

            # Recursive case
            paths_from_above = count_paths(i - 1, j)
            paths_from_left = count_paths(i, j - 1)

            result = paths_from_above + paths_from_left
            memo[(i, j)] = result
            return result

        return count_paths(m - 1, n - 1)


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different grid path scenarios.
    """
    solution = Solution()

    demos = []

    # Test cases with detailed analysis
    test_cases = [
        (3, 7, 28),
        (3, 2, 3),
        (7, 3, 28),
        (3, 3, 6),
        (1, 1, 1),
        (1, 10, 1),
        (10, 1, 1),
        (4, 4, 20),
    ]

    for m, n, expected in test_cases:
        result_dp = solution.uniquePaths(m, n)
        result_math = solution.uniquePathsMath(m, n)

        demos.append(f"Grid: {m} x {n}")
        demos.append(f"Unique paths (DP): {result_dp}")
        demos.append(f"Unique paths (Math): {result_math}")

        # Show small grids visually
        if m <= 4 and n <= 4:
            demos.append("DP table construction:")
            dp = [[0] * n for _ in range(m)]

            # Fill first row and column
            for j in range(n):
                dp[0][j] = 1
            for i in range(m):
                dp[i][0] = 1

            # Fill the rest
            for i in range(1, m):
                for j in range(1, n):
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

            # Display the grid
            for i in range(m):
                row_str = "  " + " ".join(f"{dp[i][j]:3d}" for j in range(n))
                demos.append(row_str)

            # Show combinatorial calculation
            total_moves = m + n - 2
            down_moves = m - 1
            demos.append(f"Mathematical: C({total_moves}, {down_moves}) = {result_math}")

        demos.append("")

    # Algorithm comparison and analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Problem Structure:")
    demos.append("- Robot starts at (0,0), wants to reach (m-1,n-1)")
    demos.append("- Can only move right or down")
    demos.append("- Count all possible unique paths")
    demos.append("")

    demos.append("DP Recurrence:")
    demos.append("- paths(i,j) = paths(i-1,j) + paths(i,j-1)")
    demos.append("- Base cases: paths(0,j) = 1, paths(i,0) = 1")
    demos.append("- Bottom-up: fill table row by row")
    demos.append("- Top-down: recursive with memoization")
    demos.append("")

    demos.append("Space Optimization:")
    demos.append("- 2D DP: O(m*n) space")
    demos.append("- 1D DP: O(n) space - only need previous row")
    demos.append("- Math: O(1) space - direct formula")
    demos.append("- Key insight: current row only depends on previous row")
    demos.append("")

    # Show step-by-step 1D optimization
    demos.append("=== Space Optimization Example (3x3 grid) ===")
    demos.append("2D approach would use 3x3 = 9 cells")
    demos.append("1D approach uses only 3 cells:")
    demos.append("")

    m_demo, n_demo = 3, 3
    dp_demo = [1] * n_demo
    demos.append(f"Initial (row 0): {dp_demo}")

    for i in range(1, m_demo):
        for j in range(1, n_demo):
            dp_demo[j] += dp_demo[j - 1]
        demos.append(f"After row {i}:   {dp_demo}")

    demos.append("")

    # Combinatorial explanation
    demos.append("=== Combinatorial Insight ===")
    demos.append("Robot movement can be viewed as a sequence of moves:")
    demos.append("- Must make exactly (m-1) DOWN moves")
    demos.append("- Must make exactly (n-1) RIGHT moves")
    demos.append("- Total sequence length: (m-1) + (n-1) = m+n-2")
    demos.append("")

    demos.append("Example: 3x3 grid")
    demos.append("- Need 2 DOWN, 2 RIGHT moves")
    demos.append("- Total 4 moves: choose 2 positions for DOWN")
    demos.append("- C(4,2) = 6 ways")
    demos.append("- Sequences: DDRR, DRDR, DRRD, RDDR, RDRD, RRDD")
    demos.append("")

    # Performance comparison
    import time

    large_m, large_n = 50, 50

    # Time 1D DP approach
    start_time = time.time()
    for _ in range(1000):
        solution.uniquePaths(large_m, large_n)
    dp1d_time = time.time() - start_time

    # Time 2D DP approach  
    start_time = time.time()
    for _ in range(100):
        solution.uniquePathsDP2D(large_m, large_n)
    dp2d_time = time.time() - start_time

    # Time mathematical approach
    start_time = time.time()
    for _ in range(10000):
        solution.uniquePathsMath(large_m, large_n)
    math_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"1D DP (1000 runs, 50x50): {dp1d_time:.6f}s")
    demos.append(f"2D DP (100 runs, 50x50): {dp2d_time:.6f}s")
    demos.append(f"Mathematical (10k runs, 50x50): {math_time:.6f}s")
    demos.append("")
    demos.append("Time Complexity:")
    demos.append("- 1D DP: O(m*n)")
    demos.append("- 2D DP: O(m*n)")
    demos.append("- Mathematical: O(min(m,n))")
    demos.append("- Recursive: O(m*n) with memoization")
    demos.append("")

    # Edge cases and patterns
    demos.append("=== Edge Cases & Patterns ===")
    edge_cases = [
        (1, 1, "Single cell - robot already at destination"),
        (1, 10, "Single row - only move right"),
        (10, 1, "Single column - only move down"),
        (2, 2, "Minimum non-trivial case"),
    ]

    for m_edge, n_edge, description in edge_cases:
        result = solution.uniquePaths(m_edge, n_edge)
        demos.append(f"{m_edge}x{n_edge} grid: {result} paths - {description}")

    demos.append("")

    # Problem variations and extensions
    demos.append("=== Problem Variations ===")
    demos.append("- Unique Paths II: grid with obstacles")
    demos.append("- Minimum Path Sum: find path with minimum cost")
    demos.append("- Maximum Path Sum: find path with maximum reward")
    demos.append("- Count paths with specific constraints")
    demos.append("- 3D grid navigation problems")
    demos.append("- Paths with different movement rules (diagonal, etc.)")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Robot navigation and path planning")
    demos.append("- Game development: character movement options")
    demos.append("- Network routing: count possible routes")
    demos.append("- Dynamic programming pattern recognition")
    demos.append("- Combinatorial counting problems")
    demos.append("- Grid-based puzzle solving")
    demos.append("- Resource allocation in 2D constraints")
    demos.append("- Image processing: pixel traversal patterns")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(input=[3, 7], expected=28, description="Standard rectangular grid"),
    TestCase(input=[3, 2], expected=3, description="Small grid example"),
    TestCase(input=[7, 3], expected=28, description="Symmetric to 3x7 case"),
    TestCase(input=[3, 3], expected=6, description="Square grid"),
    TestCase(input=[1, 1], expected=1, description="Single cell - already at destination"),
    TestCase(input=[1, 10], expected=1, description="Single row - only move right"),
    TestCase(input=[10, 1], expected=1, description="Single column - only move down"),
    TestCase(input=[2, 2], expected=2, description="Minimum non-trivial case"),
    TestCase(input=[4, 4], expected=20, description="4x4 square grid"),
    TestCase(input=[23, 12], expected=193536720, description="Larger grid for performance test"),
]


def test_solution():
    """Test the unique paths solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.uniquePaths, TEST_CASES)


# Register the problem
register_problem(
    slug="unique_paths",
    leetcode_num=62,
    title="Unique Paths",
    difficulty=Difficulty.MEDIUM,
    category=Category.DP_2D,
    solution_func=Solution().uniquePaths,
    test_func=test_solution,
    demo_func=create_demo_output,
)
