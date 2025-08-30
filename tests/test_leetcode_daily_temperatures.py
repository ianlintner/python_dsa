"""
Tests for Daily Temperatures
"""

from src.interview_workbook.leetcode.stack.daily_temperatures import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.solve() == [
            1,
            1,
            4,
            2,
            1,
            1,
            0,
            0,
        ]
        assert solution.solve([30, 40, 50, 60]) == [1, 1, 1, 0]
        assert solution.solve([30, 60, 90]) == [1, 1, 0]

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve([]) == []
        assert solution.solve([90, 80, 70, 60, 50]) == [0, 0, 0, 0, 0]
        assert solution.solve([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        temps = list(range(30, 101)) * 1000
        result = solution.solve(temps)
        assert len(result) == len(temps)
