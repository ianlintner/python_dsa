"""
Monotone Increasing Digits

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, n: int) -> int:
        """Return the largest number less than or equal to n with monotone increasing digits."""
        digits = list(str(n))
        i = 1
        while i < len(digits) and digits[i - 1] <= digits[i]:
            i += 1
        if i < len(digits):
            while i > 0 and digits[i - 1] > digits[i]:
                digits[i - 1] = str(int(digits[i - 1]) - 1)
                i -= 1
            for j in range(i + 1, len(digits)):
                digits[j] = '9'
        return int("".join(digits))


def demo() -> str:
    """Run a demo for the Monotone Increasing Digits problem."""
    n = 332
    print(f"Input number: {n}")
    s = Solution()
    result = s.solve(n)
    print(f"Final result: {result}")
    return f"Monotone Increasing Digits result for {n} -> {result}"


if __name__ == "__main__":
    demo()
    

register_problem(
    id=738,
    slug="monotone_increasing_digits",
    title="Monotone Increasing Digits",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["greedy"],
    url="https://leetcode.com/problems/monotone-increasing-digits/",
    notes="",
)
