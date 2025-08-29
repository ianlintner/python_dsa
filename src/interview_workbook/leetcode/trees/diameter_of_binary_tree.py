"""
Diameter Of Binary Tree

Problem: Diameter of Binary Tree
LeetCode link: https://leetcode.com/problems/diameter-of-binary-tree/
Description: Find the length of the longest path between any two nodes in a binary tree. The path may or may not pass through the root.
"""


class Solution:
    def solve(self, root) -> int:
        """
        Find the diameter of a binary tree.
        The diameter is defined as the length of the longest path between any two nodes.
        """
        self.diameter = 0

        def depth(node):
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            self.diameter = max(self.diameter, left + right)
            return max(left, right) + 1

        depth(root)
        return self.diameter


def demo():
    """Run a simple demonstration of diameter of binary tree."""

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Build a test tree:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3)

    sol = Solution()
    result = sol.solve(root)
    return f"Diameter of binary tree: {result}"


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="diameter_of_binary_tree",
#     title="Diameter Of Binary Tree",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
