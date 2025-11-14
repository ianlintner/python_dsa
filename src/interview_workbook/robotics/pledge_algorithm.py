"""
Pledge algorithm for maze navigation.

The Pledge algorithm is an improvement over simple wall-following that
can escape from closed loops by tracking the robot's total rotation angle.

Time complexity: O(P) where P is obstacle perimeter
Space complexity: O(1) - only tracks angle counter
"""

from __future__ import annotations

from interview_workbook.robotics.utils import Direction, GridWorld, RobotState


def pledge_navigate(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_steps: int = 2000
) -> list[tuple[int, int]] | None:
    """
    Navigate using Pledge algorithm.

    The Pledge algorithm improves on wall-following by tracking total rotation.
    When total rotation returns to 0 (or multiple of 360°), the robot resumes
    straight-line motion toward the goal.

    Algorithm:
    1. Move straight toward goal direction
    2. When obstacle encountered, follow wall (e.g., right-hand rule)
    3. Track cumulative rotation angle
    4. When total rotation = 0, resume straight motion
    5. Repeat until goal reached

    Time: O(P) where P is total obstacle perimeter
    Space: O(1) for rotation counter

    Args:
        grid: Environment with obstacles
        start: Starting position
        goal: Goal position
        max_steps: Maximum steps to prevent infinite loops

    Returns:
        Path to goal or None if not reachable

    Advantages over wall-following:
    - Can escape from closed obstacle loops
    - More efficient in many cases
    - Still reactive and simple

    Common pitfalls:
    - Requires orientation tracking
    - May still revisit areas
    - Not optimal path
    """
    if not grid.is_free(*start) or not grid.is_free(*goal):
        return None

    # Determine initial direction toward goal
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]

    if abs(dx) > abs(dy):
        initial_dir = Direction.EAST if dx > 0 else Direction.WEST
    else:
        initial_dir = Direction.SOUTH if dy > 0 else Direction.NORTH

    robot = RobotState(start[0], start[1], initial_dir)
    path = [start]
    rotation_sum = 0  # Track cumulative rotation in 90-degree units
    following_wall = False

    for _ in range(max_steps):
        if (robot.x, robot.y) == goal:
            return path

        if not following_wall and rotation_sum == 0:
            # Try to move straight toward goal
            next_pos = robot.move_forward()

            if grid.is_free(*next_pos):
                robot.apply_move()
                path.append((robot.x, robot.y))
            else:
                # Hit obstacle, start following wall
                following_wall = True
                robot.turn_right()
                rotation_sum += 1
        else:
            # Following wall with right-hand rule
            # First try to turn left (to follow wall closely)
            robot.turn_left()
            rotation_sum -= 1
            next_pos = robot.move_forward()

            if grid.is_free(*next_pos):
                robot.apply_move()
                path.append((robot.x, robot.y))
            else:
                # Wall on left, turn back right and try straight
                robot.turn_right()
                rotation_sum += 1
                next_pos = robot.move_forward()

                if grid.is_free(*next_pos):
                    robot.apply_move()
                    path.append((robot.x, robot.y))
                else:
                    # Blocked straight, turn right again
                    robot.turn_right()
                    rotation_sum += 1
                    next_pos = robot.move_forward()

                    if grid.is_free(*next_pos):
                        robot.apply_move()
                        path.append((robot.x, robot.y))
                    else:
                        # Turn around (blocked on 3 sides)
                        robot.turn_right()
                        rotation_sum += 1

            # Check if we can resume straight motion
            if rotation_sum == 0:
                following_wall = False

    return None


def demo():
    """Demo Pledge algorithm."""
    print("Pledge Algorithm Demo")
    print("=" * 50)

    # Create maze with a closed loop
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    grid = GridWorld(maze)
    start = (0, 0)
    goal = (8, 6)

    print("Grid (0=free, 1=wall):")
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print(f"\nStart: {start}, Goal: {goal}\n")

    path = pledge_navigate(grid, start, goal, max_steps=500)

    if path:
        print(f"Path found: {len(path)} steps")
        print(f"Unique positions visited: {len(set(path))}")

        # Show path on grid
        path_set = set(path)
        print("\nPath visualization (S=start, G=goal, *=path):")
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
            print(" ".join(line))
    else:
        print("Goal not reached")

    print("\nPledge Algorithm Insights:")
    print("- Tracks cumulative rotation to detect when robot has 'unwound'")
    print("- When rotation sum = 0, robot resumes straight motion")
    print("- Avoids infinite loops in closed obstacle boundaries")
    print("- More sophisticated than simple wall-following")
    print("- Still reactive: uses only local sensor information")
    print("- Works well for simply-connected obstacles")


if __name__ == "__main__":
    demo()
