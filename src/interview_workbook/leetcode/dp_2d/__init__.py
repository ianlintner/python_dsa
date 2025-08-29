"""
2-D Dynamic Programming Category - LeetCode Problems

Two-dimensional dynamic programming problems where the state space requires
a 2D array or matrix representation. These problems typically involve making
decisions across two dimensions or parameters.

Key Concepts:
    - State definition: dp[i][j] represents optimal solution for 2D subproblem
- Base cases=Initialize first row, column, or diagonal elements
- Recurrence relations=dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1], ...)
- Space optimization=Can often reduce to O(min(m,n)) space using rolling arrays

Common Patterns:
    - Grid traversal: Moving from top-left to bottom-right
- String matching: Comparing two sequences character by character
- Decision trees: Include/exclude choices for two different sequences
- Path counting: Number of ways to reach destination in 2D grid

This category covers:
    - Unique paths in grids with obstacles
- Longest common subsequence and edit distance
- String matching and word break problems
- 2D grid optimization problems
- Matrix-based dynamic programming
"""
