"""
RRT (Rapidly-exploring Random Tree) path planning.

RRT is a sampling-based path planning algorithm that builds a tree of
feasible paths by randomly sampling the configuration space. It's widely
used in robotics for high-dimensional planning problems.

Time complexity: O(n) where n is number of samples
Space complexity: O(n) for storing the tree
"""

from __future__ import annotations

import random


def rrt_plan(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
    max_iterations: int = 1000,
    step_size: float = 1.0,
    goal_sample_rate: float = 0.1,
) -> list[tuple[int, int]] | None:
    """
    RRT (Rapidly-exploring Random Tree) path planner.

    Builds a tree by repeatedly:
    1. Sample random point in space (or goal with probability)
    2. Find nearest node in tree
    3. Extend tree toward sample
    4. Check if goal reached

    Time: O(iterations * tree_size) for nearest neighbor search
    Space: O(tree_size) for storing nodes

    Args:
        grid: Environment (0=free, 1=obstacle)
        start: Starting position
        goal: Goal position
        max_iterations: Maximum sampling iterations
        step_size: Maximum distance to extend tree per iteration
        goal_sample_rate: Probability of sampling goal (vs random point)

    Returns:
        Path from start to goal, or None if not found

    Advantages:
    - Probabilistically complete
    - Works well in high-dimensional spaces
    - Can handle complex obstacles

    Disadvantages:
    - Not optimal (path quality depends on samples)
    - Requires tuning (step_size, iterations)
    - Memory grows with iterations
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def is_valid(x: int, y: int) -> bool:
        ix, iy = int(round(x)), int(round(y))
        return 0 <= ix < cols and 0 <= iy < rows and grid[iy][ix] == 0

    def collision_free(p1: tuple[float, float], p2: tuple[float, float]) -> bool:
        """Check if path from p1 to p2 is collision-free."""
        x1, y1 = p1
        x2, y2 = p2
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        steps = max(int(dist * 2), 1)

        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            if not is_valid(x, y):
                return False
        return True

    if not is_valid(*start) or not is_valid(*goal):
        return None

    # Tree: each node stores (position, parent_index)
    tree = [(start, -1)]
    goal_f = (float(goal[0]), float(goal[1]))

    for _ in range(max_iterations):
        # Sample random point (bias toward goal)
        if random.random() < goal_sample_rate:
            sample = goal_f
        else:
            sample = (random.uniform(0, cols - 1), random.uniform(0, rows - 1))

        # Find nearest node in tree
        nearest_idx = 0
        min_dist = float("inf")
        for idx, (pos, _) in enumerate(tree):
            dist = (pos[0] - sample[0]) ** 2 + (pos[1] - sample[1]) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_idx = idx

        nearest_pos = tree[nearest_idx][0]

        # Extend toward sample
        dx = sample[0] - nearest_pos[0]
        dy = sample[1] - nearest_pos[1]
        dist = (dx**2 + dy**2) ** 0.5

        if dist < 0.01:
            continue

        # Limit extension to step_size
        if dist > step_size:
            dx = dx / dist * step_size
            dy = dy / dist * step_size

        new_pos = (nearest_pos[0] + dx, nearest_pos[1] + dy)

        # Check collision
        if collision_free(nearest_pos, new_pos):
            tree.append((new_pos, nearest_idx))

            # Check if goal reached
            goal_dist = ((new_pos[0] - goal_f[0]) ** 2 + (new_pos[1] - goal_f[1]) ** 2) ** 0.5
            if goal_dist < step_size and collision_free(new_pos, goal_f):
                # Goal reached! Reconstruct path
                tree.append((goal_f, len(tree) - 1))
                return _reconstruct_path(tree)

    return None  # Goal not reached


def _reconstruct_path(tree: list[tuple[tuple[float, float], int]]) -> list[tuple[int, int]]:
    """Reconstruct path from tree."""
    path = []
    idx = len(tree) - 1

    while idx != -1:
        pos, parent_idx = tree[idx]
        path.append((int(round(pos[0])), int(round(pos[1]))))
        idx = parent_idx

    path.reverse()
    return path


def demo():
    """Demo RRT path planning."""
    print("RRT (Rapidly-exploring Random Tree) Demo")
    print("=" * 50)

    random.seed(42)  # For reproducible results

    # Create environment with obstacles
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    start = (1, 1)
    goal = (8, 5)

    print("Grid (0=free, 1=obstacle):")
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print(f"\nStart: {start}, Goal: {goal}\n")

    # Try different parameter settings
    configs = [
        (500, 1.0, 0.1, "Standard"),
        (500, 2.0, 0.1, "Larger steps"),
        (500, 1.0, 0.3, "Higher goal bias"),
        (1000, 1.0, 0.1, "More iterations"),
    ]

    for max_iter, step, goal_rate, name in configs:
        print(f"{name} (iter={max_iter}, step={step}, goal_bias={goal_rate}):")
        random.seed(42)  # Same seed for fair comparison
        path = rrt_plan(maze, start, goal, max_iter, step, goal_rate)

        if path:
            print(f"  Success! Path length: {len(path)} waypoints")

            # Show path on grid
            path_set = set(path)
            print("  Path visualization:")
            for y, row in enumerate(maze):
                line = []
                for x, cell in enumerate(row):
                    if (x, y) == start:
                        line.append("S")
                    elif (x, y) == goal:
                        line.append("G")
                    elif cell == 1:
                        line.append("#")
                    elif (x, y) in path_set:
                        line.append("*")
                    else:
                        line.append(".")
                print("  " + " ".join(line))
        else:
            print("  Failed to find path")
        print()

    print("RRT Key Insights:")
    print("- Samples random points and grows tree toward them")
    print("- Probabilistically complete (will find path eventually)")
    print("- Not optimal: path quality depends on sampling")
    print("- Good for high-dimensional configuration spaces")
    print("- Parameters affect performance:")
    print("  * step_size: larger = faster exploration, may miss narrow passages")
    print("  * goal_sample_rate: higher = faster toward goal, less exploration")
    print("  * max_iterations: more = higher success rate, slower")
    print("- Variants: RRT*, RRT-Connect improve performance")


if __name__ == "__main__":
    demo()
