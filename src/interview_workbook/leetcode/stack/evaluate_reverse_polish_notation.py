from src.interview_workbook.leetcode._registry import Category, Difficulty, register_problem

"""
Evaluate Reverse Polish Notation

Evaluate arithmetic expressions in Reverse Polish Notation using a stack.
"""


class Solution:
    def solve(self, *args) -> None:
        """TODO: Implement solution."""
        pass


def demo():
    """TODO: Implement demo function."""
    pass


# Register the problem with correct parameters
register_problem(
    pid=150,
    title="Evaluate Reverse Polish Notation",
    difficulty=Difficulty.MEDIUM,
    categories=[Category.STACK],
    function_signature="def evalRPN(tokens: list[str]) -> int:",
)
