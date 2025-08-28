"""
LeetCode 853: Car Fleet

There are n cars going to the same destination along a one-lane road. The destination is target miles away.
Each car i has a constant speed speed[i] (in miles per hour), and initial position position[i] (in miles).
A car can never pass another car ahead of it, but it can catch up to it and drive bumper to bumper at the same speed.
The cars form a car fleet. Return the number of car fleets that will arrive at the destination.

URL: https://leetcode.com/problems/car-fleet/
Difficulty: Medium
Category: Stack

Patterns:
- Stack (monotonic decreasing by arrival time)
- Sorting by position
- Time calculation and fleet formation

Complexity:
- Time: O(n log n) - due to sorting
- Space: O(n) - for storing car data and stack

Pitfalls:
- Forgetting to sort cars by position first
- Not handling edge cases (empty arrays, single car)
- Incorrect time calculation or fleet formation logic
- Using position instead of arrival time for fleet determination

Follow-ups:
- What if cars can change lanes?
- How to handle cars with same position or speed?
- Can we solve without using extra space for sorting?
"""

from typing import List

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        """
        Calculate the number of car fleets that will arrive at the destination.

        Algorithm:
        1. Pair each car's position with its speed and sort by position (descending)
        2. Calculate arrival time for each car: (target - position) / speed
        3. Traverse from closest to target to furthest, using a stack:
           - If current car's arrival time > last fleet's time: new fleet
           - Otherwise: current car catches up and joins the last fleet
        4. Return the number of fleets (stack size)

        Key insight: We process cars from closest to target to furthest.
        A slower car ahead can be caught by a faster car behind.

        Args:
            target: Distance to destination
            position: Starting positions of cars
            speed: Speeds of cars

        Returns:
            Number of car fleets that will arrive at destination
        """
        if not position or not speed:
            return 0

        # Pair each car's position with its speed
        cars = list(zip(position, speed))
        # Sort by position in descending order (closest to target first)
        cars.sort(reverse=True)

        stack = []  # Stack to track arrival times of fleet leaders

        for pos, spd in cars:
            # Calculate time for this car to reach the target
            time = (target - pos) / spd

            # If this car takes longer than the current slowest fleet,
            # it forms a new fleet (can't catch up)
            if not stack or time > stack[-1]:
                stack.append(time)
            # Otherwise, this car will catch up to the fleet ahead
            # and join it, so we don't add it to the stack

        return len(stack)


# Test cases
test_cases = [
    TestCase((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3, "Example 1: Multiple fleets"),
    TestCase((10, [3], [3]), 1, "Example 2: Single car"),
    TestCase((100, [0, 2, 4], [4, 2, 1]), 1, "Example 3: All cars form one fleet"),
    TestCase((10, [0, 4, 2], [2, 1, 3]), 2, "Cars at different positions with different speeds"),
    TestCase(
        (10, [8, 3, 7, 4, 6, 5], [4, 4, 4, 4, 4, 4]),
        6,
        "All cars have same speed - no fleet formation",
    ),
    TestCase((10, [6, 8], [3, 2]), 2, "Slower car ahead, faster car behind - separate fleets"),
    TestCase((10, [3, 6], [2, 3]), 1, "Faster car behind catches up - one fleet"),
    TestCase(
        (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3, "Complex case with multiple fleet formations"
    ),
    TestCase((13, [10, 2, 5, 7, 8], [3, 2, 4, 1, 1]), 4, "Mixed speeds and positions"),
    TestCase((10, [0, 9], [1, 1]), 2, "Same speed, different positions - no catching up"),
]


def demo() -> str:
    """Run Car Fleet demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.carFleet, test_cases, "LeetCode 853: Car Fleet")

    return create_demo_output(
        "Car Fleet",
        test_results,
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Sort cars by position (closest to target first) to process in correct order
2. Calculate arrival time for each car: (target - position) / speed
3. Use monotonic stack to track fleet leaders by arrival time
4. Cars with earlier arrival times join existing fleets (don't form new ones)
5. Only cars that arrive later than all previous cars start new fleets

Algorithm steps:
- Sort cars by position descending (process from target backwards)
- For each car, calculate time to destination
- If arrival time > last fleet's time: new fleet (add to stack)
- Otherwise: joins existing fleet (no stack addition)
- Return stack size (number of fleet leaders)
        """.strip(),
    )


# Register the problem
register_problem(
    id=853,
    slug="car_fleet",
    title="Car Fleet",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "stack", "sorting"],
    url="https://leetcode.com/problems/car-fleet/",
    notes="Stack problem using sorting and time calculations to determine fleet formation",
)
