"""
LeetCode 20: Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

URL: https://leetcode.com/problems/valid-parentheses/
Difficulty: Easy
Category: Stack

Patterns:
- Stack for bracket matching
- Hash map for bracket pairs

Complexity:
- Time: O(n) where n is length of string
- Space: O(n) for the stack in worst case

Pitfalls:
- Don't forget to check if stack is empty before popping
- Handle edge cases: empty string, unmatched opening brackets
- Make sure to use correct bracket pairs

Follow-ups:
- What if we had other types of brackets like '<>', '《》'?
- How would you handle nested structures with different rules?
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def isValid(self, s: str) -> bool:
        """
        Check if parentheses/brackets are valid using a stack.

        Args:
            s: String containing brackets

        Returns:
            True if brackets are properly matched, False otherwise
        """
        # Stack to keep track of opening brackets
        stack = []

        # Mapping of closing brackets to opening brackets
        bracket_map = {")": "(", "}": "{", "]": "["}

        for char in s:
            if char in bracket_map:  # Closing bracket
                # Check if stack is empty or top doesn't match
                if not stack or stack.pop() != bracket_map[char]:
                    return False
            else:  # Opening bracket
                stack.append(char)

        # Valid if no unmatched opening brackets remain
        return len(stack) == 0


# Test cases
test_cases = [
    TestCase(
        input_args=("(,
    )",), True, "Simple valid parentheses"),
    TestCase(
        input_args=("(,
    )[]{}",), True, "Multiple valid bracket types"),
    TestCase(
        input_args=("(]",,
    ), False, "Wrong bracket type"),
    TestCase(
        input_args=("([,
    )]",), False, "Wrong bracket order"),
    TestCase(
        input_args=("{[]}",,
    ), True, "Nested brackets"),
    TestCase(
        input_args=("",,
    ), True, "Empty string"),
    TestCase(
        input_args=("(",,
    ), False, "Unmatched opening"),
    TestCase(
        input_args=(",
    )",), False, "Unmatched closing"),
    TestCase(
        input_args=("(((",,
    ), False, "Multiple unmatched opening"),
    TestCase(
        input_args=(",
    )))",), False, "Multiple unmatched closing"),
]


def demo() -> str:
    """Run Valid Parentheses demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.isValid, test_cases, "LeetCode 20: Valid Parentheses")

    return create_demo_output(
        "Valid Parentheses",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use a stack to keep track of opening brackets
2. For each closing bracket, check if it matches the most recent opening bracket
3. Use a hash map to efficiently map closing brackets to their opening counterparts
4. Valid string means all brackets are matched and stack is empty at the end
        """.strip(),
    )


# Register the problem
register_problem(
    id=20,
    slug="valid_parentheses",
    title="Valid Parentheses",
    category=Category.STACK,
    difficulty=Difficulty.EASY,
    tags=["string", "stack"],
    url="https://leetcode.com/problems/valid-parentheses/",
    notes="TODO: Add implementation notes",
)
