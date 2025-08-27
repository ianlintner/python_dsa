"""
Tests for Binary Search Problems
"""

import pytest
from src.interview_workbook.leetcode.binary_search.binary_search import Solution as BinarySearchSolution
from src.interview_workbook.leetcode.binary_search.search_in_rotated_sorted_array import Solution as SearchRotatedSolution
from src.interview_workbook.leetcode.binary_search.find_min_in_rotated_sorted_array import Solution as FindMinSolution


class TestBinarySearch:
    def test_binary_search(self):
        """Test binary search with various cases."""
        solution = BinarySearchSolution()
        
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
    
    def test_binary_search_edge_cases(self):
        """Test edge cases for binary search."""
        solution = BinarySearchSolution()
        
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
    
    def test_binary_search_large_input(self):
        """Test with larger inputs to verify O(log n) performance."""
        solution = BinarySearchSolution()
        
        # Large sorted array
        large_arr = list(range(100000))
        
        # Test various positions
        assert solution.search(large_arr, 0) == 0
        assert solution.search(large_arr, 99999) == 99999
        assert solution.search(large_arr, 50000) == 50000
        assert solution.search(large_arr, -1) == -1
        assert solution.search(large_arr, 100000) == -1


class TestSearchInRotatedSortedArray:
    def test_search_rotated_examples(self):
        """Test LeetCode examples for search in rotated sorted array."""
        solution = SearchRotatedSolution()
        
        # Example 1
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
        
        # Example 2
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
        
        # Example 3
        assert solution.search([1], 0) == -1
    
    def test_search_rotated_comprehensive(self):
        """Test comprehensive cases for search in rotated sorted array."""
        solution = SearchRotatedSolution()
        
        # No rotation (sorted array)
        assert solution.search([1, 2, 3, 4, 5], 3) == 2
        assert solution.search([1, 2, 3, 4, 5], 6) == -1
        
        # Single rotation
        assert solution.search([2, 3, 4, 5, 1], 1) == 4
        assert solution.search([2, 3, 4, 5, 1], 3) == 1
        
        # Multiple rotations
        assert solution.search([6, 7, 1, 2, 3, 4, 5], 2) == 3
        assert solution.search([6, 7, 1, 2, 3, 4, 5], 7) == 1
        
        # Target at rotation point
        assert solution.search([3, 1], 1) == 1
        assert solution.search([3, 1], 3) == 0
        
        # Two element arrays
        assert solution.search([1, 3], 3) == 1
        assert solution.search([3, 1], 1) == 1
        
        # Single element
        assert solution.search([1], 1) == 0
        assert solution.search([1], 2) == -1
    
    def test_search_rotated_edge_cases(self):
        """Test edge cases for search in rotated sorted array."""
        solution = SearchRotatedSolution()
        
        # Duplicate elements at boundaries (but all unique as per constraints)
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 4) == 0  # First element
        assert solution.search([4, 5, 6, 7, 0, 1, 2], 2) == 6  # Last element
        
        # Large rotation
        assert solution.search([5, 6, 7, 8, 9, 1, 2, 3, 4], 1) == 5
        assert solution.search([5, 6, 7, 8, 9, 1, 2, 3, 4], 9) == 4
        
        # Negative numbers
        assert solution.search([0, 1, 2, -5, -4, -3, -2, -1], -3) == 5
        assert solution.search([0, 1, 2, -5, -4, -3, -2, -1], 1) == 1


class TestFindMinInRotatedSortedArray:
    def test_find_min_examples(self):
        """Test LeetCode examples for find minimum in rotated sorted array."""
        solution = FindMinSolution()
        
        # Example 1
        assert solution.findMin([3, 4, 5, 1, 2]) == 1
        
        # Example 2
        assert solution.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
        
        # Example 3: No rotation
        assert solution.findMin([11, 13, 15, 17]) == 11
    
    def test_find_min_comprehensive(self):
        """Test comprehensive cases for find minimum in rotated sorted array."""
        solution = FindMinSolution()
        
        # Single element
        assert solution.findMin([1]) == 1
        
        # Two elements - rotated
        assert solution.findMin([2, 1]) == 1
        
        # Two elements - not rotated
        assert solution.findMin([1, 2]) == 1
        
        # Large rotation with negative numbers
        assert solution.findMin([5, 1, 2, 3, 4]) == 1
        
        # Mixed positive and negative
        assert solution.findMin([-1, 0, 1, 2, -3, -2]) == -3
        
        # All negative numbers
        assert solution.findMin([-3, -2, -1, -5, -4]) == -5
        
        # No rotation (already sorted)
        assert solution.findMin([1, 2, 3, 4, 5]) == 1
        assert solution.findMin([-5, -4, -3, -2, -1]) == -5
    
    def test_find_min_edge_cases(self):
        """Test edge cases for find minimum in rotated sorted array."""
        solution = FindMinSolution()
        
        # Minimum at first position (no rotation)
        assert solution.findMin([0, 1, 2, 3, 4]) == 0
        
        # Minimum at last position
        assert solution.findMin([1, 2, 3, 4, 0]) == 0
        
        # Minimum in middle
        assert solution.findMin([4, 5, 0, 1, 2, 3]) == 0
        
        # Large array with small rotation
        arr = list(range(1, 1000)) + [0]  # [1,2,3,...,999,0]
        assert solution.findMin(arr) == 0
        
        # Large array no rotation
        arr = list(range(1000))  # [0,1,2,...,999]
        assert solution.findMin(arr) == 0
    
    def test_find_min_rotations(self):
        """Test various rotation amounts."""
        solution = FindMinSolution()
        original = [1, 2, 3, 4, 5, 6, 7]
        
        # Test different rotation amounts
        rotations = [
            ([1, 2, 3, 4, 5, 6, 7], 1),  # No rotation
            ([7, 1, 2, 3, 4, 5, 6], 1),  # Rotate by 1
            ([6, 7, 1, 2, 3, 4, 5], 1),  # Rotate by 2
            ([5, 6, 7, 1, 2, 3, 4], 1),  # Rotate by 3
            ([4, 5, 6, 7, 1, 2, 3], 1),  # Rotate by 4
            ([3, 4, 5, 6, 7, 1, 2], 1),  # Rotate by 5
            ([2, 3, 4, 5, 6, 7, 1], 1),  # Rotate by 6
        ]
        
        for rotated_array, expected_min in rotations:
            assert solution.findMin(rotated_array) == expected_min
