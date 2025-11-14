"""
Occupancy Grid Mapping for robots.

Occupancy grids represent the environment as a discretized grid where each
cell has a probability of being occupied. This is a fundamental technique
in robotic mapping and SLAM.

Time complexity: O(rays * cells_per_ray) per update
Space complexity: O(width * height) for grid
"""

from __future__ import annotations

import math


class OccupancyGrid:
    """
    Probabilistic occupancy grid for environment mapping.

    Each cell stores log-odds of occupancy for numerical stability.
    """

    def __init__(self, width: int, height: int, resolution: float = 1.0):
        """
        Initialize occupancy grid.

        Args:
            width: Grid width in cells
            height: Grid height in cells
            resolution: Meters per cell
        """
        self.width = width
        self.height = height
        self.resolution = resolution
        # Log-odds representation: log(p/(1-p))
        # 0 = unknown, > 0 = occupied, < 0 = free
        self.grid = [[0.0 for _ in range(width)] for _ in range(height)]

        # Sensor model parameters (log-odds)
        self.log_odds_occ = 0.4  # Increase when obstacle detected
        self.log_odds_free = -0.4  # Decrease when free space observed
        self.max_log_odds = 3.5  # Clamp to prevent overflow
        self.min_log_odds = -3.5

    def update_ray(self, robot_pos: tuple[float, float], hit_pos: tuple[float, float]):
        """
        Update grid with a single range sensor ray.

        Mark cells along ray as free, and endpoint as occupied.

        Time: O(ray_length) for bresenham line traversal
        Space: O(1)

        Args:
            robot_pos: Robot position in world coordinates
            hit_pos: Where ray hit obstacle (or max range)
        """
        # Convert to grid coordinates
        x0 = int(robot_pos[0] / self.resolution)
        y0 = int(robot_pos[1] / self.resolution)
        x1 = int(hit_pos[0] / self.resolution)
        y1 = int(hit_pos[1] / self.resolution)

        # Get all cells along ray (Bresenham's line algorithm)
        cells = self._bresenham_line(x0, y0, x1, y1)

        # Update cells along ray as free (except endpoint)
        for x, y in cells[:-1]:
            if self._in_bounds(x, y):
                self.grid[y][x] += self.log_odds_free
                self.grid[y][x] = max(self.min_log_odds, min(self.max_log_odds, self.grid[y][x]))

        # Update endpoint as occupied
        if cells and self._in_bounds(cells[-1][0], cells[-1][1]):
            x, y = cells[-1]
            self.grid[y][x] += self.log_odds_occ
            self.grid[y][x] = max(self.min_log_odds, min(self.max_log_odds, self.grid[y][x]))

    def get_probability(self, x: int, y: int) -> float:
        """
        Get occupancy probability for cell.

        Converts log-odds back to probability: p = 1 / (1 + exp(-log_odds))
        """
        if not self._in_bounds(x, y):
            return 0.5

        log_odds = self.grid[y][x]
        return 1.0 / (1.0 + math.exp(-log_odds))

    def is_occupied(self, x: int, y: int, threshold: float = 0.7) -> bool:
        """Check if cell is occupied (probability above threshold)."""
        return self.get_probability(x, y) > threshold

    def _in_bounds(self, x: int, y: int) -> bool:
        """Check if grid coordinates are valid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _bresenham_line(self, x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
        """Bresenham's line algorithm to get cells along ray."""
        cells = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        x, y = x0, y0

        while True:
            cells.append((x, y))

            if x == x1 and y == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return cells

    def to_grid_visualization(
        self, unknown_char: str = "?", free_char: str = ".", occ_char: str = "#"
    ) -> list[str]:
        """
        Convert occupancy grid to ASCII visualization.

        Args:
            unknown_char: Character for unknown cells
            free_char: Character for free cells
            occ_char: Character for occupied cells

        Returns:
            List of strings representing the grid
        """
        lines = []
        for row in self.grid:
            line = []
            for log_odds in row:
                if abs(log_odds) < 0.1:
                    line.append(unknown_char)
                elif log_odds > 0:
                    line.append(occ_char)
                else:
                    line.append(free_char)
            lines.append(" ".join(line))
        return lines


def demo():
    """Demo occupancy grid mapping."""
    print("Occupancy Grid Mapping Demo")
    print("=" * 50)

    # Create occupancy grid
    grid = OccupancyGrid(width=20, height=15, resolution=1.0)

    # Simulate robot scanning environment
    # Robot at center, scanning 360 degrees
    robot_x, robot_y = 10.0, 7.5

    print(f"Robot position: ({robot_x}, {robot_y})")
    print("Simulating laser scans...\n")

    # Simulate obstacles (walls)
    obstacles = [
        # Vertical wall on right
        [(15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9)],
        # Horizontal wall on top
        [(5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3)],
        # Small obstacle
        [(7, 10), (8, 10)],
    ]

    # Flatten obstacles
    obstacle_set = set()
    for obs_list in obstacles:
        obstacle_set.update(obs_list)

    # Simulate laser scans at different angles
    num_rays = 36  # 10 degree increments
    max_range = 12.0

    for i in range(num_rays):
        angle = (i / num_rays) * 2 * math.pi

        # Cast ray
        dx = math.cos(angle)
        dy = math.sin(angle)

        # Find hit point (either obstacle or max range)
        hit_x, hit_y = robot_x, robot_y
        for step in range(1, int(max_range) + 1):
            test_x = robot_x + dx * step
            test_y = robot_y + dy * step

            grid_x = int(test_x)
            grid_y = int(test_y)

            if (grid_x, grid_y) in obstacle_set:
                hit_x = test_x
                hit_y = test_y
                break

            hit_x = test_x
            hit_y = test_y

        # Update grid
        grid.update_ray((robot_x, robot_y), (hit_x, hit_y))

    # Display grid
    print("Occupancy Grid (? = unknown, . = free, # = occupied):")
    viz = grid.to_grid_visualization()
    for line in viz:
        print(line)

    print("\nKey Insights:")
    print("- Each cell stores probability of occupancy")
    print("- Log-odds representation prevents numerical issues")
    print("- Cells along ray marked as free, endpoint as occupied")
    print("- Multiple observations increase confidence")
    print("- Probabilistic: handles sensor noise gracefully")
    print("- Foundation for SLAM (Simultaneous Localization and Mapping)")
    print("\nSensor Model:")
    print(f"  - log_odds_occ: +{grid.log_odds_occ} (obstacle detected)")
    print(f"  - log_odds_free: {grid.log_odds_free} (free space observed)")
    print("  - Clamped to prevent overflow")
    print("\nApplications:")
    print("  - Autonomous navigation")
    print("  - SLAM algorithms")
    print("  - Obstacle detection and avoidance")


if __name__ == "__main__":
    demo()
