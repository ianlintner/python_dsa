"""
LeetCode 150: Evaluate Reverse Polish Notation

Evaluate the value of an arithmetic expression in Reverse Polish Notation.

Valid operators are +, -, *, and /. Each operand may be an integer or another expression.

Note that division between two integers should truncate toward zero.

It is guaranteed that the given RPN expression is always valid. That means the expression
would always evaluate to a result, and there will not be any division by zero operation.

URL: https://leetcode.com/problems/evaluate-reverse-polish-notation/
Difficulty: Medium
Category: Stack

Patterns:
- Stack-based expression evaluation
- Postfix notation processing

Complexity:
- Time: O(n) where n is the number of tokens
- Space: O(n) for the stack in worst case

Pitfalls:
- Division should truncate towards zero, not floor division
- Need to handle negative operands correctly
- Order of operands matters for subtraction and division

Follow-ups:
- How would you handle more operators like ^, %, etc.?
- How would you convert infix notation to postfix notation?
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        """
        Evaluate Reverse Polish Notation expression.

        Args:
            tokens: List of strings representing RPN expression

        Returns:
            Integer result of the expression
        """
        stack = []
        operators = {"+", "-", "*", "/"}

        for token in tokens:
            if token in operators:
                # Pop two operands (note: order matters for - and /)
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                elif token == "/":
                    # Division should truncate towards zero
                    result = int(left / right)

                stack.append(result)
            else:
                # It's a number (could be negative)
                stack.append(int(token))

        # The final result should be the only element left
        return stack[0]


# Test cases
test_cases = [
    TestCase((["2", "1", "+", "3", "*"],), 9, "Basic arithmetic: ((2 + 1) * 3) = 9"),
    TestCase((["4", "13", "5", "/", "+"],), 6, "Division and addition: (4 + (13 / 5)) = 6"),
    TestCase(
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],),
        22,
        "Complex expression with negative numbers",
    ),
    TestCase((["3", "11", "+", "5", "-"],), 9, "Addition then subtraction: ((3 + 11) - 5) = 9"),
    TestCase((["3", "11", "5", "+", "-"],), -13, "Subtraction with addition: (3 - (11 + 5)) = -13"),
    TestCase((["18"],), 18, "Single number"),
    TestCase((["4", "3", "-"],), 1, "Simple subtraction: (4 - 3) = 1"),
    TestCase((["4", "3", "/"],), 1, "Division truncating towards zero: (4 / 3) = 1"),
    TestCase((["-3", "4", "/"],), 0, "Negative division truncating towards zero: (-3 / 4) = 0"),
    TestCase((["3", "-4", "/"],), 0, "Division with negative divisor: (3 / -4) = 0"),
    TestCase((["-78", "-33", "+"],), -111, "Addition of negative numbers: (-78 + -33) = -111"),
    TestCase(
        (["1", "2", "+", "3", "*", "4", "-"],), 5, "Multiple operations: (((1 + 2) * 3) - 4) = 5"
    ),
]


def demo() -> str:
    """Run Evaluate Reverse Polish Notation demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.evalRPN, test_cases, "LeetCode 150: Evaluate Reverse Polish Notation"
    )

    return create_demo_output(
        "Evaluate Reverse Polish Notation",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use a stack to store operands as we process the expression left to right
2. When encountering a number, push it onto the stack
3. When encountering an operator, pop two operands, compute result, and push back
4. The final result is the single element remaining on the stack
5. For division, use int(a/b) to truncate towards zero instead of a//b (floor division)
        """.strip(),
    )


# Register the problem
register_problem(
    id=150,
    slug="evaluate_reverse_polish_notation",
    title="Evaluate Reverse Polish Notation",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "stack", "math"],
    url="https://leetcode.com/problems/evaluate-reverse-polish-notation/",
    notes="Classic postfix expression evaluation using stack with proper division handling",
)
