"""
Particle Filter for robot localization.

Particle filters (Sequential Monte Carlo) are used for robot localization -
estimating the robot's position and orientation from noisy sensor measurements.

Time complexity: O(N) per update where N is number of particles
Space complexity: O(N) for storing particles
"""

from __future__ import annotations

import math
import random


class Particle:
    """Represents a hypothesis about robot state (x, y, orientation)."""

    def __init__(self, x: float, y: float, heading: float, weight: float = 1.0):
        self.x = x
        self.y = y
        self.heading = heading  # In radians
        self.weight = weight

    def __repr__(self) -> str:
        return (
            f"Particle(x={self.x:.2f}, y={self.y:.2f}, θ={self.heading:.2f}, w={self.weight:.3f})"
        )


def particle_filter_localize(
    particles: list[Particle],
    measurement: tuple[float, float],
    movement: tuple[float, float, float],
    landmarks: list[tuple[float, float]],
    motion_noise: float = 0.1,
    measurement_noise: float = 0.5,
) -> list[Particle]:
    """
    Perform one iteration of particle filter localization.

    Algorithm:
    1. Prediction: Move particles according to motion model
    2. Update: Weight particles by measurement likelihood
    3. Resample: Draw new particles proportional to weights

    Time: O(N * M) where N=particles, M=landmarks
    Space: O(N) for particle set

    Args:
        particles: Current particle set
        measurement: Sensor reading (e.g., range to landmark)
        movement: (dx, dy, dtheta) motion command
        landmarks: Known landmark positions
        motion_noise: Noise in motion model
        measurement_noise: Noise in sensor measurements

    Returns:
        New particle set after prediction, update, and resample

    Advantages:
    - Non-parametric: can represent multimodal distributions
    - Works with non-Gaussian noise
    - Effective for global localization

    Disadvantages:
    - Particle depletion possible
    - Requires many particles for high dimensions
    - Computational cost scales with particles
    """
    # 1. Prediction step: apply motion model with noise
    for p in particles:
        dx, dy, dtheta = movement

        # Add motion noise
        dx += random.gauss(0, motion_noise)
        dy += random.gauss(0, motion_noise)
        dtheta += random.gauss(0, motion_noise * 0.1)

        # Update particle pose
        p.x += dx
        p.y += dy
        p.heading += dtheta

    # 2. Update step: weight particles by measurement likelihood
    for p in particles:
        # Calculate expected measurement from this particle's pose
        # Assuming measurement is distance to nearest landmark
        if landmarks:
            # Find nearest landmark
            min_expected_dist = float("inf")
            for lx, ly in landmarks:
                dist = ((p.x - lx) ** 2 + (p.y - ly) ** 2) ** 0.5
                min_expected_dist = min(min_expected_dist, dist)

            # Measurement likelihood (Gaussian)
            measured_dist = (measurement[0] ** 2 + measurement[1] ** 2) ** 0.5
            error = abs(measured_dist - min_expected_dist)
            p.weight = _gaussian(error, 0, measurement_noise)
        else:
            p.weight = 1.0

    # Normalize weights
    total_weight = sum(p.weight for p in particles)
    if total_weight > 0:
        for p in particles:
            p.weight /= total_weight

    # 3. Resample: draw new particles proportional to weights
    new_particles = []
    weights = [p.weight for p in particles]

    for _ in range(len(particles)):
        # Weighted random selection
        selected = _weighted_random_choice(particles, weights)
        # Create new particle (add small noise to avoid particle depletion)
        new_p = Particle(
            selected.x + random.gauss(0, motion_noise * 0.1),
            selected.y + random.gauss(0, motion_noise * 0.1),
            selected.heading + random.gauss(0, motion_noise * 0.01),
            1.0,
        )
        new_particles.append(new_p)

    return new_particles


def estimate_pose(particles: list[Particle]) -> tuple[float, float, float]:
    """
    Estimate robot pose from particle distribution.
    Returns weighted mean of particles.
    """
    if not particles:
        return (0.0, 0.0, 0.0)

    x_sum = sum(p.x * p.weight for p in particles)
    y_sum = sum(p.y * p.weight for p in particles)
    heading_sum = sum(p.heading * p.weight for p in particles)
    weight_sum = sum(p.weight for p in particles)

    if weight_sum > 0:
        return (x_sum / weight_sum, y_sum / weight_sum, heading_sum / weight_sum)
    else:
        return (
            sum(p.x for p in particles) / len(particles),
            sum(p.y for p in particles) / len(particles),
            sum(p.heading for p in particles) / len(particles),
        )


def _gaussian(x: float, mu: float, sigma: float) -> float:
    """Gaussian probability density."""
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))


def _weighted_random_choice(items: list[Particle], weights: list[float]) -> Particle:
    """Select item with probability proportional to weight."""
    total = sum(weights)
    r = random.uniform(0, total)
    cumsum = 0.0
    for item, weight in zip(items, weights):
        cumsum += weight
        if cumsum >= r:
            return item
    return items[-1]


def demo():
    """Demo particle filter localization."""
    print("Particle Filter Localization Demo")
    print("=" * 50)

    random.seed(42)

    # Initialize particles (uniform distribution)
    num_particles = 100
    particles = [
        Particle(
            random.uniform(0, 10),
            random.uniform(0, 10),
            random.uniform(0, 6.28),
            1.0 / num_particles,
        )
        for _ in range(num_particles)
    ]

    # Known landmarks
    landmarks = [(2.0, 2.0), (8.0, 2.0), (5.0, 8.0)]

    # True robot pose (unknown to filter)
    true_x, true_y, true_heading = 5.0, 5.0, 0.0

    print(f"Landmarks: {landmarks}")
    print(f"True initial pose: x={true_x:.2f}, y={true_y:.2f}, θ={true_heading:.2f}")
    print(f"Number of particles: {num_particles}\n")

    # Simulate robot movement and measurements
    movements = [
        (1.0, 0.0, 0.0),  # Move right
        (0.0, 1.0, 0.0),  # Move down
        (0.5, 0.5, 0.0),  # Move diagonally
    ]

    for i, movement in enumerate(movements):
        print(f"Step {i + 1}: Movement {movement}")

        # Update true pose
        true_x += movement[0]
        true_y += movement[1]
        true_heading += movement[2]

        # Simulate measurement (distance to nearest landmark)
        min_dist = float("inf")
        for lx, ly in landmarks:
            dist = ((true_x - lx) ** 2 + (true_y - ly) ** 2) ** 0.5
            min_dist = min(min_dist, dist)

        # Add measurement noise
        measured_dist = min_dist + random.gauss(0, 0.3)
        measurement = (measured_dist, 0.0)  # Simplified: just distance

        # Run particle filter
        particles = particle_filter_localize(
            particles, measurement, movement, landmarks, motion_noise=0.1, measurement_noise=0.5
        )

        # Estimate pose
        est_x, est_y, est_heading = estimate_pose(particles)

        print(f"  True pose: x={true_x:.2f}, y={true_y:.2f}, θ={true_heading:.2f}")
        print(f"  Estimated: x={est_x:.2f}, y={est_y:.2f}, θ={est_heading:.2f}")
        print(f"  Error: {((est_x - true_x) ** 2 + (est_y - true_y) ** 2) ** 0.5:.2f}")
        print()

    print("Particle Filter Key Insights:")
    print("- Represents belief as set of weighted samples (particles)")
    print("- Three steps: Predict (motion model), Update (measurement), Resample")
    print("- Non-parametric: can represent complex, multimodal distributions")
    print("- Used for global localization and kidnapped robot problem")
    print("- Number of particles trades off accuracy vs computation")
    print("- Particle depletion: adding noise during resampling helps")
    print("- Converges as particles concentrate on true pose")


if __name__ == "__main__":
    demo()
