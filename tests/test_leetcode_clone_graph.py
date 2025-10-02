from src.interview_workbook.leetcode.graphs.clone_graph import Node, Solution


def build_graph():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node1.neighbors = [node2, node3]
    node2.neighbors = [node1, node4]
    node3.neighbors = [node1, node4]
    node4.neighbors = [node2, node3]
    return node1


def test_clone_graph_structure():
    root = build_graph()
    cloned = Solution().solve(root)
    assert cloned is not root
    assert cloned.val == root.val
    assert len(cloned.neighbors) == 2
    neighbor_vals = sorted([n.val for n in cloned.neighbors])
    assert neighbor_vals == [2, 3]


def test_clone_graph_deep_copy():
    root = build_graph()
    cloned = Solution().solve(root)
    # Ensure deep copy: modifying clone does not affect original
    cloned.val = 99
    assert root.val == 1
    cloned.neighbors[0].val = 42
    assert root.neighbors[0].val == 2
