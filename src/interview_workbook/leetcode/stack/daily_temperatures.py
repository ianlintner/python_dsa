from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty

"""
Daily Temperatures

TODO: Add problem description
"""


class Solution:
    def solve(self, temperatures) -> list[int]:
        """Return number of days to wait until a warmer temperature for each day."""
        n = len(temperatures)
        res = [0] * n
        stack = []
        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                j = stack.pop()
                res[j] = i - j
            stack.append(i)
        return res


def demo() -> str:
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"Initial temperatures: {temps}")
    s = Solution()
    result = s.solve(temps)
    print(f"Final result: {result}")
    return f"Daily temperatures result for {temps} -> {result}"


if __name__ == "__main__":
    demo()


register_problem(
    id=739,
    slug="daily_temperatures",
    title="Daily Temperatures",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "monotonic stack"],
    url="https://leetcode.com/problems/daily-temperatures/",
    notes="Use a monotonic stack to track previous warmer days.",
)
