"""
Wall-following navigation algorithm.

A fundamental robotics navigation technique where the robot follows walls
to navigate through unknown environments. This is useful when you only
know start and end positions and must discover obstacles by bumping into them.

Time complexity: O(P) where P is the perimeter of all obstacles encountered
Space complexity: O(1) - only stores robot state
"""

from __future__ import annotations

from interview_workbook.robotics.utils import Direction, GridWorld, RobotState


def wall_follow_left_hand(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_steps: int = 1000
) -> list[tuple[int, int]] | None:
    """
    Navigate from start to goal using left-hand wall-following rule.

    The robot keeps its left "hand" on the wall and follows it. This guarantees
    finding the goal if it's reachable and the obstacles are simply connected.

    Args:
        grid: The environment with obstacles
        start: Starting position (x, y)
        goal: Goal position (x, y)
        max_steps: Maximum steps to prevent infinite loops

    Returns:
        Path as list of positions, or None if goal not reached within max_steps

    Algorithm:
    1. Move forward if possible
    2. If can't move forward, turn right
    3. After turning right, try to turn left (to follow wall on left)
    4. Repeat until goal reached or max_steps exceeded

    Common pitfalls:
    - May not find goal if obstacles are not simply connected (multiple disconnected walls)
    - Can loop forever in certain maze configurations
    - Does not find shortest path
    """
    if not grid.is_free(*start) or not grid.is_free(*goal):
        return None

    robot = RobotState(start[0], start[1], Direction.NORTH)
    path = [start]
    visited = {start}

    for _ in range(max_steps):
        if (robot.x, robot.y) == goal:
            return path

        # Try to turn left first (to keep left hand on wall)
        robot.turn_left()
        next_pos = robot.move_forward()

        if grid.is_free(*next_pos):
            # Can move with left hand on wall
            robot.apply_move()
        else:
            # Wall on left, turn back right and try forward
            robot.turn_right()
            next_pos = robot.move_forward()

            if grid.is_free(*next_pos):
                robot.apply_move()
            else:
                # Can't move forward, keep turning right until we can
                robot.turn_right()
                next_pos = robot.move_forward()

                if grid.is_free(*next_pos):
                    robot.apply_move()
                else:
                    # Surrounded on 3 sides, turn around
                    robot.turn_right()

        current_pos = (robot.x, robot.y)
        if current_pos not in visited:
            visited.add(current_pos)
        path.append(current_pos)

    return None  # Goal not reached within max_steps


def wall_follow_right_hand(
    grid: GridWorld, start: tuple[int, int], goal: tuple[int, int], max_steps: int = 1000
) -> list[tuple[int, int]] | None:
    """
    Navigate using right-hand wall-following rule.

    Similar to left-hand rule but keeps right hand on the wall.

    Args:
        grid: The environment with obstacles
        start: Starting position (x, y)
        goal: Goal position (x, y)
        max_steps: Maximum steps to prevent infinite loops

    Returns:
        Path as list of positions, or None if goal not reached
    """
    if not grid.is_free(*start) or not grid.is_free(*goal):
        return None

    robot = RobotState(start[0], start[1], Direction.NORTH)
    path = [start]
    visited = {start}

    for _ in range(max_steps):
        if (robot.x, robot.y) == goal:
            return path

        # Try to turn right first (to keep right hand on wall)
        robot.turn_right()
        next_pos = robot.move_forward()

        if grid.is_free(*next_pos):
            # Can move with right hand on wall
            robot.apply_move()
        else:
            # Wall on right, turn back left and try forward
            robot.turn_left()
            next_pos = robot.move_forward()

            if grid.is_free(*next_pos):
                robot.apply_move()
            else:
                # Can't move forward, keep turning left until we can
                robot.turn_left()
                next_pos = robot.move_forward()

                if grid.is_free(*next_pos):
                    robot.apply_move()
                else:
                    # Surrounded on 3 sides, turn around
                    robot.turn_left()

        current_pos = (robot.x, robot.y)
        if current_pos not in visited:
            visited.add(current_pos)
        path.append(current_pos)

    return None


def demo():
    """Demo wall-following navigation."""
    print("Wall-Following Navigation Demo")
    print("=" * 50)

    # Create a simple maze
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    grid = GridWorld(maze)
    start = (0, 0)
    goal = (7, 6)

    print("Grid (0=free, 1=wall):")
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print()

    # Left-hand rule
    print(f"Start: {start}, Goal: {goal}")
    print("\nLeft-hand wall following:")
    path_left = wall_follow_left_hand(grid, start, goal, max_steps=200)
    if path_left:
        print(f"Found goal in {len(path_left)} steps")
        print(f"Path length: {len(set(path_left))} unique positions")
    else:
        print("Goal not reached")

    # Right-hand rule
    print("\nRight-hand wall following:")
    path_right = wall_follow_right_hand(grid, start, goal, max_steps=200)
    if path_right:
        print(f"Found goal in {len(path_right)} steps")
        print(f"Path length: {len(set(path_right))} unique positions")
    else:
        print("Goal not reached")

    print("\nKey insights:")
    print("- Wall-following is reactive, not optimal")
    print("- Works well in simply-connected environments")
    print("- Left vs right rule can give different paths")
    print("- May revisit cells multiple times")
    print("- No memory of visited cells in basic version")


if __name__ == "__main__":
    demo()
