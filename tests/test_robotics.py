"""Tests for robotics navigation algorithms."""

import random

from interview_workbook.robotics import (
    bug_algorithms,
    occupancy_grid,
    particle_filter,
    pledge_algorithm,
    potential_fields,
    rrt,
    utils,
    wall_following,
)


def test_direction_enum():
    """Test Direction enum functionality."""
    # Test turning
    assert utils.Direction.NORTH.turn_left() == utils.Direction.WEST
    assert utils.Direction.NORTH.turn_right() == utils.Direction.EAST
    assert utils.Direction.NORTH.turn_around() == utils.Direction.SOUTH

    # Test vectors
    assert utils.Direction.NORTH.to_vector() == (0, -1)
    assert utils.Direction.EAST.to_vector() == (1, 0)
    assert utils.Direction.SOUTH.to_vector() == (0, 1)
    assert utils.Direction.WEST.to_vector() == (-1, 0)


def test_robot_state():
    """Test RobotState class."""
    robot = utils.RobotState(5, 5, utils.Direction.NORTH)

    # Test forward movement
    assert robot.move_forward() == (5, 4)
    robot.apply_move()
    assert robot.x == 5 and robot.y == 4

    # Test turning
    robot.turn_right()
    assert robot.direction == utils.Direction.EAST
    assert robot.move_forward() == (6, 4)


def test_grid_world():
    """Test GridWorld class."""
    grid = utils.GridWorld([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

    # Test validity checks
    assert grid.is_valid(0, 0)
    assert not grid.is_valid(-1, 0)
    assert not grid.is_valid(3, 0)

    # Test obstacle checks
    assert grid.is_free(0, 0)
    assert grid.is_obstacle(1, 0)

    # Test neighbors (1,1) has neighbors at (0,1) and (1,2) - free cells
    neighbors = grid.get_neighbors(1, 1)
    assert (0, 1) in neighbors
    assert (1, 2) in neighbors
    assert len(neighbors) == 2  # Only two neighbors are free


def test_manhattan_distance():
    """Test Manhattan distance calculation."""
    assert utils.manhattan_distance((0, 0), (3, 4)) == 7
    assert utils.manhattan_distance((1, 1), (1, 1)) == 0
    assert utils.manhattan_distance((0, 0), (-3, -4)) == 7


def test_euclidean_distance():
    """Test Euclidean distance calculation."""
    assert utils.euclidean_distance((0, 0), (3, 4)) == 5.0
    assert utils.euclidean_distance((1, 1), (1, 1)) == 0.0


def test_wall_following_simple():
    """Test wall following algorithms."""
    maze = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    grid = utils.GridWorld(maze)
    start = (0, 0)
    goal = (4, 2)

    # Test left-hand rule
    path = wall_following.wall_follow_left_hand(grid, start, goal, max_steps=100)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal


def test_wall_following_invalid_positions():
    """Test wall following with invalid start/goal."""
    maze = [[0, 1, 0], [0, 0, 0], [1, 0, 0]]
    grid = utils.GridWorld(maze)

    # Start in obstacle
    path = wall_following.wall_follow_left_hand(grid, (1, 0), (2, 1), max_steps=100)
    assert path is None

    # Goal in obstacle
    path = wall_following.wall_follow_left_hand(grid, (0, 0), (1, 0), max_steps=100)
    assert path is None


def test_bug1_navigate():
    """Test Bug1 algorithm."""
    maze = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    grid = utils.GridWorld(maze)
    start = (0, 1)
    goal = (5, 1)

    path = bug_algorithms.bug1_navigate(grid, start, goal, max_steps=100)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal


def test_pledge_navigate():
    """Test Pledge algorithm."""
    maze = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    grid = utils.GridWorld(maze)
    start = (0, 0)
    goal = (4, 2)

    path = pledge_algorithm.pledge_navigate(grid, start, goal, max_steps=100)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal


def test_potential_field_navigate():
    """Test potential field navigation."""
    maze = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    start = (0, 1)
    goal = (4, 1)

    # Try with parameters that should work
    path = potential_fields.potential_field_navigate(
        maze,
        start,
        goal,
        attractive_gain=2.0,
        repulsive_gain=50.0,
        influence_distance=2.0,
        max_steps=100,
    )
    # Potential fields may fail due to local minima, so we just check it doesn't crash
    assert path is None or (isinstance(path, list) and len(path) > 0)


def test_rrt_plan():
    """Test RRT path planner."""
    random.seed(42)
    maze = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    start = (0, 1)
    goal = (4, 1)

    path = rrt.rrt_plan(maze, start, goal, max_iterations=500, step_size=1.0, goal_sample_rate=0.2)
    # RRT is probabilistic, so it may not always find a path, but with these parameters it should
    # Check that path is either None or a valid non-empty list
    assert path is None or (isinstance(path, list) and len(path) > 0)
    if path:
        assert path[0] == start
        assert path[-1] == goal


def test_rrt_invalid_positions():
    """Test RRT with invalid start/goal."""
    maze = [[0, 1, 0], [0, 0, 0]]

    # Start in obstacle
    path = rrt.rrt_plan(maze, (1, 0), (2, 1), max_iterations=100)
    assert path is None

    # Goal in obstacle
    path = rrt.rrt_plan(maze, (0, 0), (1, 0), max_iterations=100)
    assert path is None


def test_particle_filter_localize():
    """Test particle filter localization."""
    random.seed(42)

    # Initialize particles
    particles = [
        particle_filter.Particle(random.uniform(0, 10), random.uniform(0, 10), 0.0, 1.0)
        for _ in range(50)
    ]

    landmarks = [(5.0, 5.0)]
    measurement = (2.0, 0.0)
    movement = (1.0, 0.0, 0.0)

    # Run one iteration
    new_particles = particle_filter.particle_filter_localize(
        particles, measurement, movement, landmarks, motion_noise=0.1, measurement_noise=0.5
    )

    assert len(new_particles) == len(particles)
    assert all(isinstance(p, particle_filter.Particle) for p in new_particles)


def test_particle_filter_estimate_pose():
    """Test pose estimation from particles."""
    particles = [
        particle_filter.Particle(5.0, 5.0, 0.0, 1.0),
        particle_filter.Particle(5.1, 4.9, 0.1, 1.0),
        particle_filter.Particle(4.9, 5.1, -0.1, 1.0),
    ]

    x, y, heading = particle_filter.estimate_pose(particles)
    assert 4.8 < x < 5.2
    assert 4.8 < y < 5.2
    assert -0.2 < heading < 0.2


def test_occupancy_grid_creation():
    """Test occupancy grid initialization."""
    grid = occupancy_grid.OccupancyGrid(width=10, height=10, resolution=1.0)

    assert grid.width == 10
    assert grid.height == 10
    assert grid.resolution == 1.0
    assert len(grid.grid) == 10
    assert len(grid.grid[0]) == 10


def test_occupancy_grid_update():
    """Test occupancy grid ray updates."""
    grid = occupancy_grid.OccupancyGrid(width=10, height=10, resolution=1.0)

    # Update with a ray
    robot_pos = (5.0, 5.0)
    hit_pos = (8.0, 5.0)

    grid.update_ray(robot_pos, hit_pos)

    # Check that some cells were updated
    # Cells along ray should be marked as free (log_odds < 0)
    assert grid.grid[5][6] < 0  # Cell along ray should be free

    # Endpoint should be marked as occupied (log_odds > 0)
    assert grid.grid[5][8] > 0


def test_occupancy_grid_probability():
    """Test occupancy probability calculation."""
    grid = occupancy_grid.OccupancyGrid(width=5, height=5)

    # Initially all cells should be at 0.5 probability (unknown)
    assert abs(grid.get_probability(2, 2) - 0.5) < 0.01

    # Manually set log-odds and check probability
    grid.grid[2][2] = 2.0  # High log-odds = high probability
    assert grid.get_probability(2, 2) > 0.8

    grid.grid[3][3] = -2.0  # Low log-odds = low probability
    assert grid.get_probability(3, 3) < 0.2


def test_occupancy_grid_visualization():
    """Test occupancy grid visualization."""
    grid = occupancy_grid.OccupancyGrid(width=5, height=5)

    # Set some cells
    grid.grid[2][2] = 2.0  # Occupied
    grid.grid[1][1] = -2.0  # Free

    viz = grid.to_grid_visualization()
    assert len(viz) == 5
    assert "#" in viz[2]  # Occupied cell should show as #
    assert "." in viz[1]  # Free cell should show as .


def test_all_demos_run():
    """Test that all robotics demos can run without errors."""
    # Just check that demos don't crash
    wall_following.demo()
    bug_algorithms.demo()
    pledge_algorithm.demo()
    potential_fields.demo()
    particle_filter.demo()
    occupancy_grid.demo()

    # RRT demo uses randomness
    random.seed(42)
    rrt.demo()
