"""
Tests for Search in Rotated Sorted Array
"""


from src.interview_workbook.leetcode.binary_search.search_in_rotated_sorted_array import (
    Solution,
)


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.search(, 0) == 4
        assert solution.search(, 3) == -1
        assert solution.search(, 0) == -1

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.search(, 1) == 0
        assert solution.search(, 3) == 1
        assert solution.search(, 1) == 1
        assert solution.search(, 5) == 0

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        nums = list(range(1000, 5001)) + list(range(0, 1000))
        assert solution.search(nums, 2000) == 1000
        assert solution.search(nums, 500) == 4501
