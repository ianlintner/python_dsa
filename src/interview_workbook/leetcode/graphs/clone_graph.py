"""
Clone Graph

TODO: Add problem description
"""


from collections import deque

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


def demo():
    """Run a demo for the Clone Graph problem."""
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


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="clone_graph",
#     title="Clone Graph",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
