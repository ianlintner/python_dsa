"""
Merge Triplets

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, triplets, target):
        """Check if we can merge triplets to form the target triplet."""
        good = set()
        for t in triplets:
            if all(t[i] <= target[i] for i in range(3)):
                for i in range(3):
                    if t[i] == target[i]:
                        good.add(i)
        return len(good) == 3


def demo() -> str:
    """Run a demo for the Merge Triplets problem."""
    triplets = [[2,5,3],[1,8,4],[1,7,5]]
    target = [2,7,5]
    print(f"Triplets: {triplets}, Target: {target}")
    s = Solution()
    result = s.solve(triplets, target)
    print(f"Final result: {result}")
    return f"Merge Triplets result for target {target} -> {result}"


if __name__ == "__main__":
    demo()
    

register_problem(
    id=1899,
    slug="merge_triplets",
    title="Merge Triplets to Form Target Triplet",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "greedy"],
    url="https://leetcode.com/problems/merge-triplets-to-form-target-triplet/",
    notes="",
)
