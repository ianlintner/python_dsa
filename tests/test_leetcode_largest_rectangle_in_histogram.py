"""
Tests for Largest Rectangle in Histogram
"""

from src.interview_workbook.leetcode.stack.largest_rectangle_in_histogram import (
    Solution,
)


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.solve([2, 1, 5, 6, 2, 3]) == 10
        assert solution.solve([2, 4]) == 4

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve([]) == 0
        assert solution.solve([1]) == 1
        assert solution.solve([5, 5, 5, 5, 5]) == 25
        assert solution.solve([6, 7, 5, 2, 4, 5, 9, 3]) == 16

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        heights = list(range(1, 1001))
        assert solution.solve(heights) == 250500
