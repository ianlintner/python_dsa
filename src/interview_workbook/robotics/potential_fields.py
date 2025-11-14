"""
Potential field navigation for robots.

Potential fields create artificial attractive and repulsive forces to guide
robots to goals while avoiding obstacles. This is a reactive planning method
commonly used in mobile robotics.

Time complexity: O(steps * obstacles) per iteration
Space complexity: O(1) for force calculations
"""

from __future__ import annotations

import math


def potential_field_navigate(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
    attractive_gain: float = 1.0,
    repulsive_gain: float = 100.0,
    influence_distance: float = 3.0,
    max_steps: int = 500,
) -> list[tuple[int, int]] | None:
    """
    Navigate using artificial potential fields.

    The robot is attracted to the goal and repelled by obstacles.
    Total force = Attractive force + Repulsive forces

    Time: O(steps * obstacles) where obstacles are within influence_distance
    Space: O(1) for force calculations

    Args:
        grid: Environment (0=free, 1=obstacle)
        start: Starting position
        goal: Goal position
        attractive_gain: Weight for attractive force (higher = stronger pull to goal)
        repulsive_gain: Weight for repulsive force (higher = stronger obstacle avoidance)
        influence_distance: Max distance for obstacle repulsion
        max_steps: Maximum navigation steps

    Returns:
        Path from start to goal, or None if stuck

    Advantages:
    - Simple and reactive
    - Smooth paths in open spaces
    - Real-time capable

    Disadvantages:
    - Can get stuck in local minima
    - No completeness guarantee
    - Oscillations possible near obstacles
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < cols and 0 <= y < rows and grid[y][x] == 0

    if not is_valid(*start) or not is_valid(*goal):
        return None

    path = [start]
    current = start
    stuck_counter = 0
    prev_pos = None

    for _ in range(max_steps):
        if current == goal:
            return path

        # Calculate attractive force (toward goal)
        dx_goal = goal[0] - current[0]
        dy_goal = goal[1] - current[1]
        dist_goal = math.sqrt(dx_goal**2 + dy_goal**2)

        if dist_goal < 0.1:
            return path

        # Unit vector toward goal
        fx_attr = attractive_gain * dx_goal / dist_goal
        fy_attr = attractive_gain * dy_goal / dist_goal

        # Calculate repulsive forces (away from obstacles)
        fx_rep = 0.0
        fy_rep = 0.0

        for y in range(
            max(0, current[1] - int(influence_distance) - 1),
            min(rows, current[1] + int(influence_distance) + 2),
        ):
            for x in range(
                max(0, current[0] - int(influence_distance) - 1),
                min(cols, current[0] + int(influence_distance) + 2),
            ):
                if grid[y][x] == 1:  # Obstacle
                    dx_obs = current[0] - x
                    dy_obs = current[1] - y
                    dist_obs = math.sqrt(dx_obs**2 + dy_obs**2)

                    if dist_obs < influence_distance and dist_obs > 0.1:
                        # Repulsive force: inversely proportional to distance
                        magnitude = (
                            repulsive_gain
                            * (1.0 / dist_obs - 1.0 / influence_distance)
                            / (dist_obs**2)
                        )
                        fx_rep += magnitude * dx_obs / dist_obs
                        fy_rep += magnitude * dy_obs / dist_obs

        # Total force
        fx_total = fx_attr + fx_rep
        fy_total = fy_attr + fy_rep

        # Determine next move (discretized to 8 directions)
        angle = math.atan2(fy_total, fx_total)

        # Try 8 directions, prioritizing the direction of total force
        directions = []
        for i in range(8):
            a = angle + (i // 2) * (math.pi / 4) * (1 if i % 2 == 0 else -1)
            dx = round(math.cos(a))
            dy = round(math.sin(a))
            directions.append((dx, dy))

        # Find first valid move
        moved = False
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if is_valid(nx, ny):
                current = (nx, ny)
                path.append(current)
                moved = True
                break

        if not moved:
            return None  # Stuck (no valid moves)

        # Detect oscillation or being stuck
        if current == prev_pos:
            stuck_counter += 1
            if stuck_counter > 5:
                return None  # Likely in local minimum
        else:
            stuck_counter = 0

        prev_pos = path[-2] if len(path) >= 2 else None

    return None  # Max steps exceeded


def demo():
    """Demo potential field navigation."""
    print("Potential Field Navigation Demo")
    print("=" * 50)

    # Create environment with obstacles
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    start = (1, 1)
    goal = (8, 6)

    print("Grid (0=free, 1=obstacle):")
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print(f"\nStart: {start}, Goal: {goal}\n")

    # Try different parameter combinations
    configs = [
        (1.0, 100.0, 3.0, "Balanced"),
        (2.0, 100.0, 3.0, "Strong attraction"),
        (1.0, 200.0, 3.0, "Strong repulsion"),
        (1.0, 100.0, 5.0, "Large influence distance"),
    ]

    for attr_gain, rep_gain, influence, name in configs:
        print(f"{name} (attr={attr_gain}, rep={rep_gain}, influence={influence}):")
        path = potential_field_navigate(
            maze,
            start,
            goal,
            attractive_gain=attr_gain,
            repulsive_gain=rep_gain,
            influence_distance=influence,
            max_steps=300,
        )

        if path:
            print(f"  Success! Path length: {len(path)} steps")
        else:
            print("  Failed (local minimum or stuck)")
        print()

    print("Key Insights:")
    print("- Attractive force pulls robot toward goal")
    print("- Repulsive forces push robot away from obstacles")
    print("- Can get stuck in local minima (e.g., U-shaped obstacles)")
    print("- Parameter tuning is crucial:")
    print("  * Higher attractive_gain: more direct path, may hit obstacles")
    print("  * Higher repulsive_gain: safer but may not reach goal")
    print("  * Larger influence_distance: smoother but may be overly cautious")
    print("- Works well in open environments")
    print("- Real-time capable (reactive)")


if __name__ == "__main__":
    demo()
