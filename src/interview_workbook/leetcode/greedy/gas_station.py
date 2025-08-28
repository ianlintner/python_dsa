"""
LeetCode 134: Gas Station

There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].
You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1.

If there exists a solution, it is guaranteed to be unique.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        """
        Greedy approach: Find the starting position that allows completing the circuit.

        Key insights:
        1. If total_gas < total_cost, no solution exists
        2. If a solution exists, it's unique and can be found by tracking cumulative deficit
        3. When we can't continue from a position, the next valid start is after current position

        Algorithm:
        - Track total gas and cost to verify solution exists
        - Track current tank and starting position
        - When tank goes negative, reset start to next position

        Time: O(n) - Single pass through arrays
        Space: O(1) - Only using constant extra space
        """
        n = len(gas)
        total_gas = sum(gas)
        total_cost = sum(cost)

        # If total gas < total cost, impossible to complete circuit
        if total_gas < total_cost:
            return -1

        current_tank = 0
        start = 0

        for i in range(n):
            current_tank += gas[i] - cost[i]

            # If we can't reach next station from current start
            if current_tank < 0:
                # Reset: next position as potential start
                start = i + 1
                current_tank = 0

        return start

    def canCompleteCircuitBruteForce(self, gas: List[int], cost: List[int]) -> int:
        """
        Brute force approach: Try each position as starting point.

        For each potential starting position, simulate the journey
        and check if we can complete the full circuit.

        Time: O(n²) - For each starting position, check all stations
        Space: O(1) - Only using constant extra space
        """
        n = len(gas)

        for start in range(n):
            tank = 0
            position = start

            # Try to complete circuit from this start
            for _ in range(n):
                tank += gas[position] - cost[position]

                # Can't reach next station
                if tank < 0:
                    break

                position = (position + 1) % n

            # Successfully completed circuit
            if tank >= 0:
                return start

        return -1

    def canCompleteCircuitTwoPass(self, gas: List[int], cost: List[int]) -> int:
        """
        Two-pass approach: First check if solution exists, then find starting position.

        This approach separates the logic for checking feasibility
        and finding the optimal starting position.

        Time: O(n) - Two passes through the arrays
        Space: O(1) - Only using constant extra space
        """
        n = len(gas)
        total_surplus = 0
        current_surplus = 0
        start = 0

        for i in range(n):
            net_gain = gas[i] - cost[i]
            total_surplus += net_gain
            current_surplus += net_gain

            # If current surplus is negative, reset start position
            if current_surplus < 0:
                start = i + 1
                current_surplus = 0

        # If total surplus is negative, no solution exists
        return start if total_surplus >= 0 else -1


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different gas station scenarios.
    """
    solution = Solution()

    demos = []

    # Test case 1: Standard case with valid solution
    gas1 = [1, 2, 3, 4, 5]
    cost1 = [3, 4, 5, 1, 2]
    result1 = solution.canCompleteCircuit(gas1, cost1)
    demos.append(f"Input: gas={gas1}, cost={cost1}")
    demos.append(f"Starting station: {result1}")
    demos.append("Analysis: Start at station 3 (0-indexed)")
    demos.append("Journey: 3→4→0→1→2→3 (completes circuit)")
    demos.append("")

    # Test case 2: No solution possible
    gas2 = [2, 3, 4]
    cost2 = [3, 4, 3]
    result2 = solution.canCompleteCircuit(gas2, cost2)
    demos.append(f"Input: gas={gas2}, cost={cost2}")
    demos.append(f"Starting station: {result2}")
    demos.append("Analysis: Total gas=9, total cost=10 → impossible")
    demos.append("")

    # Test case 3: Multiple feasible starts, but only one optimal
    gas3 = [5, 1, 2, 3, 4]
    cost3 = [4, 4, 1, 5, 1]
    result3 = solution.canCompleteCircuit(gas3, cost3)
    demos.append(f"Input: gas={gas3}, cost={cost3}")
    demos.append(f"Starting station: {result3}")
    demos.append("Analysis: Station 4 allows completing entire circuit")
    demos.append("")

    # Test case 4: Single station
    gas4 = [2]
    cost4 = [2]
    result4 = solution.canCompleteCircuit(gas4, cost4)
    demos.append(f"Input: gas={gas4}, cost={cost4}")
    demos.append(f"Starting station: {result4}")
    demos.append("Analysis: Exactly enough gas to complete circuit")
    demos.append("")

    # Test case 5: Large surplus at one station
    gas5 = [3, 1, 1]
    cost5 = [1, 2, 2]
    result5 = solution.canCompleteCircuit(gas5, cost5)
    demos.append(f"Input: gas={gas5}, cost={cost5}")
    demos.append(f"Starting station: {result5}")
    demos.append("Analysis: Must start where there's enough surplus")
    demos.append("")

    # Algorithm analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Greedy Strategy:")
    demos.append("1. Check if total_gas >= total_cost (necessary condition)")
    demos.append("2. Track current tank level while traversing")
    demos.append("3. When tank goes negative, reset start to next position")
    demos.append("4. This works because:")
    demos.append("   - If solution exists, it's unique")
    demos.append("   - Any position between old_start and current can't work")
    demos.append("   - The first position after deficit is optimal candidate")
    demos.append("")

    demos.append("Key Insights:")
    demos.append("- If we can't reach station i from start j, then no station k (j ≤ k < i) works")
    demos.append("- This is because partial sums are decreasing in this range")
    demos.append("- Therefore, we can skip all intermediate positions")
    demos.append("- Single pass solution is possible with this observation")
    demos.append("")

    # Performance comparison
    import time

    large_gas = [i % 10 + 1 for i in range(1000)]
    large_cost = [(i + 3) % 8 + 1 for i in range(1000)]

    # Time greedy approach
    start_time = time.time()
    for _ in range(1000):
        solution.canCompleteCircuit(large_gas, large_cost)
    greedy_time = time.time() - start_time

    # Time brute force approach (smaller array for reasonable runtime)
    small_gas = [i % 5 + 1 for i in range(20)]
    small_cost = [(i + 2) % 4 + 1 for i in range(20)]
    start_time = time.time()
    for _ in range(100):
        solution.canCompleteCircuitBruteForce(small_gas, small_cost)
    brute_time = time.time() - start_time

    demos.append("=== Performance Comparison ===")
    demos.append(f"Greedy approach (1000 runs, 1000 stations): {greedy_time:.6f}s")
    demos.append(f"Brute force (100 runs, 20 stations): {brute_time:.6f}s")
    demos.append("Greedy: O(n) time, O(1) space")
    demos.append("Brute force: O(n²) time, O(1) space")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Vehicle route planning with fuel constraints")
    demos.append("- Supply chain optimization with capacity limits")
    demos.append("- Circular buffer management in systems")
    demos.append("- Resource allocation in distributed systems")
    demos.append("- Power grid load balancing across stations")
    demos.append("- Delivery route optimization with refueling stops")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(
        input=[[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]],
        expected=3,
        description="Standard case - start at station 3",
    ),
    TestCase(
        input=[[2, 3, 4], [3, 4, 3]],
        expected=-1,
        description="Impossible case - insufficient total gas",
    ),
    TestCase(
        input=[[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], expected=4, description="Start at last station"
    ),
    TestCase(input=[[2], [2]], expected=0, description="Single station - exactly enough gas"),
    TestCase(input=[[1], [2]], expected=-1, description="Single station - insufficient gas"),
    TestCase(
        input=[[3, 1, 1], [1, 2, 2]], expected=0, description="Start at station with large surplus"
    ),
    TestCase(
        input=[[5, 8, 2, 8], [6, 5, 6, 6]], expected=3, description="Multiple deficit regions"
    ),
]


def test_solution():
    """Test the gas station solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.canCompleteCircuit, TEST_CASES)


# Register the problem
register_problem(
    slug="gas_station",
    leetcode_num=134,
    title="Gas Station",
    difficulty=Difficulty.MEDIUM,
    category=Category.GREEDY,
    solution_func=Solution().canCompleteCircuit,
    test_func=test_solution,
    demo_func=create_demo_output,
)
