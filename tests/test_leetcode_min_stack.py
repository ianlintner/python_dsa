"""
Tests for Min Stack
"""


from src.interview_workbook.leetcode.stack.min_stack import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        ops = ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"]
        vals = [[], [-2], [0], [-3], [], [], [], []]
        expected = [None, None, None, None, -3, None, 0, -2]
        assert solution.solve(ops, vals) == expected

    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        ops = ["MinStack", "push", "getMin", "push", "getMin", "pop", "getMin"]
        vals = [[], [1], [], [2], [], [], []]
        expected = [None, None, 1, None, 1, None, 1]
        assert solution.solve(ops, vals) == expected

    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        ops = ["MinStack"]
        vals = [[]]
        expected = [None]
        for i in range(1000):
            ops.append("push")
            vals.append([i])
            expected.append(None)
        for i in range(1000):
            ops.append("getMin")
            expected.append(0)
            ops.append("top")
            expected.append(999 - i)
            ops.append("pop")
            expected.append(None)
        assert solution.solve(ops, vals) == expected
