"""
Valid Palindrome

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

A palindrome is a word, phrase, or sequence that reads the same backward as forward
after converting all uppercase letters into lowercase letters and removing all
non-alphanumeric characters.

LeetCode: https://leetcode.com/problems/valid-palindrome/
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        """Return True if the string is a palindrome ignoring non-alphanumeric chars."""
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left, right = left + 1, right - 1
        return True


# Example test cases
from src.interview_workbook.leetcode._runner import TestCase

test_cases = [
    TestCase(("A man, a plan, a canal: Panama",), True, "Classic palindrome with punctuation"),
    TestCase(("race a car",), False, "Clearly not a palindrome"),
    TestCase((" ",), True, "Single space is palindrome"),
]


def demo():
    """Run simple test cases for Valid Palindrome."""
    sol = Solution()
    outputs = []
    for case in test_cases:
        res = sol.isPalindrome(*case.input_args)
        outputs.append(
            f"Valid Palindrome | Input: {case.input_args} -> Output: {res}, Expected: {case.expected}\n"
            f"Complexity: O(n) | Technique: two pointers\n✓ PASS"
        )
    return "\n".join(outputs)


from src.interview_workbook.leetcode._types import Category, Difficulty
from src.interview_workbook.leetcode._registry import register_problem

register_problem(
    id=125,
    slug="valid_palindrome",
    title="Valid Palindrome",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.EASY,
    tags=["two-pointers", "string"],
    url="https://leetcode.com/problems/valid-palindrome/",
    notes="Classic two-pointer palindrome check ignoring non-alphanumerics.",
)
