"""
Balanced Binary Tree

TODO: Add problem description
"""

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, root) -> bool:
        """
        Check if a binary tree is height-balanced.
        A height-balanced tree is defined as:
        the depth of the two subtrees of every node never differs by more than one.
        """

        def check(node):
            if not node:
                return 0, True
            left_height, left_bal = check(node.left)
            right_height, right_bal = check(node.right)
            balanced = left_bal and right_bal and abs(left_height - right_height) <= 1
            return max(left_height, right_height) + 1, balanced

        return check(root)[1]


def demo():
    """Run a simple demonstration of balanced binary tree check."""

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Balanced tree
    root_balanced = TreeNode(1, TreeNode(2), TreeNode(3))

    # Unbalanced tree
    root_unbalanced = TreeNode(1)
    root_unbalanced.left = TreeNode(2)
    root_unbalanced.left.left = TreeNode(3)

    sol = Solution()
    return (
        f"Balanced tree check (should be True): {sol.solve(root_balanced)}\n"
        f"Unbalanced tree check (should be False): {sol.solve(root_unbalanced)}"
    )


# TODO: Register the problem with correct parameters
register_problem(
    id=0,
    slug="balanced_binary_tree",
    title="Balanced Binary Tree",
    category=Category.TREES,
    difficulty=Difficulty.EASY,
    tags=[],
    url="",
    notes="",
)
