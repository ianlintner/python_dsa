"""
Candy

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, ratings):
        """Distribute candies to children based on ratings."""
        n = len(ratings)
        candies = [1] * n

        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)


def demo() -> str:
    """Run a demo for the Candy problem."""
    ratings = [1,0,2]
    print(f"Ratings: {ratings}")
    s = Solution()
    result = s.solve(ratings)
    print(f"Final result: {result}")
    return f"Candy distribution result for ratings {ratings} -> {result}"


if __name__ == "__main__":
    demo()
    

register_problem(
    id=135,
    slug="candy",
    title="Candy",
    category=Category.GREEDY,
    difficulty=Difficulty.HARD,
    tags=["array", "greedy"],
    url="https://leetcode.com/problems/candy/",
    notes="",
)
