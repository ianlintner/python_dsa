"""
Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
"""


class Solution:
    def solve(self, s: str) -> bool:
        """Check if the parentheses string is valid."""
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in mapping.values():
                stack.append(char)
            elif char in mapping:
                if not stack or stack[-1] != mapping[char]:
                    return False
                stack.pop()
            else:
                # Invalid character
                return False
        return not stack


def demo():
    """Run demo for Valid Parentheses problem."""
    import random
    random.seed(0)

    cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
    sol = Solution()
    outputs = [sol.solve(c) for c in cases]
    return str(outputs)


from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty

register_problem(
    id=20,
    slug="valid_parentheses",
    title="Valid Parentheses",
    category=Category.STACK,
    difficulty=Difficulty.EASY,
    tags=["stack", "string"],
    url="https://leetcode.com/problems/valid-parentheses/",
    notes="Classic stack-based validation problem."
)
