"""
LeetCode 572: Subtree of Another Tree

Given the roots of two binary trees root and subRoot, return true if there is a
subtree of root with the same structure and node values of subRoot and false otherwise.

A subtree of a binary tree tree is a tree that consists of a node in tree and
all of this node's descendants. The tree tree could also be considered as a
subtree of itself.

Examples:
    Input: root = [3,4,5,1,2], subRoot = [4,1,2]
    Output: true

    Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
    Output: false

Constraints:
    - The number of nodes in the root tree is in the range [1, 2000].
    - The number of nodes in the subRoot tree is in the range [1, 1000].
    - -10^4 <= root.val <= 10^4
    - -10^4 <= subRoot.val <= 10^4

Time Complexity: O(m * n) where m and n are the number of nodes in each tree
Space Complexity: O(max(m, n)) for recursion stack
"""

from typing import Optional

from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 1: Recursive traversal with same tree check.
        For each node in root, check if subtree starting from that node equals subRoot.
        """
        if not subRoot:
            return True  # Empty tree is subtree of any tree
        if not root:
            return False

        # Check if current subtree matches
        if self.isSameTree(root, subRoot):
            return True

        # Check left and right subtrees
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """Helper function to check if two trees are identical."""
        if not p and not q:
            return True
        if not p or not q:
            return False
        return (
            p.val == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
        )

    def isSubtree_serialization(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach 2: String serialization and substring search.
        Convert both trees to strings and check if subRoot string is substring of root string.
        """
        if not subRoot:
            return True  # Empty tree is subtree of any tree

        def serialize(node):
            if not node:
                return "null"
            return f"#{node.val}#{serialize(node.left)}#{serialize(node.right)}"

        root_str = serialize(root)
        subroot_str = serialize(subRoot)

        return subroot_str in root_str

    def isSubtree_preorder(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 3: Preorder traversal with KMP-like matching.
        Use preorder traversal to find potential matches.
        """

        def preorder(node, path):
            if not node:
                path.append(None)
                return
            path.append(node.val)
            preorder(node.left, path)
            preorder(node.right, path)

        def matches_at_position(root_path, sub_path, start):
            if start + len(sub_path) > len(root_path):
                return False
            for i in range(len(sub_path)):
                if root_path[start + i] != sub_path[i]:
                    return False
            return True

        root_path = []
        sub_path = []
        preorder(root, root_path)
        preorder(subRoot, sub_path)

        # Check all positions where subtree could match
        for i in range(len(root_path) - len(sub_path) + 1):
            if matches_at_position(root_path, sub_path, i):
                return True
        return False

    def isSubtree_optimized(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Approach 4: Optimized with early termination.
        Only check subtrees that have matching root values.
        """
        if not subRoot:
            return True  # Empty tree is subtree of any tree
        if not root:
            return False

        def find_candidates(node, target_val, candidates):
            if not node:
                return
            if node.val == target_val:
                candidates.append(node)
            find_candidates(node.left, target_val, candidates)
            find_candidates(node.right, target_val, candidates)

        candidates = []
        find_candidates(root, subRoot.val, candidates)

        for candidate in candidates:
            if self.isSameTree(candidate, subRoot):
                return True
        return False


def demo():
    """
    Demonstrate subtree checking with multiple approaches.
    """
    print("=== LeetCode 572: Subtree of Another Tree ===\n")

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
        # Subtree exists
        ([3, 4, 5, 1, 2], [4, 1, 2], True),
        # Subtree doesn't exist (extra node in main tree)
        ([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], False),
        # Whole tree is subtree
        ([1, 2, 3], [1, 2, 3], True),
        # Single node subtree exists
        ([1, 2, 3], [2], True),
        # Single node subtree doesn't exist
        ([1, 2, 3], [4], False),
        # Empty subtree
        ([1, 2, 3], [], True),
        # Subtree at root
        ([3, 4, 5, 1, 2, 6, 7], [3, 4, 5, 1, 2, 6, 7], True),
        # Complex case - subtree in right branch
        ([1, 2, 3, 4, 5, None, 6, None, None, 7, 8], [3, None, 6], True),
    ]

    for i, (tree_list, subtree_list, expected) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Root: {tree_list}")
        print(f"SubRoot: {subtree_list}")
        print(f"Expected: {expected}")

        root = list_to_tree(tree_list)
        subRoot = list_to_tree(subtree_list)

        # Test all approaches
        result1 = solution.isSubtree(root, subRoot)
        result2 = solution.isSubtree_serialization(root, subRoot)
        result3 = solution.isSubtree_optimized(root, subRoot)

        print(f"Recursive result: {result1}")
        print(f"Serialization result: {result2}")
        print(f"Optimized result: {result3}")

        # Verify all approaches give same result
        assert result1 == result2 == result3 == expected, f"Mismatch in test case {i}"
        print("✅ All approaches passed")
        print()

    print("Algorithm Analysis:")
    print("• Recursive: O(m*n) time, O(max(m,n)) space")
    print("• Serialization: O(m+n) time, O(m+n) space")
    print("• Optimized: O(m*k) time where k is # of matching root values")
    print("• Space complexity: O(max(m,n)) for recursion stack")
    print("\nKey Insight:")
    print("• A tree T is a subtree of S if:")
    print("  1. T equals S, OR")
    print("  2. T is a subtree of S.left, OR")
    print("  3. T is a subtree of S.right")
    print("• Serialization approach can have false positives without careful delimiter choice")


# Register the problem
register_problem(
    id=572,
    slug="subtree_of_another_tree",
    title="Subtree of Another Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "string-matching", "hash-table"],
    url="https://leetcode.com/problems/subtree-of-another-tree/",
)


if __name__ == "__main__":
    demo()
