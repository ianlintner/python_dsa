"""
LeetCode 110: Balanced Binary Tree

Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is a binary tree in which the depth of the two
subtrees of every node never differ by more than 1.

Examples:
    Input: root = [3,9,20,null,null,15,7]
    Output: true

    Input: root = [1,2,2,3,3,null,null,4,4]
    Output: false

    Input: root = []
    Output: true

Constraints:
    - The number of nodes in the tree is in the range [0, 5000].
    - -10^4 <= Node.val <= 10^4

Time Complexity: O(n) where n is the number of nodes
Space Complexity: O(h) where h is the height of the tree (recursion stack)
"""

from typing import Optional
from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 1: Top-down recursion (inefficient - O(n^2))
        Check height difference at each node by calculating heights.
        """
        if not root:
            return True

        def height(node):
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))

        left_height = height(root.left)
        right_height = height(root.right)

        return (
            abs(left_height - right_height) <= 1
            and self.isBalanced(root.left)
            and self.isBalanced(root.right)
        )

    def isBalanced_optimal(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 2: Bottom-up recursion (optimal - O(n))
        Use helper function that returns both height and balance status.
        """

        def check_balance(node):
            # Returns (is_balanced, height)
            if not node:
                return True, 0

            left_balanced, left_height = check_balance(node.left)
            if not left_balanced:
                return False, 0

            right_balanced, right_height = check_balance(node.right)
            if not right_balanced:
                return False, 0

            current_height = 1 + max(left_height, right_height)
            is_balanced = abs(left_height - right_height) <= 1

            return is_balanced, current_height

        return check_balance(root)[0]

    def isBalanced_clean(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 3: Clean bottom-up using -1 as sentinel for unbalanced.
        """

        def get_height(node):
            if not node:
                return 0

            left_height = get_height(node.left)
            if left_height == -1:
                return -1

            right_height = get_height(node.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return 1 + max(left_height, right_height)

        return get_height(root) != -1


def demo():
    """
    Demonstrate balanced binary tree checking with multiple approaches.
    """
    print("=== LeetCode 110: Balanced Binary Tree ===\n")

    solution = Solution()

    # Helper function to create trees from lists
    def list_to_tree(arr):
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

    # Test cases
    test_cases = [
        # Balanced tree
        ([3, 9, 20, None, None, 15, 7], True),
        # Unbalanced tree
        ([1, 2, 2, 3, 3, None, None, 4, 4], False),
        # Empty tree
        ([], True),
        # Single node
        ([1], True),
        # Left skewed (unbalanced)
        ([1, 2, None, 3, None, 4], False),
        # Perfectly balanced
        ([1, 2, 3, 4, 5, 6, 7], True),
    ]

    for i, (tree_list, expected) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Tree: {tree_list}")
        print(f"Expected: {expected}")

        root = list_to_tree(tree_list)

        # Test all approaches
        result1 = solution.isBalanced(root)
        result2 = solution.isBalanced_optimal(root)
        result3 = solution.isBalanced_clean(root)

        print(f"Top-down result: {result1}")
        print(f"Bottom-up result: {result2}")
        print(f"Clean result: {result3}")

        # Verify all approaches give same result
        assert result1 == result2 == result3 == expected, f"Mismatch in test case {i}"
        print(f"✅ All approaches passed")
        print()

    print("Algorithm Analysis:")
    print("• Top-down approach: O(n²) time - recalculates heights")
    print("• Bottom-up approach: O(n) time - single traversal")
    print("• Clean approach: O(n) time - uses sentinel value")
    print("• Space complexity: O(h) for all approaches (recursion stack)")
    print("\nKey Insight:")
    print("• A tree is balanced if:")
    print("  1. Left subtree is balanced")
    print("  2. Right subtree is balanced")
    print("  3. Height difference ≤ 1")
    print("• Bottom-up is optimal - avoid redundant height calculations")


# Register the problem
register_problem(
    id=110,
    slug="balanced_binary_tree",
    title="Balanced Binary Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "binary-tree", "height-balanced"],
    url="https://leetcode.com/problems/balanced-binary-tree/",
)


if __name__ == "__main__":
    demo()
