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
        assert solution.solve() == 10
        assert solution.solve() == 4

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve([]) == 0
        assert solution.solve() == 1
        assert solution.solve() == 25
        assert solution.solve() == 9

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        heights = list(range(1, 1001))
        assert solution.solve(heights) == 250500
