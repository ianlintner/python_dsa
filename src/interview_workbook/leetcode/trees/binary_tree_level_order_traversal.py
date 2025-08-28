"""
LeetCode 102: Binary Tree Level Order Traversal

Given the root of a binary tree, return the level order traversal of its nodes'
values. (i.e., from left to right, level by level).

Examples:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]

    Input: root = [1]
    Output: [[1]]

    Input: root = []
    Output: []

Constraints:
    - The number of nodes in the tree is in the range [0, 2000].
    - -1000 <= Node.val <= 1000

Time Complexity: O(n) where n is the number of nodes
Space Complexity: O(w) where w is the maximum width of the tree
"""

from typing import Optional, List
from collections import deque
from .._nodes import TreeNode
from .._registry import register_problem
from .._types import Category


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach 1: BFS with queue - process level by level.
        """
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            level_nodes = []

            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                level_nodes.append(node.val)

                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_nodes)

        return result

    def levelOrder_recursive(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach 2: Recursive DFS with level tracking.
        """
        result = []

        def dfs(node, level):
            if not node:
                return

            # Create new level if needed
            if level >= len(result):
                result.append([])

            # Add current node to its level
            result[level].append(node.val)

            # Recurse on children
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)

        dfs(root, 0)
        return result

    def levelOrder_two_queues(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach 3: BFS with two alternating queues.
        """
        if not root:
            return []

        result = []
        current_level = [root]

        while current_level:
            level_values = []
            next_level = []

            for node in current_level:
                level_values.append(node.val)

                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            result.append(level_values)
            current_level = next_level

        return result

    def levelOrder_with_markers(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Approach 4: BFS with level markers (None as separator).
        """
        if not root:
            return []

        result = []
        queue = deque([root, None])  # None marks end of level
        level_nodes = []

        while queue:
            node = queue.popleft()

            if node is None:
                # End of current level
                result.append(level_nodes)
                level_nodes = []

                # Add marker for next level if queue not empty
                if queue:
                    queue.append(None)
            else:
                level_nodes.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result


def demo():
    """
    Demonstrate level order traversal with multiple approaches.
    """
    print("=== LeetCode 102: Binary Tree Level Order Traversal ===\n")

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
        # Standard tree
        ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
        # Single node
        ([1], [[1]]),
        # Empty tree
        ([], []),
        # Left skewed tree
        ([1, 2, None, 3, None, 4], [[1], [2], [3], [4]]),
        # Right skewed tree
        ([1, None, 2, None, 3, None, 4], [[1], [2], [3], [4]]),
        # Perfect binary tree
        ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]]),
        # Complex tree
        (
            [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1],
            [[5], [4, 8], [11, 13, 4], [7, 2, 1]],
        ),
    ]

    for i, (tree_list, expected) in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Tree: {tree_list}")
        print(f"Expected: {expected}")

        root = list_to_tree(tree_list)

        # Test all approaches
        result1 = solution.levelOrder(root)
        result2 = solution.levelOrder_recursive(root)
        result3 = solution.levelOrder_two_queues(root)
        result4 = solution.levelOrder_with_markers(root)

        print(f"BFS queue result: {result1}")
        print(f"Recursive DFS result: {result2}")
        print(f"Two queues result: {result3}")
        print(f"Markers result: {result4}")

        # Verify all approaches give same result
        assert result1 == result2 == result3 == result4 == expected, f"Mismatch in test case {i}"
        print(f"✅ All approaches passed")
        print()

    print("Algorithm Analysis:")
    print("• BFS queue: O(n) time, O(w) space where w is max width")
    print("• Recursive DFS: O(n) time, O(h + n) space for recursion + result")
    print("• Two queues: O(n) time, O(w) space")
    print("• Markers: O(n) time, O(w) space")
    print("\nKey Insight:")
    print("• Level order = BFS traversal")
    print("• Track level boundaries to group nodes")
    print("• Queue size at start of iteration = nodes in current level")
    print("• Recursive approach: DFS with level parameter")


# Register the problem
register_problem(
    id=102,
    slug="binary_tree_level_order_traversal",
    title="Binary Tree Level Order Traversal",
    category=Category.TREES,
    difficulty="Medium",
    tags=["tree", "bfs", "queue"],
    url="https://leetcode.com/problems/binary-tree-level-order-traversal/",
)


if __name__ == "__main__":
    demo()
