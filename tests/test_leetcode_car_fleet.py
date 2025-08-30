"""
Tests for Car Fleet
"""


from src.interview_workbook.leetcode.stack.car_fleet import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.solve(12,,) == 3
        assert solution.solve(10,,) == 1
        assert solution.solve(100,,) == 1

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve(10, [], []) == 0
        assert solution.solve(20,,) == 3
        assert solution.solve(10,,) == 1

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        target = 10**6
        positions = list(range(0, 10**5))
        speeds = * 10**5
        assert solution.solve(target, positions, speeds) == 10**5
