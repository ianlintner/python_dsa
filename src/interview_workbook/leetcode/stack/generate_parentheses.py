"""
Generate Parentheses

Given `n` pairs of parentheses, write a function to generate all
combinations of well-formed parentheses.

Example:
    Input: n = 3
    Output: ["((()))","(()())","(())()","()(())","()()()"]

Constraints:
    - 1 <= n <= 8
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, n: int) -> list[str]:
        """Return all combinations of n pairs of valid parentheses."""
        res = []

        def backtrack(s, left, right):
            if len(s) == 2 * n:
                res.append(s)
                return
            if left < n:
                backtrack(s + "(", left + 1, right)
            if right < left:
                backtrack(s + ")", left, right + 1)

        backtrack("", 0, 0)
        return res


def demo() -> str:
    n = 3
    print(f"Initial n: {n}")
    s = Solution()
    result = s.solve(n)
    print(f"Final result: {result}")
    return f"Generate Parentheses for n={n} -> {result}"


if __name__ == "__main__":
    demo()


register_problem(
    id=22,
    slug="generate_parentheses",
    title="Generate Parentheses",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "backtracking"],
    url="https://leetcode.com/problems/generate-parentheses/",
    notes="Backtracking with stack constraints. Ensure left>=right always.",
)
