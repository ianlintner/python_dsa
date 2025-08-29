from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty

"""
Evaluate Reverse Polish Notation

Evaluate arithmetic expressions in Reverse Polish Notation using a stack.
"""


class Solution:
    def solve(self, tokens: list[str]) -> int:
        """Evaluate Reverse Polish Notation using a stack."""
        stack = []
        for token in tokens:
            if token in {"+", "-", "*", "/"}:
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    # Truncate toward zero division
                    stack.append(int(a / b))
            else:
                stack.append(int(token))
        return stack[0]


def demo():
    """Run a deterministic demo using a sample test case."""
    tokens = ["2", "1", "+", "3", "*"]  # (2 + 1) * 3 = 9
    result = Solution().solve(tokens)
    return str(result)


register_problem(
    id=150,
    slug="evaluate_reverse_polish_notation",
    title="Evaluate Reverse Polish Notation",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "expression evaluation"],
    url="https://leetcode.com/problems/evaluate-reverse-polish-notation/",
    notes="Use a stack to evaluate operators and operands in reverse Polish form.",
)
