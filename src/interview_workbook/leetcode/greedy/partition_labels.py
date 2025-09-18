"""
Partition Labels

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> list[int]:
        """
        Greedy solution to Partition Labels.
        Returns a list of partition lengths.
        """
        s = args[0]
        last_index = {c: i for i, c in enumerate(s)}
        partitions = []
        start = end = 0
        for i, c in enumerate(s):
            end = max(end, last_index[c])
            if i == end:
                partitions.append(end - start + 1)
                start = i + 1
        return partitions


def demo() -> str:
    """Run a demo for the Partition Labels problem."""
    s = "ababcbacadefegdehijhklij"
    print(f"Input string: {s}")
    solver = Solution()
    result = solver.solve(s)
    print(f"Final result: {result}")
    return f"Partition Labels result for '{s}' -> {result}"


if __name__ == "__main__":
    demo()


register_problem(
    id=763,
    slug="partition_labels",
    title="Partition Labels",
    category=Category.GREEDY,
    difficulty=Difficulty.MEDIUM,
    tags=["string", "greedy", "two_pointers"],
    url="https://leetcode.com/problems/partition-labels/",
    notes="",
)
