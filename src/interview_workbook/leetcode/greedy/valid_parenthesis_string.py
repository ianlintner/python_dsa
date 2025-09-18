"""
Valid Parenthesis String

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, s: str) -> bool:
        """Check if the string is a valid parenthesis string with '*' wildcard."""
        lo = hi = 0
        for c in s:
            if c == '(':
                lo += 1
                hi += 1
            elif c == ')':
                lo = max(lo - 1, 0)
                hi -= 1
            else:  # '*'
                lo = max(lo - 1, 0)
                hi += 1
            if hi < 0:
                return False
        return lo == 0


def demo() -> str:
    """Run a demo for the Valid Parenthesis String problem."""
    s = "(*)"
    print(f"Input string: {s}")
    solver = Solution()
    result = solver.solve(s)
    print(f"Final result: {result}")
    return f"Valid Parenthesis String result for '{s}' -> {result}"


if __name__ == "__main__":
    demo()
    

register_problem(
    id=678,
    slug="valid_parenthesis_string",
    title="Valid Parenthesis String",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "greedy", "stack"],
    url="https://leetcode.com/problems/valid-parenthesis-string/",
    notes="",
)
