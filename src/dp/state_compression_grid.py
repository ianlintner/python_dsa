from collections import deque
from typing import Callable, Deque, Dict, List, Optional, Set, Tuple

Grid = List[List[str]]
Coord = Tuple[int, int]


def shortest_path_collect_all(
    grid: Grid, passable: Callable[[str], bool] = lambda c: c != "#"
) -> int:
    """
    State-compression BFS on a grid: shortest steps to collect all targets 'T' starting from 'S'.
    - Cells:
        'S' = start (exactly one)
        'T' = targets (zero or more)
        '#' = wall (impassable)
        '.' or other chars = passable by default (configurable via passable)
    Movement: 4-directional, cost 1 per move.

    Returns:
        Minimum steps to collect all targets; -1 if impossible.

    Technique:
      - Encode state as (r, c, mask) where mask is a bitmask of collected targets.
      - BFS over state space; first time we reach mask == all_collected, we have the shortest path.

    Complexity:
      Let N = rows*cols, K = number of targets. States are O(N * 2^K). Each processed once -> O(N * 2^K).
    """
    if not grid or not grid[0]:
        return -1
    R, C = len(grid), len(grid[0])

    # Collect positions of start and targets
    start: Optional[Coord] = None
    targets: List[Coord] = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "T":
                targets.append((r, c))
    if start is None:
        return -1
    K = len(targets)
    target_index: Dict[Coord, int] = {pos: i for i, pos in enumerate(targets)}
    ALL = (1 << K) - 1

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < R and 0 <= c < C

    # BFS
    q: Deque[Tuple[int, int, int]] = deque()
    dist: Dict[Tuple[int, int, int], int] = {}

    sr, sc = start
    start_mask = 0
    if (sr, sc) in target_index:
        start_mask = 1 << target_index[(sr, sc)]
    q.append((sr, sc, start_mask))
    dist[(sr, sc, start_mask)] = 0

    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        r, c, mask = q.popleft()
        d = dist[(r, c, mask)]
        if mask == ALL:
            return d
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not in_bounds(nr, nc) or not passable(grid[nr][nc]):
                continue
            nmask = mask
            if (nr, nc) in target_index:
                nmask |= 1 << target_index[(nr, nc)]
            state = (nr, nc, nmask)
            if state not in dist:
                dist[state] = d + 1
                q.append(state)
    return -1


def demo():
    print("State Compression on Grid (BFS over (r,c,mask)) Demo")
    print("=" * 55)

    grid = [
        list("S..#.."),
        list("..#T.."),
        list("..#..."),
        list("..T#.."),
        list("......"),
    ]
    steps = shortest_path_collect_all(grid)
    print("Grid:")
    for row in grid:
        print("  " + "".join(row))
    print(f"\nShortest steps to collect all T from S: {steps}")
    print()
    print("Notes & Interview Tips:")
    print("  - Use (r,c,mask) to encode collected items or visited subsets.")
    print("  - Works for keys/locks problems (e.g., 'Shortest Path to Get All Keys').")
    print("  - Complexity grows with 2^K; keep K modest (<= 10-12 typically).")


if __name__ == "__main__":
    demo()
