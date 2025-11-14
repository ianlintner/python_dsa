"""
Robotics navigation algorithm visualization.

Generates animation frames for various robotics navigation algorithms.
"""

from __future__ import annotations

import random
from typing import Any

from interview_workbook.robotics import (
    bug_algorithms,
    pledge_algorithm,
    potential_fields,
    rrt,
    utils,
)

Coord = tuple[int, int]


def generate_grid(
    rows: int = 15,
    cols: int = 20,
    density: float = 0.2,
    seed: int | None = None,
) -> dict[str, Any]:
    """
    Generate a grid with random obstacles.
    - rows x cols grid
    - Each cell becomes an obstacle with probability 'density'
    - Start at (1,1), Goal at (cols-2, rows-2)
    """
    if seed is not None:
        random.seed(seed)

    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Add random obstacles
    for r in range(rows):
        for c in range(cols):
            if random.random() < density:
                grid[r][c] = 1

    # Ensure start and goal are free
    start = (1, 1)
    goal = (cols - 2, rows - 2)
    grid[start[1]][start[0]] = 0
    grid[goal[1]][goal[0]] = 0

    # Clear immediate neighbors of start
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x, y = start[0] + dx, start[1] + dy
            if 0 <= x < cols and 0 <= y < rows:
                grid[y][x] = 0

    return {
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "start": start,
        "goal": goal,
    }


def _frame(
    robot_pos: Coord | None,
    robot_dir: str | None,
    path: list[Coord],
    visited: set[Coord],
    op: str,
) -> dict[str, Any]:
    """Create a visualization frame."""
    return {
        "robot": list(robot_pos) if robot_pos else None,
        "direction": robot_dir,
        "path": [list(p) for p in path],
        "visited": [list(v) for v in sorted(visited)],
        "op": op,
    }


def wall_following_frames(
    grid_data: dict[str, Any], use_left_hand: bool = True, max_steps: int = 500
) -> list[dict[str, Any]]:
    """Generate frames for wall-following algorithm."""
    grid_world = utils.GridWorld(grid_data["grid"])
    start = tuple(grid_data["start"])
    goal = tuple(grid_data["goal"])

    frames: list[dict[str, Any]] = []

    # Track execution step by step
    robot = utils.RobotState(start[0], start[1], utils.Direction.NORTH)
    path = [start]
    visited: set[Coord] = {start}

    frames.append(_frame(start, "NORTH", path, visited, "init"))

    for _ in range(max_steps):
        if (robot.x, robot.y) == goal:
            frames.append(_frame((robot.x, robot.y), robot.direction.name, path, visited, "goal"))
            break

        if use_left_hand:
            # Left-hand rule
            robot.turn_left()
            next_pos = robot.move_forward()

            if grid_world.is_free(*next_pos):
                robot.apply_move()
            else:
                robot.turn_right()
                next_pos = robot.move_forward()
                if grid_world.is_free(*next_pos):
                    robot.apply_move()
                else:
                    robot.turn_right()
                    next_pos = robot.move_forward()
                    if grid_world.is_free(*next_pos):
                        robot.apply_move()
                    else:
                        robot.turn_right()
        else:
            # Right-hand rule
            robot.turn_right()
            next_pos = robot.move_forward()

            if grid_world.is_free(*next_pos):
                robot.apply_move()
            else:
                robot.turn_left()
                next_pos = robot.move_forward()
                if grid_world.is_free(*next_pos):
                    robot.apply_move()
                else:
                    robot.turn_left()
                    next_pos = robot.move_forward()
                    if grid_world.is_free(*next_pos):
                        robot.apply_move()
                    else:
                        robot.turn_left()

        current_pos = (robot.x, robot.y)
        if current_pos not in visited:
            visited.add(current_pos)
        path.append(current_pos)

        frames.append(_frame(current_pos, robot.direction.name, path, visited, "move"))

    return frames


def bug1_frames(grid_data: dict[str, Any], max_steps: int = 500) -> list[dict[str, Any]]:
    """Generate frames for Bug1 algorithm."""
    grid_world = utils.GridWorld(grid_data["grid"])
    start = tuple(grid_data["start"])
    goal = tuple(grid_data["goal"])

    frames: list[dict[str, Any]] = []
    path = [start]
    visited: set[Coord] = {start}

    frames.append(_frame(start, None, path, visited, "init"))

    # Run Bug1 algorithm - simplified visualization
    full_path = bug_algorithms.bug1_navigate(grid_world, start, goal, max_steps=max_steps)

    if full_path:
        for i, pos in enumerate(full_path[1:], 1):
            visited.add(pos)
            frames.append(_frame(pos, None, path[:i], visited, "move"))
        frames.append(_frame(goal, None, full_path, visited, "goal"))

    return frames


def rrt_frames(grid_data: dict[str, Any], max_iter: int = 300) -> list[dict[str, Any]]:
    """Generate frames for RRT algorithm."""
    grid = grid_data["grid"]
    start = tuple(grid_data["start"])
    goal = tuple(grid_data["goal"])

    frames: list[dict[str, Any]] = []
    frames.append(_frame(start, None, [start], {start}, "init"))

    # Run RRT
    path = rrt.rrt_plan(
        grid, start, goal, max_iterations=max_iter, step_size=1.5, goal_sample_rate=0.15
    )

    if path:
        visited = set(path)
        for i, pos in enumerate(path):
            frames.append(_frame(pos, None, path[: i + 1], visited, "explore"))
        frames.append(_frame(goal, None, path, visited, "goal"))
    else:
        frames.append(_frame(None, None, [start], {start}, "no-path"))

    return frames


def potential_field_frames(grid_data: dict[str, Any], max_steps: int = 200) -> list[dict[str, Any]]:
    """Generate frames for potential field algorithm."""
    grid = grid_data["grid"]
    start = tuple(grid_data["start"])
    goal = tuple(grid_data["goal"])

    frames: list[dict[str, Any]] = []
    frames.append(_frame(start, None, [start], {start}, "init"))

    # Run potential field
    path = potential_fields.potential_field_navigate(
        grid,
        start,
        goal,
        attractive_gain=2.0,
        repulsive_gain=80.0,
        influence_distance=3.0,
        max_steps=max_steps,
    )

    if path:
        visited = set(path)
        for i, pos in enumerate(path):
            frames.append(_frame(pos, None, path[: i + 1], visited, "move"))
        frames.append(_frame(goal, None, path, visited, "goal"))
    else:
        frames.append(_frame(None, None, [start], {start}, "stuck"))

    return frames


def pledge_frames(grid_data: dict[str, Any], max_steps: int = 500) -> list[dict[str, Any]]:
    """Generate frames for Pledge algorithm."""
    grid_world = utils.GridWorld(grid_data["grid"])
    start = tuple(grid_data["start"])
    goal = tuple(grid_data["goal"])

    frames: list[dict[str, Any]] = []
    frames.append(_frame(start, None, [start], {start}, "init"))

    # Run Pledge algorithm
    path = pledge_algorithm.pledge_navigate(grid_world, start, goal, max_steps=max_steps)

    if path:
        visited = set(path)
        for i, pos in enumerate(path):
            frames.append(_frame(pos, None, path[: i + 1], visited, "move"))
        frames.append(_frame(goal, None, path, visited, "goal"))
    else:
        frames.append(_frame(None, None, [start], {start}, "no-path"))

    return frames


ALGORITHMS = {
    "wall_left": {
        "name": "Wall Following (Left-Hand)",
        "frames": lambda g, **kw: wall_following_frames(g, use_left_hand=True, **kw),
    },
    "wall_right": {
        "name": "Wall Following (Right-Hand)",
        "frames": lambda g, **kw: wall_following_frames(g, use_left_hand=False, **kw),
    },
    "bug1": {"name": "Bug1 Algorithm", "frames": bug1_frames},
    "pledge": {"name": "Pledge Algorithm", "frames": pledge_frames},
    "potential": {"name": "Potential Fields", "frames": potential_field_frames},
    "rrt": {"name": "RRT (Rapidly-exploring Random Tree)", "frames": rrt_frames},
}


def visualize(
    algo_key: str,
    rows: int = 15,
    cols: int = 20,
    density: float = 0.2,
    seed: int | None = None,
) -> dict[str, Any]:
    """Generate visualization data for a robotics algorithm."""
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")

    grid_data = generate_grid(rows=rows, cols=cols, density=density, seed=seed)
    frames = algo["frames"](grid_data)

    return {
        "algorithm": algo_key,
        "name": algo["name"],
        "grid": grid_data,
        "frames": frames,
    }
