"""
Clone Graph

LeetCode 133. Clone Graph

Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.
Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

Constraints:
- The number of nodes in the graph is in the range [0, 100].
- 1 <= Node.val <= 100
- Node.val is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The graph is connected and all nodes can be visited starting from the given node.
"""

from collections import deque
from typing import Optional

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Node:
    def __init__(self, val):
        self.val = val
        self.neighbors = []

    def __repr__(self):
        return f"Node({self.val})"


class Solution:
    def solve(self, node: Node) -> Optional[Node]:
        """Clone an undirected graph using BFS."""
        if not node:
            return None

        clones: dict[Node, Node] = {}
        clones[node] = Node(node.val)
        queue = deque([node])

        while queue:
            curr = queue.popleft()
            for nei in curr.neighbors:
                if nei not in clones:
                    clones[nei] = Node(nei.val)
                    queue.append(nei)
                clones[curr].neighbors.append(clones[nei])
        return clones[node]


def demo() -> str:
    """Run a demo for the Clone Graph problem."""
    # Simple graph: 1--2, 1--3, 2--4, 3--4

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
    print("Graph constructed with Node instances.")
    print(node1)
    s.solve(node1)
    print("Graph cloned successfully (root node returned).")
    return "Clone Graph demo executed"


if __name__ == "__main__":
    demo()


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
