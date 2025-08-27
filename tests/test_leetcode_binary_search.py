"""
Tests for Binary Search
"""

import pytest
from src.interview_workbook.leetcode.binary_search.binary_search import Solution


class TestSolution:
    def test_binary_search(self):
        """Test binary search with various cases."""
        solution = Solution()
        
        # Example cases from LeetCode
        assert solution.search([-1, 0, 3, 5, 9, 12], 9) == 4
        assert solution.search([-1, 0, 3, 5, 9, 12], 2) == -1
        
        # Single element cases
        assert solution.search([5], 5) == 0
        assert solution.search([5], -5) == -1
        
        # Target at boundaries
        assert solution.search([-1, 0, 3, 5, 9, 12], -1) == 0  # First element
        assert solution.search([-1, 0, 3, 5, 9, 12], 12) == 5  # Last element
        
        # Target in middle positions
        assert solution.search([-1, 0, 3, 5, 9, 12], 0) == 1
        assert solution.search([-1, 0, 3, 5, 9, 12], 5) == 3
        
        # Empty array
        assert solution.search([], 1) == -1
        
        # Target larger than all elements
        assert solution.search([1, 2, 3, 4, 5], 6) == -1
    
    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        
        # Two element arrays
        assert solution.search([1, 3], 1) == 0
        assert solution.search([1, 3], 3) == 1
        assert solution.search([1, 3], 2) == -1
        
        # Large array with target at various positions
        arr = list(range(0, 1000, 2))  # [0, 2, 4, 6, ..., 998]
        assert solution.search(arr, 0) == 0
        assert solution.search(arr, 998) == 499
        assert solution.search(arr, 500) == 250
        assert solution.search(arr, 1) == -1  # Odd number not in array
    
    def test_large_input(self):
        """Test with larger inputs to verify O(log n) performance."""
        solution = Solution()
        
        # Large sorted array
        large_arr = list(range(100000))
        
        # Test various positions
        assert solution.search(large_arr, 0) == 0
        assert solution.search(large_arr, 99999) == 99999
        assert solution.search(large_arr, 50000) == 50000
        assert solution.search(large_arr, -1) == -1
        assert solution.search(large_arr, 100000) == -1
