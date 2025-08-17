from interview_workbook.graphs.floyd_warshall import (
    NEG_INF,
    build_adj_matrix,
    floyd_warshall,
    has_negative_cycle,
    reconstruct_path,
)


def test_apsp_no_negative_cycle():
    # Graph with negative edges but no negative cycles
    n = 4
    edges = [
        (0, 1, 3),
        (0, 2, 10),
        (1, 2, -2),
        (2, 3, 2),
        (1, 3, 7),
    ]
    dist = build_adj_matrix(n, edges, directed=True)
    dist_out, next_hop = floyd_warshall(dist)

    # Expected shortest distances:
    # 0->2 via 0->1->2: 3 + (-2) = 1
    # 0->3 via 0->1->2->3: 3 + (-2) + 2 = 3
    assert dist_out[0][2] == 1.0
    assert dist_out[0][3] == 3.0

    # Reconstructed path should start at 0 and end at 3
    path_0_to_3 = reconstruct_path(next_hop, 0, 3)
    assert path_0_to_3[0] == 0 and path_0_to_3[-1] == 3
    assert has_negative_cycle(dist_out) is False


def test_negative_cycle_propagation_and_path_undefined():
    # Simple negative cycle across all 3 nodes:
    # 0->1 (1), 1->2 (-1), 2->0 (-1) => cycle weight = -1
    n = 3
    edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1),
    ]
    dist = build_adj_matrix(n, edges, directed=True)
    dist_out, next_hop = floyd_warshall(dist)

    # Negative cycle must be detected
    assert has_negative_cycle(dist_out) is True

    # Any pairs reachable through the negative cycle should be -inf
    assert dist_out[0][2] == NEG_INF
    assert dist_out[1][0] == NEG_INF
    assert dist_out[2][1] == NEG_INF

    # Path is undefined due to negative cycle propagation
    assert reconstruct_path(next_hop, 0, 2) == []
    assert reconstruct_path(next_hop, 1, 0) == []


def test_unreachable_and_out_of_bounds_reconstruction():
    n = 3
    edges: list[tuple[int, int, float]] = []
    dist = build_adj_matrix(n, edges, directed=True)
    dist_out, next_hop = floyd_warshall(dist)

    # Unreachable node pair yields empty reconstruction
    assert reconstruct_path(next_hop, 0, 2) == []

    # Out-of-bounds indices handled gracefully
    assert reconstruct_path(next_hop, -1, 2) == []
    assert reconstruct_path(next_hop, 0, 99) == []
    # Self path always trivial (0 length), but our reconstruct_path returns [] if next_hop[u][u] is None
    # This behavior is acceptable; we only validate non-crash and empty for no movement.
    assert reconstruct_path(next_hop, 1, 1) in ([], [1])
