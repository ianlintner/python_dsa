"""
LeetCode 22: Generate Parentheses

Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

Example 1:
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:
Input: n = 1
Output: ["()"]

Constraints:
- 1 <= n <= 8

URL: https://leetcode.com/problems/generate-parentheses/
Difficulty: Medium
Category: Stack

Patterns:
- Backtracking
- String manipulation
- Recursive generation

Complexity:
- Time: O(4^n / sqrt(n)) - Catalan number
- Space: O(4^n / sqrt(n))

Pitfalls:
- Not tracking open/close parentheses count properly
- Adding closing parentheses when there are no open ones
- Forgetting to backtrack properly

Follow-ups:
- Generate parentheses with different bracket types
- Check if a string of parentheses is valid
"""

from typing import List
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def generateParentheses(self, n: int) -> List[str]:
        """
        Generate all valid combinations of n pairs of parentheses using backtracking.

        Args:
            n: Number of pairs of parentheses

        Returns:
            List of all valid parentheses combinations
        """
        result = []

        def backtrack(current: str, open_count: int, close_count: int) -> None:
            # Base case: we've used all n pairs
            if len(current) == 2 * n:
                result.append(current)
                return

            # Add opening parenthesis if we haven't used all n
            if open_count < n:
                backtrack(current + "(", open_count + 1, close_count)

            # Add closing parenthesis if we have unmatched opening ones
            if close_count < open_count:
                backtrack(current + ")", open_count, close_count + 1)

        backtrack("", 0, 0)
        return result


# Test cases
test_cases = [
    TestCase((1,), ["()"], "Example: n=1"),
    TestCase((2,), ["(())", "()()"], "Example: n=2"),
    TestCase((3,), ["((()))", "(()())", "(())()", "()(())", "()()()"], "Example: n=3"),
    TestCase((0,), [""], "Edge case: n=0"),
    TestCase(
        (4,),
        [
            "(((())))",
            "((()()))",
            "((())())",
            "((()))()",
            "(()(()))",
            "(()()())",
            "(()())()",
            "(())(())",
            "(())()()",
            "()((()))",
            "()(()())",
            "()(())()",
            "()()(())",
            "()()()()",
        ],
        "Larger case: n=4",
    ),
]


def demo() -> str:
    """Run Generate Parentheses demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.generateParentheses, test_cases, "LeetCode 22: Generate Parentheses"
    )

    return create_demo_output(
        "Generate Parentheses",
        test_results,
        time_complexity="O(4^n / √n)",
        space_complexity="O(4^n / √n)",
        approach_notes="""
Key insights:
1. Use backtracking to explore all possible combinations
2. Track count of open and close parentheses to ensure validity
3. Only add '(' when we haven't reached the limit of n open parentheses
4. Only add ')' when we have more open than close parentheses (ensures validity)
5. The time complexity is the nth Catalan number: 4^n / √(πn)
        """.strip(),
    )


# Register the problem
register_problem(
    id=22,
    slug="generate_parentheses",
    title="Generate Parentheses",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "dynamic_programming", "backtracking"],
    url="https://leetcode.com/problems/generate-parentheses/",
    notes="Classic backtracking problem using recursive generation with constraints",
)
