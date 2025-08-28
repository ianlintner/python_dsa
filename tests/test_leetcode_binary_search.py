"""
Tests for Binary Search Problems
"""

from src.interview_workbook.leetcode.binary_search.binary_search import (
    Solution as BinarySearchSolution,
)
from src.interview_workbook.leetcode.binary_search.find_kth_smallest_in_sorted_matrix import (
    Solution as FindKthSmallestSolution,
)
from src.interview_workbook.leetcode.binary_search.find_min_in_rotated_sorted_array import (
    Solution as FindMinSolution,
)
from src.interview_workbook.leetcode.binary_search.find_peak_element import (
    Solution as FindPeakSolution,
)
from src.interview_workbook.leetcode.binary_search.koko_eating_bananas import (
    Solution as KokoSolution,
)
from src.interview_workbook.leetcode.binary_search.search_2d_matrix import (
    Solution as Search2DMatrixSolution,
)
from src.interview_workbook.leetcode.binary_search.search_in_rotated_sorted_array import (
    Solution as SearchRotatedSolution,
)


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


class TestSearch2DMatrix:
    def test_search_2d_matrix_examples(self):
        """Test LeetCode examples for search 2D matrix."""
        solution = Search2DMatrixSolution()

        # Example 1
        matrix1 = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]]
        assert solution.searchMatrix(matrix1, 5) == True

        # Example 2
        assert solution.searchMatrix(matrix1, 13) == False

    def test_search_2d_matrix_comprehensive(self):
        """Test comprehensive cases for search 2D matrix."""
        solution = Search2DMatrixSolution()

        # Single element matrix
        assert solution.searchMatrix([[1]], 1) == True
        assert solution.searchMatrix([[1]], 2) == False

        # Single row
        assert solution.searchMatrix([[1, 3, 5, 7]], 3) == True
        assert solution.searchMatrix([[1, 3, 5, 7]], 6) == False

        # Single column
        assert solution.searchMatrix([[1], [3], [5]], 3) == True
        assert solution.searchMatrix([[1], [3], [5]], 2) == False

        # Empty matrix
        assert solution.searchMatrix([], 1) == False
        assert solution.searchMatrix([[]], 1) == False


class TestFindKthSmallestInSortedMatrix:
    def test_kth_smallest_examples(self):
        """Test LeetCode examples for kth smallest in sorted matrix."""
        solution = FindKthSmallestSolution()

        # Example 1
        matrix1 = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
        assert solution.kthSmallest(matrix1, 8) == 13

        # Example 2
        assert solution.kthSmallest([[-5]], 1) == -5

    def test_kth_smallest_comprehensive(self):
        """Test comprehensive cases for kth smallest in sorted matrix."""
        solution = FindKthSmallestSolution()

        # Small matrices
        matrix2 = [[1, 2], [1, 3]]
        assert solution.kthSmallest(matrix2, 3) == 2

        # Test both solutions match
        matrix3 = [[1, 3, 5], [6, 7, 12], [11, 14, 14]]
        result_binary = solution.kthSmallest(matrix3, 6)
        result_heap = solution.kthSmallestHeap(matrix3, 6)
        assert result_binary == result_heap == 11


class TestKokoEatingBananas:
    def test_koko_examples(self):
        """Test LeetCode examples for Koko eating bananas."""
        solution = KokoSolution()

        # Example 1
        assert solution.minEatingSpeed([3, 6, 7, 11], 8) == 4

        # Example 2
        assert solution.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30

        # Example 3
        assert solution.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23

    def test_koko_comprehensive(self):
        """Test comprehensive cases for Koko eating bananas."""
        solution = KokoSolution()

        # Single pile
        assert solution.minEatingSpeed([1000000], 2) == 500000

        # All same pile sizes
        assert solution.minEatingSpeed([1, 1, 1, 1], 4) == 1

        # Test both solutions match
        result_standard = solution.minEatingSpeed([3, 6, 7, 11], 8)
        result_optimized = solution.minEatingSpeedOptimized([3, 6, 7, 11], 8)
        assert result_standard == result_optimized == 4


class TestFindPeakElement:
    def test_find_peak_examples(self):
        """Test LeetCode examples for find peak element."""
        solution = FindPeakSolution()

        # Example 1
        result1 = solution.findPeakElement([1, 2, 3, 1])
        assert result1 == 2  # Peak at index 2

        # Example 2 - multiple valid peaks
        result2 = solution.findPeakElement([1, 2, 1, 3, 5, 6, 4])
        assert result2 in [1, 5]  # Peaks at indices 1 or 5

    def test_find_peak_comprehensive(self):
        """Test comprehensive cases for find peak element."""
        solution = FindPeakSolution()

        # Single element
        assert solution.findPeakElement([1]) == 0

        # Two elements - ascending
        assert solution.findPeakElement([1, 2]) == 1

        # Two elements - descending
        assert solution.findPeakElement([2, 1]) == 0

        # Test all solutions give valid peaks
        nums = [1, 3, 2, 1]
        result_binary = solution.findPeakElement(nums)
        result_linear = solution.findPeakElementLinear(nums)
        result_recursive = solution.findPeakElementRecursive(nums)

        # All should be valid peak indices
        def is_peak(arr, idx):
            n = len(arr)
            left_ok = idx == 0 or arr[idx] > arr[idx - 1]
            right_ok = idx == n - 1 or arr[idx] > arr[idx + 1]
            return left_ok and right_ok

        assert is_peak(nums, result_binary)
        assert is_peak(nums, result_linear)
        assert is_peak(nums, result_recursive)
