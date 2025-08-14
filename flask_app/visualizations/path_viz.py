from __future__ import annotations

import heapq
import random
from typing import Any, Dict, List, Optional, Tuple


Coord = Tuple[int, int]


def generate_grid(
    rows: int = 20,
    cols: int = 30,
    density: float = 0.25,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a grid with random walls.
    - rows x cols grid
    - Each cell becomes a wall with probability 'density'
    - Start at (0,0), Goal at (rows-1, cols-1) (never walls)
    """
    rng = random.Random(seed)
    walls = set()
    for r in range(rows):
        for c in range(cols):
            if rng.random() < density:
                walls.add((r, c))
    start = (0, 0)
    goal = (rows - 1, cols - 1)
    walls.discard(start)
    walls.discard(goal)
    return {
        "rows": rows,
        "cols": cols,
        "walls": sorted(list(walls)),
        "start": start,
        "goal": goal,
    }


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(r: int, c: int, rows: int, cols: int) -> List[Coord]:
    out: List[Coord] = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            out.append((nr, nc))
    return out


def _frame(
    current: Optional[Coord],
    open_list: List[Coord],
    closed: List[Coord],
    path: List[Coord],
    op: str,
) -> Dict[str, Any]:
    return {
        "current": list(current) if current is not None else None,
        "open": [list(x) for x in open_list],
        "closed": [list(x) for x in closed],
        "path": [list(x) for x in path],
        "op": op,
    }


def _reconstruct_path(came_from: Dict[Coord, Coord], current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star_frames(grid: Dict[str, Any], max_steps: int = 50000) -> List[Dict[str, Any]]:
    rows, cols = grid["rows"], grid["cols"]
    walls = set(map(tuple, grid["walls"]))
    start: Coord = tuple(grid["start"])  # type: ignore
    goal: Coord = tuple(grid["goal"])  # type: ignore

    open_heap: List[Tuple[int, int, Coord]] = []
    tie = 0
    heapq.heappush(open_heap, (manhattan(start, goal), tie, start))
    open_set = {start}
    closed_set: set[Coord] = set()

    came_from: Dict[Coord, Coord] = {}
    g_score: Dict[Coord, int] = {start: 0}

    frames: List[Dict[str, Any]] = [_frame(None, list(open_set), list(closed_set), [], "init")]

    while open_heap and len(frames) < max_steps:
        _, _, current = heapq.heappop(open_heap)
        if current not in open_set:
            continue
        open_set.remove(current)
        frames.append(_frame(current, list(open_set), list(closed_set), [], "pop"))

        if current == goal:
            path = _reconstruct_path(came_from, current)
            frames.append(_frame(current, list(open_set), list(closed_set), path, "done"))
            return frames

        closed_set.add(current)
        frames.append(_frame(current, list(open_set), list(closed_set), [], "visit"))

        for nbr in neighbors(*current, rows, cols):
            if nbr in walls or nbr in closed_set:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nbr, 10**9):
                came_from[nbr] = current
                g_score[nbr] = tentative_g
                f = tentative_g + manhattan(nbr, goal)
                tie += 1
                heapq.heappush(open_heap, (f, tie, nbr))
                open_set.add(nbr)
                p = _reconstruct_path(came_from, current)
                frames.append(_frame(nbr, list(open_set), list(closed_set), p, "push/update"))

    # No path found
    frames.append(_frame(None, list(open_set), list(closed_set), [], "no-path"))
    return frames


def dijkstra_frames(grid: Dict[str, Any], max_steps: int = 50000) -> List[Dict[str, Any]]:
    rows, cols = grid["rows"], grid["cols"]
    walls = set(map(tuple, grid["walls"]))
    start: Coord = tuple(grid["start"])  # type: ignore
    goal: Coord = tuple(grid["goal"])  # type: ignore

    open_heap: List[Tuple[int, int, Coord]] = []
    tie = 0
    heapq.heappush(open_heap, (0, tie, start))
    open_set = {start}
    closed_set: set[Coord] = set()

    came_from: Dict[Coord, Coord] = {}
    dist: Dict[Coord, int] = {start: 0}

    frames: List[Dict[str, Any]] = [_frame(None, list(open_set), list(closed_set), [], "init")]

    while open_heap and len(frames) < max_steps:
        _, _, current = heapq.heappop(open_heap)
        if current not in open_set:
            continue
        open_set.remove(current)
        frames.append(_frame(current, list(open_set), list(closed_set), [], "pop"))

        if current == goal:
            path = _reconstruct_path(came_from, current)
            frames.append(_frame(current, list(open_set), list(closed_set), path, "done"))
            return frames

        closed_set.add(current)
        frames.append(_frame(current, list(open_set), list(closed_set), [], "visit"))

        for nbr in neighbors(*current, rows, cols):
            if nbr in walls or nbr in closed_set:
                continue
            nd = dist[current] + 1
            if nd < dist.get(nbr, 10**9):
                dist[nbr] = nd
                came_from[nbr] = current
                tie += 1
                heapq.heappush(open_heap, (nd, tie, nbr))
                open_set.add(nbr)
                p = _reconstruct_path(came_from, current)
                frames.append(_frame(nbr, list(open_set), list(closed_set), p, "push/update"))

    frames.append(_frame(None, list(open_set), list(closed_set), [], "no-path"))
    return frames


ALGORITHMS = {
    "astar": {"name": "A* Search (Manhattan Heuristic)", "frames": a_star_frames},
    "dijkstra": {"name": "Dijkstra's Algorithm (Uniform-Cost)", "frames": dijkstra_frames},
}


def visualize(
    algo_key: str,
    rows: int = 20,
    cols: int = 30,
    density: float = 0.25,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    grid = generate_grid(rows=rows, cols=cols, density=density, seed=seed)
    frames = algo["frames"](grid)
    return {"algorithm": algo_key, "name": algo["name"], "grid": grid, "frames": frames}
