from typing import List, Tuple, Dict

"""
Bitmask DP (Held-Karp) for Traveling Salesman Problem (TSP)

Problem:
  Given a complete weighted graph with n nodes (0..n-1), find a minimum-cost Hamiltonian
  cycle starting and ending at 'start' that visits each node exactly once.

Complexity:
  Time:  O(n^2 * 2^n)
  Space: O(n * 2^n)

Notes:
  - Works for n up to ~20 with optimizations; practically ~15-18 in Python.
  - distances[i][j] should represent cost from i to j; ensure triangle inequality if desired.
  - If graph is not complete, set large costs for missing edges.
"""

INF = 10**18


def held_karp_tsp(distances: List[List[int]], start: int = 0) -> Tuple[int, List[int]]:
    """
    Held-Karp dynamic programming solution to the TSP.

    Args:
        distances: nxn matrix of non-negative edge weights (complete graph assumed).
        start: starting node (also ending node for the tour).

    Returns:
        (min_cost, path_including_return_to_start)
        If no tour exists, returns (INF, []).
    """
    n = len(distances)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [start, start]

    # dp[mask][j] = min cost to start at 'start', visit set 'mask' (including 'start' and 'j'), and end at 'j'
    # mask is a bitmask over nodes {0..n-1}
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    start_mask = 1 << start
    dp[start_mask][start] = 0

    for mask in range(size):
        if not (mask & start_mask):
            continue  # must contain start
        # Skip masks with a single bit if not start
        for j in range(n):
            if not (mask & (1 << j)):
                continue  # j not in mask
            if dp[mask][j] == INF:
                continue
            # Try to extend to next node k not yet visited
            for k in range(n):
                if mask & (1 << k):
                    continue
                nxt = mask | (1 << k)
                new_cost = dp[mask][j] + distances[j][k]
                if new_cost < dp[nxt][k]:
                    dp[nxt][k] = new_cost
                    parent[nxt][k] = j

    full_mask = (1 << n) - 1
    best_cost = INF
    best_end = -1
    # Close the tour back to start
    for j in range(n):
        if j == start:
            continue
        cost = dp[full_mask][j] + distances[j][start]
        if cost < best_cost:
            best_cost = cost
            best_end = j

    if best_cost >= INF:
        return INF, []

    # Reconstruct path: ... -> best_end -> start
    path = [start]
    mask = full_mask
    j = best_end
    tour_nodes = []
    while j != -1:
        tour_nodes.append(j)
        pj = parent[mask][j]
        mask ^= 1 << j
        j = pj

    tour_nodes.reverse()
    # Ensure starts with start; parent chain ends at start
    if tour_nodes and tour_nodes[0] != start:
        tour_nodes = [start] + tour_nodes
    # Append return to start to complete cycle representation
    tour_nodes.append(start)
    return best_cost, tour_nodes


def demo():
    print("Bitmask DP (Held-Karp) TSP Demo")
    print("=" * 40)

    # Example: 4-city TSP (complete graph)
    # Distances matrix (symmetric, triangle inequality holds)
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    start = 0
    cost, path = held_karp_tsp(distances, start=start)
    print("Distances:")
    for row in distances:
        print(" ", row)
    print(f"\nOptimal tour cost: {cost}")
    print(f"Tour path: {path}")
    print()

    # A slightly larger example (asymmetric costs)
    distances2 = [
        [0, 29, 20, 21, 16],
        [29, 0, 15, 17, 28],
        [20, 15, 0, 28, 39],
        [21, 17, 28, 0, 13],
        [16, 28, 39, 13, 0],
    ]
    cost2, path2 = held_karp_tsp(distances2, start=0)
    print("Asymmetric distances example:")
    print(f"Optimal tour cost: {cost2}")
    print(f"Tour path: {path2}")

    print("\nNotes & Interview Tips:")
    print(
        "  - TSP via Held-Karp is a classic bitmask DP: dp[mask][j] stores partial tour ending at j."
    )
    print("  - Complexity O(n^2 * 2^n) limits n to ~20 in optimized languages; smaller in Python.")
    print("  - For metric TSP, approximation algorithms (e.g., Christofides) are used at scale.")


if __name__ == "__main__":
    demo()
