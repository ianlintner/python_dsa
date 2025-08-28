"""
LeetCode 104: Maximum Depth of Binary Tree
https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -100 <= Node.val <= 100
"""

from typing import Optional
from collections import deque
from .._types import Category
from .._registry import register_problem
from .._nodes import TreeNode


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using recursive DFS.
        
        Time: O(n) - visit each node once
        Space: O(h) - recursion stack, h = height of tree
        """
        if not root:
            return 0
        
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)
    
    def maxDepthIterative(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using iterative BFS (level-order).
        
        Time: O(n) - visit each node once
        Space: O(w) - queue space, w = maximum width
        """
        if not root:
            return 0
        
        queue = deque([(root, 1)])
        max_depth = 0
        
        while queue:
            node, depth = queue.popleft()
            max_depth = max(max_depth, depth)
            
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        
        return max_depth
    
    def maxDepthLevelOrder(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using level-by-level BFS.
        
        Time: O(n) - visit each node once
        Space: O(w) - queue space, w = maximum width
        """
        if not root:
            return 0
        
        queue = deque([root])
        depth = 0
        
        while queue:
            depth += 1
            level_size = len(queue)
            
            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        
        return depth
    
    def maxDepthIterativeDFS(self, root: Optional[TreeNode]) -> int:
        """
        Find maximum depth using iterative DFS with explicit stack.
        
        Time: O(n) - visit each node once
        Space: O(h) - stack space
        """
        if not root:
            return 0
        
        stack = [(root, 1)]
        max_depth = 0
        
        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))
        
        return max_depth


def demo():
    """Demonstrate maximum depth calculation with comprehensive test cases."""
    solution = Solution()
    
    def list_to_tree(vals: list) -> Optional[TreeNode]:
        """Convert level-order list to tree for testing."""
        if not vals:
            return None
        
        root = TreeNode(vals[0])
        queue = deque([root])
        i = 1
        
        while queue and i < len(vals):
            node = queue.popleft()
            
            if i < len(vals) and vals[i] is not None:
                node.left = TreeNode(vals[i])
                queue.append(node.left)
            i += 1
            
            if i < len(vals) and vals[i] is not None:
                node.right = TreeNode(vals[i])
                queue.append(node.right)
            i += 1
        
        return root
    
    test_cases = [
        {
            "name": "Example 1: balanced tree",
            "input": [3, 9, 20, None, None, 15, 7],
            "expected": 3
        },
        {
            "name": "Example 2: right skewed",
            "input": [1, None, 2],
            "expected": 2
        },
        {
            "name": "Single node",
            "input": [1],
            "expected": 1
        },
        {
            "name": "Empty tree",
            "input": [],
            "expected": 0
        },
        {
            "name": "Left skewed tree",
            "input": [1, 2, None, 3, None, 4],
            "expected": 4
        },
        {
            "name": "Complete binary tree",
            "input": [1, 2, 3, 4, 5, 6, 7],
            "expected": 3
        },
        {
            "name": "Deep tree",
            "input": [1, 2, 3, 4, None, None, 7, 8, None, None, None, None, None, 15],
            "expected": 4
        },
        {
            "name": "Full tree depth 4",
            "input": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "expected": 4
        }
    ]
    
    print("=== LeetCode 104: Maximum Depth of Binary Tree ===\n")
    
    for i, test in enumerate(test_cases, 1):
        root = list_to_tree(test["input"])
        result = solution.maxDepth(root)
        
        status = "✓ PASS" if result == test["expected"] else "✗ FAIL"
        print(f"Test Case {i}: {status}")
        print(f"  Description: {test['name']}")
        print(f"  Input: {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got: {result}")
        
        if result != test["expected"]:
            print(f"  ❌ Mismatch!")
        print()
    
    # Test all approaches on a sample case
    print("Algorithm Comparison:")
    test_input = [3, 9, 20, None, None, 15, 7]
    expected = 3
    
    approaches = [
        ("Recursive DFS", solution.maxDepth),
        ("Iterative BFS (node+depth)", solution.maxDepthIterative), 
        ("Level-order BFS", solution.maxDepthLevelOrder),
        ("Iterative DFS (stack)", solution.maxDepthIterativeDFS)
    ]
    
    for name, method in approaches:
        root = list_to_tree(test_input)
        result = method(root)
        status = "✓" if result == expected else "✗"
        print(f"  {name}: {status} (depth = {result})")
    
    print(f"\nComplexity Analysis:")
    print(f"  Time: O(n) - must visit every node")
    print(f"  Space:")
    print(f"    Recursive DFS: O(h) - recursion stack")
    print(f"    Iterative BFS: O(w) - queue width")
    print(f"    Iterative DFS: O(h) - explicit stack")
    print(f"    Best case (balanced): O(log n)")
    print(f"    Worst case (skewed): O(n)")
    
    print(f"\nKey Insights:")
    print(f"  • Base case: null node has depth 0")
    print(f"  • Recursive: 1 + max(left_depth, right_depth)")
    print(f"  • BFS naturally processes level-by-level")
    print(f"  • DFS can use explicit stack with depth tracking")
    print(f"  • All approaches have same time complexity")


# Register the problem
register_problem(
    id=104,
    slug="max_depth_binary_tree",
    title="Maximum Depth of Binary Tree",
    category=Category.TREES,
    difficulty="Easy",
    tags=["tree", "dfs", "bfs", "binary-tree", "recursion"],
    url="https://leetcode.com/problems/maximum-depth-of-binary-tree/"
)


if __name__ == "__main__":
    demo()
