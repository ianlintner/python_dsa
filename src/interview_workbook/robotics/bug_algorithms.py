"""
Bug algorithms for robot navigation.

Bug1 and Bug2 are simple, reactive navigation algorithms that combine
goal-seeking behavior with obstacle avoidance. These algorithms are
provably complete for point robots in 2D environments.

Time complexity: O(n * P) where n is obstacles, P is total perimeter
Space complexity: O(P) for storing boundary points
"""

from __future__ import annotations

from interview_workbook.robotics.utils import GridWorld, euclidean_distance


def bug1_navigate(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_steps: int = 2000
) -> list[tuple[int, int]] | None:
    """
    Bug1 algorithm: Simple and complete obstacle avoidance.

    Algorithm:
    1. Move toward goal in straight line
    2. When hit obstacle, follow its perimeter completely
    3. Leave obstacle at point closest to goal
    4. Repeat until goal reached

    Time: O(n * P) where n is obstacles, P is total perimeter
    Space: O(P) to store perimeter points

    Args:
        grid: Environment with obstacles
        start: Starting position
        goal: Goal position
        max_steps: Maximum steps to prevent infinite loops

    Returns:
        Path to goal or None if not reachable

    Advantages:
    - Complete: guaranteed to find path if one exists
    - Simple to implement

    Disadvantages:
    - Not efficient: may traverse entire obstacle perimeter
    - Requires sensing entire perimeter before leaving
    """
    if not grid.is_free(*start) or not grid.is_free(*goal):
        return None

    path = [start]
    current = start

    for _ in range(max_steps):
        if current == goal:
            return path

        # Try to move toward goal
        next_pos = _move_toward_goal(grid, current, goal)

        if next_pos is None:
            # Hit an obstacle - use Bug1 strategy
            perimeter_path = _follow_obstacle_perimeter(grid, current, goal)
            if perimeter_path is None:
                return None

            path.extend(perimeter_path)
            if len(perimeter_path) > 0:
                current = perimeter_path[-1]
        else:
            path.append(next_pos)
            current = next_pos

    return None  # Max steps exceeded


def bug2_navigate(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_steps: int = 2000
) -> list[tuple[int, int]] | None:
    """
    Bug2 algorithm: More efficient than Bug1 in many cases.

    Algorithm:
    1. Define m-line: straight line from start to goal
    2. Move along m-line toward goal
    3. When hit obstacle, follow perimeter until:
       - Back on m-line AND
       - Closer to goal than hit point
    4. Resume moving along m-line

    Time: O(n * P) worst case, often better in practice
    Space: O(1) only tracks m-line

    Args:
        grid: Environment with obstacles
        start: Starting position
        goal: Goal position
        max_steps: Maximum steps

    Returns:
        Path to goal or None if not reachable

    Advantages:
    - Often more efficient than Bug1
    - Still complete

    Disadvantages:
    - Can be worse than Bug1 in adversarial cases
    - Requires sensing position relative to m-line
    """
    if not grid.is_free(*start) or not grid.is_free(*goal):
        return None

    path = [start]
    current = start
    following_wall = False
    hit_point = None
    hit_distance = float("inf")

    for _ in range(max_steps):
        if current == goal:
            return path

        if not following_wall:
            # Try to move toward goal along m-line
            next_pos = _move_toward_goal(grid, current, goal)

            if next_pos is None:
                # Hit obstacle - start following perimeter
                following_wall = True
                hit_point = current
                hit_distance = euclidean_distance(current, goal)
            else:
                path.append(next_pos)
                current = next_pos
        else:
            # Following obstacle perimeter
            # Check if we're back on m-line and closer to goal
            if current != hit_point and _on_m_line(start, goal, current):
                current_distance = euclidean_distance(current, goal)
                if current_distance < hit_distance:
                    # Leave obstacle and resume toward goal
                    following_wall = False
                    continue

            # Continue following perimeter
            next_pos = _follow_wall_step(grid, current, goal)
            if next_pos is None:
                return None
            path.append(next_pos)
            current = next_pos

    return None


def _move_toward_goal(
    grid: GridWorld, current: tuple[int, int], goal: tuple[int, int]
) -> tuple[int, int] | None:
    """
    Try to move one step toward goal. Return None if obstacle blocks.
    Uses simple greedy approach: move in direction that reduces distance most.
    """
    x, y = current
    best_pos = None
    best_dist = euclidean_distance(current, goal)

    # Try all 4 neighbors
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if grid.is_free(nx, ny):
            dist = euclidean_distance((nx, ny), goal)
            if dist < best_dist:
                best_dist = dist
                best_pos = (nx, ny)

    return best_pos


def _follow_obstacle_perimeter(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_perimeter: int = 500
) -> list[tuple[int, int]] | None:
    """
    Follow obstacle perimeter completely (Bug1).
    Return to point closest to goal.
    """
    perimeter = []
    current = start
    closest_point = start
    closest_dist = euclidean_distance(start, goal)

    # Follow wall using right-hand rule
    for _ in range(max_perimeter):
        next_pos = _follow_wall_step(grid, current, goal)
        if next_pos is None:
            return None

        perimeter.append(next_pos)
        current = next_pos

        # Track closest point to goal
        dist = euclidean_distance(current, goal)
        if dist < closest_dist:
            closest_dist = dist
            closest_point = current

        # Check if we've completed the perimeter
        if current == start and len(perimeter) > 1:
            break

    # Find path from start to closest point along perimeter
    if closest_point == start:
        return []

    for i, pos in enumerate(perimeter):
        if pos == closest_point:
            return perimeter[: i + 1]

    return perimeter


def _follow_wall_step(
    grid: GridWorld, current: tuple[int, int], goal: tuple[int, int]
) -> tuple[int, int] | None:
    """Make one step following the wall (right-hand rule)."""
    x, y = current

    # Try directions in order: prefer moving toward goal when possible
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if grid.is_free(nx, ny):
            return (nx, ny)

    return None


def _on_m_line(start: tuple[int, int], goal: tuple[int, int], point: tuple[int, int]) -> bool:
    """
    Check if point is (approximately) on the line from start to goal.
    Uses cross product to check collinearity with tolerance for grid cells.
    """
    # Vector from start to goal
    v1 = (goal[0] - start[0], goal[1] - start[1])
    # Vector from start to point
    v2 = (point[0] - start[0], point[1] - start[1])

    # Cross product (for 2D, this is scalar)
    cross = v1[0] * v2[1] - v1[1] * v2[0]

    # Allow small tolerance for discrete grid
    return abs(cross) < 1.5


def demo():
    """Demo Bug algorithms."""
    print("Bug Algorithms Demo")
    print("=" * 50)

    # Create environment with obstacles
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    grid = GridWorld(maze)
    start = (1, 1)
    goal = (7, 4)

    print("Grid (0=free, 1=obstacle):")
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print(f"\nStart: {start}, Goal: {goal}\n")

    # Bug1
    print("Bug1 Algorithm:")
    path1 = bug1_navigate(grid, start, goal, max_steps=500)
    if path1:
        print(f"  Path found: {len(path1)} steps")
        print(f"  Direct distance: {euclidean_distance(start, goal):.2f}")
    else:
        print("  Path not found")

    # Bug2
    print("\nBug2 Algorithm:")
    path2 = bug2_navigate(grid, start, goal, max_steps=500)
    if path2:
        print(f"  Path found: {len(path2)} steps")
        print(f"  Direct distance: {euclidean_distance(start, goal):.2f}")
    else:
        print("  Path not found")

    print("\nKey Differences:")
    print("Bug1:")
    print("  + Always complete (finds path if exists)")
    print("  + Simple strategy")
    print("  - May traverse entire perimeter unnecessarily")
    print("\nBug2:")
    print("  + Often more efficient")
    print("  + Stays closer to m-line")
    print("  - Can be worse in adversarial cases")
    print("\nBoth algorithms:")
    print("  - Reactive: only use local information")
    print("  - Complete: guaranteed to find path")
    print("  - Not optimal: don't find shortest path")


if __name__ == "__main__":
    demo()
