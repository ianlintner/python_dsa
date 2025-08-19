"""
LeetCode 125: Valid Palindrome

A phrase is a palindrome if, after converting all uppercase letters into lowercase
letters and removing all non-alphanumeric characters, it reads the same forward
and backward.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

URL: https://leetcode.com/problems/valid-palindrome/
Difficulty: Easy
Category: Two Pointers

Patterns:
- Two pointers from opposite ends
- Character normalization (case, alphanumeric filtering)
- String preprocessing vs on-the-fly processing

Complexity:
- Time: O(n) - single pass with two pointers
- Space: O(1) - only using pointers, no extra space

Pitfalls:
- Remember to handle non-alphanumeric characters
- Case insensitive comparison
- Empty string is considered palindrome
- Single character is palindrome

Follow-ups:
- What if we want to preserve spaces but ignore case?
- Can you do it without creating a new string? (Yes, this solution)
- What about Unicode characters?
- How would you handle very long strings efficiently?
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, run_test_cases, create_demo_output
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        Check if string is a palindrome after normalizing.

        Args:
            s: Input string to check

        Returns:
            True if s is a palindrome, False otherwise
        """
        # Use two pointers approach
        left, right = 0, len(s) - 1

        while left < right:
            # Skip non-alphanumeric characters from left
            while left < right and not s[left].isalnum():
                left += 1

            # Skip non-alphanumeric characters from right
            while left < right and not s[right].isalnum():
                right -= 1

            # Compare characters (case insensitive)
            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True


# Test cases
test_cases = [
    TestCase(("A man, a plan, a canal: Panama",), True, "Classic palindrome with punctuation"),
    TestCase(("race a car",), False, "Not a palindrome"),
    TestCase(("",), True, "Empty string is palindrome"),
    TestCase(("a",), True, "Single character is palindrome"),
    TestCase(("Madam",), True, "Case insensitive palindrome"),
    TestCase(("No 'x' in Nixon",), True, "Complex punctuation"),
    TestCase(("Was it a car or a cat I saw?",), True, "Question marks and mixed case"),
    TestCase(("12321",), True, "Numeric palindrome"),
    TestCase(("A Santa at NASA",), True, "Palindrome with multiple words"),
    TestCase(("Not a palindrome",), False, "Definitely not a palindrome"),
]


def demo() -> str:
    """Run Valid Palindrome demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(
        solution.isPalindrome, test_cases, "LeetCode 125: Valid Palindrome"
    )

    return create_demo_output(
        "Valid Palindrome",
        test_results,
        time_complexity="O(n)",
        space_complexity="O(1)",
        approach_notes="""
Key insights:
1. Two pointers from opposite ends moving inward
2. Skip non-alphanumeric characters on both sides
3. Compare characters case-insensitively
4. No need to create new string - process in place
5. Terminates when pointers meet or cross

Alternative approach: Normalize string first, then check
- Pros: Cleaner logic, easier to understand
- Cons: O(n) extra space, two passes through string
        """.strip(),
    )


# Register the problem
register_problem(
    id=125,
    slug="valid_palindrome",
    title="Valid Palindrome",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.EASY,
    tags=["string", "two_pointers"],
    url="https://leetcode.com/problems/valid-palindrome/",
    notes="Classic two-pointer technique for palindrome validation with character filtering",
)
