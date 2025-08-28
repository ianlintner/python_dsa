"""
1-D Dynamic Programming Category - LeetCode Problems

One-dimensional dynamic programming problems where the state space can be
represented as a single array. These problems typically involve making
optimal decisions based on previous states in a linear sequence.

Key Concepts:
- State definition: dp[i] represents optimal solution for subproblem ending at i
- Base cases: Initialize dp[0] or first few elements
- Recurrence relations: dp[i] = f(dp[i-1], dp[i-2], ...)
- Space optimization: Often can reduce O(n) space to O(1)

Common Patterns:
- Fibonacci-style: dp[i] depends on dp[i-1] and dp[i-2]
- Decision problems: Choose to include/exclude current element
- Counting problems: Sum ways to reach current state
- Optimization problems: Min/max over previous decisions

This category covers:
- Climbing stairs with step variations
- House robber problems with adjacency constraints
- Coin change and subset sum problems
- Longest increasing subsequence variations
- Knapsack and partition problems
"""
