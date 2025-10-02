import heapq
from collections.abc import Callable


def a_star(
    start: int,
    goal: int,
    neighbors: Callable[[int], list[tuple[int, float]]],
    heuristic: Callable[[int], float],
) -> tuple[float, list[int]]:
    """
    A* search on a generic graph.

    Args:
        start: start node id
        goal: goal node id
        neighbors: function mapping node -> list of (neighbor, edge_cost)
        heuristic: admissible heuristic h(n) estimating cost(n -> goal)
                   Must be consistent (monotone) for optimality guarantees on graphs with varying costs.

    Returns:
        (total_cost, path_nodes). If unreachable, returns (float('inf'), []).

    Time: O((V + E) log V) with a binary heap (typical)
    Space: O(V)

    Notes:
    - For heuristic:
        * h(n) = 0 reduces to Dijkstra's algorithm
        * h(n) must never overestimate true remaining cost (admissible)
        * Consistency: h(u) <= w(u,v) + h(v) for all edges (u,v)
    """
    open_heap: list[tuple[float, int]] = []  # (f = g+h, node)
    g_score: dict[int, float] = {start: 0.0}
    parent: dict[int, int | None] = {start: None}

    f_start = heuristic(start)
    heapq.heappush(open_heap, (f_start, start))

    in_open: dict[int, float] = {start: f_start}  # node -> best f seen in heap

    while open_heap:
        f, u = heapq.heappop(open_heap)
        # If this popped entry is stale, skip
        if in_open.get(u, float("inf")) < f:
            continue

        if u == goal:
            # Reconstruct
            path: list[int] = []
            cur: int | None = u
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return g_score[u], path

        for v, w in neighbors(u):
            tentative_g = g_score[u] + w
            if tentative_g < g_score.get(v, float("inf")):
                g_score[v] = tentative_g
                parent[v] = u
                f_v = tentative_g + heuristic(v)
                in_open[v] = f_v
                heapq.heappush(open_heap, (f_v, v))

    return float("inf"), []


# Grid A* convenience implementation (4-directional)
Grid = list[list[int]]
Coord = tuple[int, int]


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_grid(
    grid: Grid,
    start: Coord,
    goal: Coord,
    passable: Callable[[int], bool] = lambda cell: cell == 0,
    diagonal: bool = False,
) -> tuple[float, list[Coord]]:
    """
    A* on a 2D grid.
    - grid: 0 = free cell by default, non-zero = blocked (configurable via 'passable')
    - movement cost: 1 per step (orthogonal). If diagonal=True, diagonal moves cost sqrt(2).

    Returns:
        (total_cost, path as list of coordinates). [] if unreachable.

    Time: O(N log N) where N = rows*cols in worst-case
    Space: O(N)
    """
    import math

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    if rows == 0 or cols == 0:
        return float("inf"), []

    # Directions
    if diagonal:
        dirs = [
            (1, 0, 1.0),
            (-1, 0, 1.0),
            (0, 1, 1.0),
            (0, -1, 1.0),
            (1, 1, math.sqrt(2)),
            (1, -1, math.sqrt(2)),
            (-1, 1, math.sqrt(2)),
            (-1, -1, math.sqrt(2)),
        ]

        def h(p: Coord) -> float:
            # Octile distance
            dx = abs(p[0] - goal[0])
            dy = abs(p[1] - goal[1])
            return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

    else:
        dirs = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0)]

        def h(p: Coord) -> float:
            return float(manhattan(p, goal))

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    start_r, start_c = start
    goal_r, goal_c = goal
    if not in_bounds(*start) or not in_bounds(*goal):
        return float("inf"), []
    if not passable(grid[start_r][start_c]) or not passable(grid[goal_r][goal_c]):
        return float("inf"), []

    open_heap: list[tuple[float, Coord]] = []
    g_score: dict[Coord, float] = {start: 0.0}
    parent: dict[Coord, Coord | None] = {start: None}

    f_start = h(start)
    heapq.heappush(open_heap, (f_start, start))
    in_open: dict[Coord, float] = {start: f_start}

    while open_heap:
        f, u = heapq.heappop(open_heap)
        if in_open.get(u, float("inf")) < f:
            continue

        if u == goal:
            # Reconstruct path
            path: list[Coord] = []
            cur: Coord | None = u
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return g_score[u], path

        ur, uc = u
        for dr, dc, step_cost in dirs:
            vr, vc = ur + dr, uc + dc
            if not in_bounds(vr, vc) or not passable(grid[vr][vc]):
                continue
            v = (vr, vc)
            tentative_g = g_score[u] + step_cost
            if tentative_g < g_score.get(v, float("inf")):
                g_score[v] = tentative_g
                parent[v] = u
                f_v = tentative_g + h(v)
                in_open[v] = f_v
                heapq.heappush(open_heap, (f_v, v))

    return float("inf"), []


def demo():
    print("A* Search Demo")
    print("=" * 40)

    # Generic graph example (directed)
    print("Generic Graph A* (h=0 => Dijkstra):")
    graph = {0: [(1, 2), (2, 5)], 1: [(2, 1), (3, 3)], 2: [(3, 1)], 3: []}
    start, goal = 0, 3

    def neighbors(u: int) -> list[tuple[int, float]]:
        return graph.get(u, [])

    def h_zero(_: int) -> float:
        return 0.0  # reduces to Dijkstra

    cost, path = a_star(start, goal, neighbors, h_zero)
    print(f"Path {start}->{goal}: cost={cost}, path={path}")
    print()

    # Grid example
    print("Grid A* (Manhattan heuristic):")
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],  # 1 = wall
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (3, 4)
    cost, path = a_star_grid(
        grid, start, goal, passable=lambda x: x == 0, diagonal=False
    )
    print(f"Path {start}->{goal}: cost={cost:.2f}, path={path}")
    print()

    print("Notes & Interview Tips:")
    print("  - Heuristic must be admissible and ideally consistent for optimality.")
    print("  - On grids, Manhattan (4-dir) or Octile (8-dir) are common heuristics.")
    print(
        "  - If h=0, A* becomes Dijkstra; if h overestimates, may be fast but not optimal."
    )
    print("  - Practical uses: pathfinding in games, routing, planning.")


if __name__ == "__main__":
    demo()
