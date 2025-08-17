from interview_workbook.graphs.bellman_ford import (
    bellman_ford,
    detect_negative_cycle,
    reconstruct_path,
)


def test_bellman_ford_no_negative_cycle():
    # Small graph with negative edges but no negative cycle
    # 0 -> 1 (6), 0 -> 3 (7), 1 -> 2 (5), 1 -> 4 (-4), 2 -> 1 (-2), 3 -> 2 (-3), 4 -> 0 (2), 4 -> 2 (7)
    n = 5
    edges = [
        (0, 1, 6),
        (0, 3, 7),
        (1, 2, 5),
        (1, 4, -4),
        (2, 1, -2),
        (3, 2, -3),
        (4, 0, 2),
        (4, 2, 7),
    ]
    source = 0
    dist, parent = bellman_ford(n, edges, source)

    # Distances known from CLRS example
    assert dist[0] == 0
    # 0->3->2->1 total: 7 + (-3) + (-2) = 2
    assert dist[1] == 2
    # 0->3->2 total: 7 + (-3) = 4
    assert dist[2] == 4
    # 0->3 total: 7
    assert dist[3] == 7

    # Reconstruct a path (0 -> 1): should be defined and start/end correct
    path_0_to_1 = reconstruct_path(parent, 1)
    assert path_0_to_1[0] == 0 and path_0_to_1[-1] == 1


def test_bellman_ford_negative_cycle_marking_and_reconstruct_path_blocks():
    # Construct a graph where a negative cycle is reachable from source
    # 0->1 (1), 1->2 (-2), 2->1 (-2) => cycle with sum -4 reachable from 0
    n = 3
    edges = [
        (0, 1, 1),
        (1, 2, -2),
        (2, 1, -2),
    ]
    dist, parent = bellman_ford(n, edges, 0)

    # parent marked -2 denotes affected by negative cycle
    # At least one vertex on or reachable from the cycle should be flagged
    assert any(p == -2 for p in parent[1:])

    # reconstruct_path should return [] for affected target
    for t in range(n):
        if parent[t] == -2:
            assert reconstruct_path(parent, t) == []


def test_detect_negative_cycle_returns_cycle():
    # 1 -> 2 -> 3 -> 1 with negative sum
    n = 4
    edges = [
        (0, 1, 5),
        (1, 2, -2),
        (2, 3, -2),
        (3, 1, -2),
    ]
    cycle = detect_negative_cycle(n, edges)
    assert cycle is not None
    # All vertices in the reported cycle are between 0..n-1 and include at least one of {1,2,3}
    assert all(0 <= v < n for v in cycle)
    assert any(v in {1, 2, 3} for v in cycle)
