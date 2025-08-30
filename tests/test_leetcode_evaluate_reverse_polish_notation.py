"""
Tests for Evaluate Reverse Polish Notation
"""


from src.interview_workbook.leetcode.stack.evaluate_reverse_polish_notation import (
    Solution,
)


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.solve(["2", "1", "+", "3", "*"]) == 9
        assert solution.solve(["4", "13", "5", "/", "+"]) == 6
        assert (
            solution.solve(
                ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
            )
            == 22
        )

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve(["3"]) == 3
        assert solution.solve(["-1"]) == -1
        assert solution.solve(["5", "2", "-"]) == 3
        assert solution.solve(["5", "2", "/"]) == 2
        assert solution.solve(["2", "5", "/"]) == 0

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        tokens = [str(i) for i in range(1000)] + ["+"] * 999
        assert solution.solve(tokens) == sum(range(1000))
