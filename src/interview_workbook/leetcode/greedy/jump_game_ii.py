"""
LeetCode 45: Jump Game II

You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
Each element nums[i] represents the maximum length of a forward jump from index i.

Return the minimum number of jumps to reach nums[n - 1].

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List
from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def jump(self, nums: List[int]) -> int:
        """
        Greedy approach: Track the farthest reachable position and current jump boundary.
        
        We maintain two pointers:
        - current_end: The farthest index we can reach with current number of jumps
        - farthest: The farthest index we can reach with one more jump
        
        When we reach current_end, we increment jumps and update current_end to farthest.
        
        Time: O(n) - Single pass through array
        Space: O(1) - Only using constant extra space
        """
        if len(nums) <= 1:
            return 0
        
        jumps = 0
        current_end = 0  # Boundary of current jump level
        farthest = 0     # Farthest reachable with one more jump
        
        # We don't need to consider the last index since we want to reach it
        for i in range(len(nums) - 1):
            # Update the farthest we can reach from current position
            farthest = max(farthest, i + nums[i])
            
            # If we've reached the end of current jump level
            if i == current_end:
                jumps += 1
                current_end = farthest
                
                # Early termination: if we can reach the end, no need to continue
                if current_end >= len(nums) - 1:
                    break
        
        return jumps
    
    def jumpBFS(self, nums: List[int]) -> int:
        """
        Alternative: BFS approach (less efficient but more intuitive).
        
        Treat each position as a node in a graph, and each possible jump as an edge.
        Use BFS to find the shortest path (minimum jumps) to the last index.
        
        Time: O(n²) - In worst case, we might visit all positions multiple times
        Space: O(n) - Queue can contain up to n positions
        """
        if len(nums) <= 1:
            return 0
        
        from collections import deque
        
        queue = deque([(0, 0)])  # (position, jumps)
        visited = set([0])
        
        while queue:
            pos, jumps = queue.popleft()
            
            # If we've reached the end
            if pos >= len(nums) - 1:
                return jumps
            
            # Try all possible jumps from current position
            for jump in range(1, nums[pos] + 1):
                next_pos = pos + jump
                if next_pos not in visited and next_pos < len(nums):
                    visited.add(next_pos)
                    queue.append((next_pos, jumps + 1))
        
        return -1  # Should never reach here if input is valid
    
    def jumpDP(self, nums: List[int]) -> int:
        """
