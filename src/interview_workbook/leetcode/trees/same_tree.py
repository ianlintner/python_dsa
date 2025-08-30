"""
Same Tree (LeetCode 100)

Given two binary trees, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical
and the nodes have the same value.
"""

from src.interview_workbook.leetcode._nodes import TreeNode
from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, *args) -> bool:
        """Check if two binary trees are the same using DFS recursion."""
        if len(args) < 2:
            return False
        p, q = args[0], args[1]

        def is_same(t1, t2):
            if not t1 and not t2:
                return True
            if not t1 or not t2:
                return False
            return t1.val == t2.val and is_same(t1.left, t2.left) and is_same(t1.right, t2.right)

        return is_same(p, q)


def demo():
    """Run deterministic test cases for Same Tree."""
    sol = Solution()

    # Case 1: Two identical trees
    t1 = TreeNode(1, TreeNode(2), TreeNode(3))
    t2 = TreeNode(1, TreeNode(2), TreeNode(3))
    result1 = sol.solve(t1, t2)

    # Case 2: Different structure
    t3 = TreeNode(1, TreeNode(2), None)
    t4 = TreeNode(1, None, TreeNode(2))
    result2 = sol.solve(t3, t4)

    return f"Same Tree Test 1 (identical): {result1}\n" f"Same Tree Test 2 (different): {result2}"


# Register the problem with correct parameters
register_problem(
    id=100,
    slug="same-tree",
    title="Same Tree",
    category=Category.TREES,
    difficulty=Difficulty.EASY,
    tags=[],
    url="https://leetcode.com/problems/same-tree/",
    notes="",
)
