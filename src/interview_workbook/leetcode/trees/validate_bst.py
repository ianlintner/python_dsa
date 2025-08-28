"""
LeetCode 98: Validate Binary Search Tree

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Examples:
    Input: root = [2,1,3]
    Output: true

    Input: root = [5,1,4,null,null,3,6]
    Output: false
    Explanation: The root node's value is 5 but its right child's value is 4.

Constraints:
    - The number of nodes in the tree is in the range [1, 10^4].
    - -2^31 <= Node.val <= 2^31 - 1

Time Complexity: O(n) where n is the number of nodes
Space Complexity: O(h) where h is the height of the tree (recursion stack)
"""

from typing import Optional

from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive with min/max bounds.
        For each node, check if its value is within valid range and recurse.
        """

        def validate(node, min_val, max_val):
            if not node:
                return True

            if node.val <= min_val or node.val >= max_val:
                return False

            # Left subtree: all values must be < node.val
            # Right subtree: all values must be > node.val
            return validate(node.left, min_val, node.val) and validate(
                node.right, node.val, max_val
            )

        return validate(root, float("-inf"), float("inf"))

    def isValidBST_inorder(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 2: Inorder traversal should give sorted sequence.
        """

        def inorder(node, values):
            if not node:
                return
            inorder(node.left, values)
            values.append(node.val)
            inorder(node.right, values)

        values = []
        inorder(root, values)

        # Check if values are in strictly increasing order
        for i in range(1, len(values)):
            if values[i] <= values[i - 1]:
                return False
        return True

    def isValidBST_inorder_optimized(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 3: Inorder traversal with early termination.
        Track previous value during traversal without storing all values.
        """
        self.prev = float("-inf")

        def inorder(node):
            if not node:
                return True

            # Check left subtree
            if not inorder(node.left):
                return False

            # Check current node
            if node.val <= self.prev:
                return False
            self.prev = node.val

            # Check right subtree
            return inorder(node.right)

        return inorder(root)

    def isValidBST_iterative(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 4: Iterative inorder traversal using stack.
        """
        stack = []
        prev = float("-inf")
        current = root

        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left

            # Process current node
            current = stack.pop()
            if current.val <= prev:
                return False
            prev = current.val

            # Move to right subtree
            current = current.right

        return True

    def isValidBST_bounds_iterative(self, root: Optional[TreeNode]) -> bool:
        """
        Approach 5: Iterative with explicit bounds checking.
        """
        if not root:
            return True

        stack = [(root, float("-inf"), float("inf"))]

        while stack:
            node, min_val, max_val = stack.pop()

            if node.val <= min_val or node.val >= max_val:
                return False

            if node.right:
                stack.append((node.right, node.val, max_val))
            if node.left:
                stack.append((node.left, min_val, node.val))

        return True


def demo():
    """
    Demonstrate BST validation with multiple approaches.
    """
    print("=== LeetCode 98: Validate Binary Search Tree ===\n")

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
        # Valid BST
        ([2, 1, 3], True),
        # Invalid BST - right child of root violates BST property
        ([5, 1, 4, None, None, 3, 6], False),
        # Single node
        ([1], True),
        # Valid BST - larger tree
        ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], True),
        # Invalid BST - duplicate values
        ([1, 1], False),
        # Invalid BST - left subtree has value greater than root
        ([5, 4, 6, None, None, 3, 7], False),
        # Valid BST - min and max values
        ([2147483647], True),
        # Edge case with negative values
        ([-2147483648, None, 2147483647], True),
        # Invalid - right subtree has smaller value than ancestor
        ([10, 5, 15, None, None, 6, 20], False),
    ]

    for i, (tree_list, expected) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Tree: {tree_list}")
        print(f"Expected: {expected}")

        root = list_to_tree(tree_list)

        # Test all approaches
        result1 = solution.isValidBST(root)
        result2 = solution.isValidBST_inorder(root)
        result3 = solution.isValidBST_inorder_optimized(root)
        result4 = solution.isValidBST_iterative(root)
        result5 = solution.isValidBST_bounds_iterative(root)

        print(f"Bounds recursive result: {result1}")
        print(f"Inorder array result: {result2}")
        print(f"Inorder optimized result: {result3}")
        print(f"Inorder iterative result: {result4}")
        print(f"Bounds iterative result: {result5}")

        # Verify all approaches give same result
        assert result1 == result2 == result3 == result4 == result5 == expected, (
            f"Mismatch in test case {i}"
        )
        print("✅ All approaches passed")
        print()

    print("Algorithm Analysis:")
    print("• Bounds recursive: O(n) time, O(h) space")
    print("• Inorder array: O(n) time, O(n) space")
    print("• Inorder optimized: O(n) time, O(h) space")
    print("• Inorder iterative: O(n) time, O(h) space")
    print("• Bounds iterative: O(n) time, O(h) space")
    print("\nKey Insight:")
    print("• BST property: for each node:")
    print("  - All left descendants < node.val")
    print("  - All right descendants > node.val")
    print("• Inorder traversal of BST gives sorted sequence")
    print("• Bounds approach is most efficient for early termination")


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
    demo()
