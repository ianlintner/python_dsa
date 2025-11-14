"""Utility classes and functions for robotics algorithms."""

from __future__ import annotations

from enum import Enum


class Direction(Enum):
    """Cardinal directions for robot orientation."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_left(self) -> Direction:
        """Turn 90 degrees counterclockwise."""
        return Direction((self.value - 1) % 4)

    def turn_right(self) -> Direction:
        """Turn 90 degrees clockwise."""
        return Direction((self.value + 1) % 4)

    def turn_around(self) -> Direction:
        """Turn 180 degrees."""
        return Direction((self.value + 2) % 4)

    def to_vector(self) -> tuple[int, int]:
        """Convert direction to (dx, dy) movement vector."""
        vectors = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        return vectors[self]


class RobotState:
    """Represents the state of a robot (position and orientation)."""

    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move_forward(self) -> tuple[int, int]:
        """Return the position the robot would reach by moving forward."""
        dx, dy = self.direction.to_vector()
        return (self.x + dx, self.y + dy)

    def apply_move(self):
        """Move the robot forward in its current direction."""
        self.x, self.y = self.move_forward()

    def turn_left(self):
        """Turn the robot left (counterclockwise)."""
        self.direction = self.direction.turn_left()

    def turn_right(self):
        """Turn the robot right (clockwise)."""
        self.direction = self.direction.turn_right()

    def turn_around(self):
        """Turn the robot 180 degrees."""
        self.direction = self.direction.turn_around()

    def __repr__(self) -> str:
        return f"RobotState(x={self.x}, y={self.y}, dir={self.direction.name})"


class GridWorld:
    """
    2D grid world environment for robot navigation.

    Convention:
    - 0 = free space
    - 1 = obstacle/wall
    - Grid coordinates: (0,0) is top-left
    """

    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def is_valid(self, x: int, y: int) -> bool:
        """Check if coordinates are within bounds."""
        return 0 <= x < self.cols and 0 <= y < self.rows

    def is_free(self, x: int, y: int) -> bool:
        """Check if cell is free (not an obstacle)."""
        return self.is_valid(x, y) and self.grid[y][x] == 0

    def is_obstacle(self, x: int, y: int) -> bool:
        """Check if cell contains an obstacle."""
        return not self.is_valid(x, y) or self.grid[y][x] == 1

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Get valid neighboring cells (4-directional)."""
        neighbors = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_free(nx, ny):
                neighbors.append((nx, ny))
        return neighbors


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
