"""
Tests for Generate Parentheses
"""


from src.interview_workbook.leetcode.stack.generate_parentheses import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert set(solution.solve(3)) == {"((()))", "(()())", "(())()", "()(())", "()()()"}
        assert set(solution.solve(1)) == {"()"}

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert set(solution.solve(0)) == {""}
        assert len(solution.solve(8)) == 1430

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        # Performance test for n=8, which is the constraint limit
        result = solution.solve(8)
        assert isinstance(result, list)
        assert len(result) > 0
