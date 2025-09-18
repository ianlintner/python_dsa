"""
Clone Graph

TODO: Add problem description
"""

from collections import deque

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, node):
        """Clone an undirected graph using BFS."""
        if not node:
            return None

        clones = {}
        clones[node] = type(node)(node.val)
        queue = deque([node])

        while queue:
            curr = queue.popleft()
            for nei in curr.neighbors:
                if nei not in clones:
                    clones[nei] = type(nei)(nei.val)
                    queue.append(nei)
                clones[curr].neighbors.append(clones[nei])
        return clones[node]


def demo() -> str:
    """Run a demo for the Clone Graph problem."""
    # Simple graph: 1--2, 1--3, 2--4, 3--4
    from collections import defaultdict
    graph = {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]}
    print(f"Initial graph adjacency list: {graph}")
    s = Solution()
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node1.neighbors = [node2, node3]
    node2.neighbors = [node1, node4]
    node3.neighbors = [node1, node4]
    node4.neighbors = [node2, node3]
    result = s.solve(node1)
    print("Graph cloned successfully (root node returned).")
    return "Clone Graph demo executed"
    
    
if __name__ == "__main__":
    demo()

    class Node:
        def __init__(self, val):
            self.val = val
            self.neighbors = []

        def __repr__(self):
            return f"Node({self.val})"

    # Build a simple graph: 1 -- 2, 1 -- 3
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.neighbors = [n2, n3]
    n2.neighbors = [n1]
    n3.neighbors = [n1]

    solver = Solution()
    clone = solver.solve(n1)
    return f"Cloned node val: {clone.val}, neighbors: {[nei.val for nei in clone.neighbors]}"


register_problem(
    id=133,
    slug="clone_graph",
    title="Clone Graph",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["hashmap", "dfs", "bfs", "graph"],
    url="https://leetcode.com/problems/clone-graph/",
    notes="",
)
