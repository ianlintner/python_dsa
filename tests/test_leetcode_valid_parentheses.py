"""
Tests for Valid Parentheses
"""


from src.interview_workbook.leetcode.stack.valid_parentheses import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        assert solution.solve("()") is True
        assert solution.solve("()[]{}") is True
        assert solution.solve("(]") is False
        assert solution.solve("([)]") is False
        assert solution.solve("{[]}") is True

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        assert solution.solve("") is True
        assert solution.solve("(") is False
        assert solution.solve(")") is False
        assert solution.solve("[") is False
        assert solution.solve("]") is False
        assert solution.solve("{") is False
        assert solution.solve("}") is False

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        s = "()" * 5000
        assert solution.solve(s) is True
        s = "{" * 5000 + "}" * 5000
        assert solution.solve(s) is True
        s = "{" * 5000 + "}" * 4999
        assert solution.solve(s) is False
