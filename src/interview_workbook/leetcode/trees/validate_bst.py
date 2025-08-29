"""
LeetCode 98: Validate Binary Search Tree

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Time Complexity:
    O(n) where n is the number of nodes
Space Complexity:
    O(h) where h is the height of the tree (recursion stack)
"""

import random
from typing import List, Optional

from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def isValidBST_bounds(self, root: Optional[TreeNode]) -> bool:
        """Approach 1: Recursive bounds checking"""

        def validate(node: Optional[TreeNode], min_val: float, max_val: float) -> bool:
            if not node:
                return True
            if not (min_val < node.val < max_val):
                return False
            return validate(node.left, min_val, node.val) and validate(
                node.right, node.val, max_val
            )

        return validate(root, float("-inf"), float("inf"))

    def isValidBST_inorder(self, root: Optional[TreeNode]) -> bool:
        """Approach 2: Collect inorder traversal and check if strictly increasing"""
        values: List[int] = []

        def inorder(node: Optional[TreeNode]):
            if not node:
                return
            inorder(node.left)
            values.append(node.val)
            inorder(node.right)

        inorder(root)
        for i in range(1, len(values)):
            if values[i] <= values[i - 1]:
                return False
        return True

    def isValidBST_inorder_optimized(self, root: Optional[TreeNode]) -> bool:
        """Approach 3: Optimized inorder traversal with previous value tracking"""
        self.prev = None

        def inorder(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            if not inorder(node.left):
                return False
            if self.prev is not None and node.val <= self.prev:
                return False
            self.prev = node.val
            return inorder(node.right)

        return inorder(root)

    def isValidBST_iterative(self, root: Optional[TreeNode]) -> bool:
        """Approach 4: Iterative inorder traversal using stack"""
        stack = []
        prev = None
        current = root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            if prev is not None and current.val <= prev:
                return False
            prev = current.val
            current = current.right

        return True

    def isValidBST_bounds_iterative(self, root: Optional[TreeNode]) -> bool:
        """Approach 5: Iterative bounds checking"""
        if not root:
            return True

        stack = [(root, float("-inf"), float("inf"))]
        while stack:
            node, min_val, max_val = stack.pop()
            if not (min_val < node.val < max_val):
                return False
            if node.right:
                stack.append((node.right, node.val, max_val))
            if node.left:
                stack.append((node.left, min_val, node.val))

        return True


def list_to_tree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    """Helper: Convert list to binary tree"""
    if not arr:
        return None
    nodes = [TreeNode(val) if val is not None else None for val in arr]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    return root


def demo() -> str:
    """Demonstrate BST validation with multiple approaches"""
    random.seed(0)  # ensure deterministic

    output_lines = []
    output_lines.append("=== LeetCode 98: Validate Binary Search Tree ===")

    solution = Solution()

    test_cases = [
        ([2, 1, 3], True),
        ([5, 1, 4, None, None, 3, 6], False),
        ([1], True),
        ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], True),
        ([1, 1], False),
        ([5, 4, 6, None, None, 3, 7], False),
        ([2147483647], True),
        ([-2147483648, None, 2147483647], True),
        ([10, 5, 15, None, None, 6, 20], False),
    ]

    for i, (tree_list, expected) in enumerate(test_cases, 1):
        root = list_to_tree(tree_list)
        results = [
            solution.isValidBST_bounds(root),
            solution.isValidBST_inorder(root),
            solution.isValidBST_inorder_optimized(root),
            solution.isValidBST_iterative(root),
            solution.isValidBST_bounds_iterative(root),
        ]
        output_lines.append(f"Test Case {i}: Tree={tree_list}, Expected={expected}, Got={results}")
        assert all(r == expected for r in results), f"Mismatch in case {i}"

    output_lines.append("✅ All test cases passed")
    return "\n".join(output_lines)


# Register the problem
register_problem(
    id=98,
    slug="validate_bst",
    title="Validate Binary Search Tree",
    category=Category.TREES,
    difficulty="Medium",
    tags=["tree", "dfs", "bst", "inorder-traversal"],
    url="https://leetcode.com/problems/validate-binary-search-tree/",
)


if __name__ == "__main__":
    print(demo())
