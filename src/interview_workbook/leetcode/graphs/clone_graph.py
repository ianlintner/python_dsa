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
    """TODO: Implement demo function."""
    pass


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
