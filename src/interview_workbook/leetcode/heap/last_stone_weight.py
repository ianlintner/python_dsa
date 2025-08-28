"""
LeetCode 1046: Last Stone Weight

You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone remaining.

Return the weight of the last remaining stone. If there are no stones left, return 0.

Examples:
    Input: stones = [2,7,4,1,8,1]
    Output: 1
    Explanation:
    We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
    we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
    we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
    we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

    Input: stones = [1]
    Output: 1

Constraints:
    1 <= stones.length <= 30
    1 <= stones[i] <= 1000
"""

import heapq
from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Simulate stone smashing using max-heap.

        Algorithm:
        1. Use max-heap to always access two heaviest stones
        2. Python heapq is min-heap, so negate values for max-heap behavior
        3. Pop two largest stones, calculate difference
        4. If difference > 0, push back to heap
        5. Continue until heap has at most one element

        Time Complexity: O(n log n) - n heap operations
        Space Complexity: O(n) - heap storage
        """
        if not stones:
            return 0

        if len(stones) == 1:
            return stones[0]

        # Convert to max-heap by negating values
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)

        while len(max_heap) > 1:
            # Get two heaviest stones
            first = -heapq.heappop(max_heap)  # Heaviest stone
            second = -heapq.heappop(max_heap)  # Second heaviest stone

            # Smash stones together
            if first != second:
                # New stone has weight |first - second|
                new_weight = abs(first - second)
                heapq.heappush(max_heap, -new_weight)
            # If first == second, both stones are destroyed (do nothing)

        # Return weight of last stone, or 0 if no stones remain
        return -max_heap[0] if max_heap else 0

    def lastStoneWeightSimulation(self, stones: List[int]) -> int:
        """
        Direct simulation using sorting (less efficient but more intuitive).

        Algorithm:
        1. Keep stones list sorted in descending order
        2. Take two heaviest stones from front
        3. Calculate difference and insert back if needed
        4. Repeat until at most one stone remains

        Time Complexity: O(n² log n) - n iterations of O(n log n) sorting
        Space Complexity: O(1) - in-place operations
        """
        stones = stones.copy()  # Don't modify original

        while len(stones) > 1:
            # Sort in descending order to get heaviest stones first
            stones.sort(reverse=True)

            # Take two heaviest stones
            first = stones[0]
            second = stones[1]

            # Remove the two heaviest stones
            stones = stones[2:]

            # Smash stones together
            if first != second:
                # Add new stone with weight |first - second|
                stones.append(abs(first - second))

        return stones[0] if stones else 0

    def lastStoneWeightRecursive(self, stones: List[int]) -> int:
        """
        Recursive approach for educational purposes.

        Algorithm:
        1. Base case: 0 or 1 stones remaining
        2. Find and remove two heaviest stones
        3. Add difference back (if non-zero) and recurse

        Time Complexity: O(n² log n) - n recursive calls, each doing O(n log n) work
        Space Complexity: O(n) - recursion stack
        """
        if len(stones) <= 1:
            return stones[0] if stones else 0

        # Find two heaviest stones
        stones_copy = stones.copy()
        stones_copy.sort(reverse=True)

        first = stones_copy[0]
        second = stones_copy[1]

        # Create new stones list without the two heaviest
        remaining = stones_copy[2:]

        # Add difference if stones have different weights
        if first != second:
            remaining.append(abs(first - second))

        return self.lastStoneWeightRecursive(remaining)


def create_demo_output() -> str:
    """Create comprehensive demo showing stone smashing simulation and analysis."""
    solution = Solution()

    # Test cases for demonstration
    test_cases = [
        ([2, 7, 4, 1, 8, 1], "Classic example with multiple rounds"),
        ([1], "Single stone"),
        ([3, 7, 2], "Three stones"),
        ([2, 2], "Two equal stones - both destroyed"),
        ([10, 4, 2, 10], "Duplicate heaviest stones"),
        ([1, 2, 3, 4, 5], "Sequential weights"),
    ]

    output = []
    output.append("=== LeetCode 1046: Last Stone Weight ===\n")

    for stones, desc in test_cases:
        output.append(f"Test: {desc}")
        output.append(f"Input: stones = {stones}")

        # Test all approaches
        result1 = solution.lastStoneWeight(stones)
        result2 = solution.lastStoneWeightSimulation(stones)
        result3 = solution.lastStoneWeightRecursive(stones)

        output.append(f"Heap approach: {result1}")
        output.append(f"Simulation approach: {result2}")
        output.append(f"Recursive approach: {result3}")

        # Show step-by-step simulation for small examples
        if len(stones) <= 6:
            output.append("Step-by-step simulation:")
            steps = simulate_stone_smashing(stones)
            for i, step in enumerate(steps, 1):
                output.append(f"  Step {i}: {step}")

        output.append("")

    # Performance analysis
    output.append("=== Performance Analysis ===")
    output.append("Heap Approach:")
    output.append("  • Time: O(n log n) - n heap operations")
    output.append("  • Space: O(n) - heap storage")
    output.append("  • Best for: Optimal time complexity")
    output.append("")

    output.append("Simulation Approach:")
    output.append("  • Time: O(n² log n) - n iterations of sorting")
    output.append("  • Space: O(1) - in-place operations")
    output.append("  • Best for: Simple implementation")
    output.append("")

    output.append("Recursive Approach:")
    output.append("  • Time: O(n² log n) - recursive calls with sorting")
    output.append("  • Space: O(n) - recursion stack")
    output.append("  • Best for: Educational understanding")
    output.append("")

    # Algorithm insights
    output.append("=== Key Insights ===")
    output.append("1. **Max-Heap Usage**: Always process heaviest stones first")
    output.append(
        "2. **Greedy Strategy**: Local optimal choice (heaviest stones) leads to global optimum"
    )
    output.append("3. **Heap Simulation**: Python heapq is min-heap, so negate values")
    output.append("4. **Edge Cases**: Handle equal stones (both destroyed) and single stone")
    output.append("")

    # Game theory analysis
    output.append("=== Game Theory Analysis ===")
    output.append("Stone smashing follows these principles:")
    output.append("• **Deterministic**: Given stones, outcome is always the same")
    output.append("• **Greedy Optimal**: Always choosing heaviest stones is optimal")
    output.append("• **Reduction Problem**: Each step reduces problem size by 1 or 2")
    output.append("• **Invariant**: Total parity of all stones remains constant")
    output.append("")

    # Mathematical properties
    output.append("=== Mathematical Properties ===")
    output.append("Let S = sum of all stone weights:")
    output.append("• If all stones have same parity → final result has same parity as S")
    output.append("• Maximum possible result = max(stones)")
    output.append("• Minimum possible result = 0 (when stones can be paired perfectly)")
    output.append("• Result ≡ S (mod 2) - parity is preserved")
    output.append("")

    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **Resource Merging**: Combining inventory items or resources")
    output.append("• **Load Balancing**: Distributing workload by combining heavy tasks")
    output.append("• **Game Mechanics**: Turn-based games with resource consumption")
    output.append("• **Chemical Reactions**: Modeling reactions with different concentrations")
    output.append("• **Tournament Systems**: Elimination tournaments with weighted participants")

    return "\n".join(output)


def simulate_stone_smashing(stones: List[int]) -> List[str]:
    """Helper function to generate step-by-step simulation."""
    stones_copy = stones.copy()
    steps = []
    step_num = 0

    while len(stones_copy) > 1:
        step_num += 1
        stones_copy.sort(reverse=True)

        first = stones_copy[0]
        second = stones_copy[1]
        stones_copy = stones_copy[2:]

        if first == second:
            steps.append(f"Smash {first} and {second} → both destroyed, remaining: {stones_copy}")
        else:
            new_stone = abs(first - second)
            stones_copy.append(new_stone)
            stones_copy.sort(reverse=True)
            steps.append(
                f"Smash {first} and {second} → new stone {new_stone}, remaining: {stones_copy}"
            )

        # Limit steps for display
        if step_num > 10:
            steps.append("... (continuing)")
            break

    if len(stones_copy) == 1:
        steps.append(f"Final stone weight: {stones_copy[0]}")
    elif len(stones_copy) == 0:
        steps.append("All stones destroyed, result: 0")

    return steps


# Test cases
TEST_CASES = [
    TestCase(
        input_args={"stones": [2, 7, 4, 1, 8, 1]},
        expected=1,
        description="Classic example from problem statement",
    ),
    TestCase(
        input_args={"stones": [1]},
        expected=1,
        description="Single stone remains",
    ),
    TestCase(
        input_args={"stones": [3, 7, 2]},
        expected=2,
        description="Three stones with specific outcome",
    ),
    TestCase(
        input_args={"stones": [2, 2]},
        expected=0,
        description="Two equal stones destroy each other",
    ),
    TestCase(
        input_args={"stones": [10, 4, 2, 10]},
        expected=2,
        description="Duplicate heaviest stones",
    ),
    TestCase(
        input_args={"stones": [1, 2, 3, 4, 5]},
        expected=1,
        description="Sequential weights",
    ),
    TestCase(
        input_args={"stones": [20, 3, 1, 1]},
        expected=17,
        description="One dominant heavy stone",
    ),
    TestCase(
        input_args={"stones": [4, 3, 2, 1]},
        expected=0,
        description="Descending weights that cancel out",
    ),
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_data["stones"])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Heap Approach", solution.lastStoneWeight)
    run_tests("Simulation Approach", solution.lastStoneWeightSimulation)
    run_tests("Recursive Approach", solution.lastStoneWeightRecursive)

    # Run standard test framework
    run_test_cases(TEST_CASES, lambda tc: solution.lastStoneWeight(tc.input_data["stones"]))


# Register the problem
register_problem(
    slug="last_stone_weight",
    leetcode_num=1046,
    title="Last Stone Weight",
    difficulty=Difficulty.EASY,
    category=Category.HEAP,
    solution_func=lambda stones: Solution().lastStoneWeight(stones),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["array", "heap", "priority-queue"],
    notes="Heap-based simulation of stone smashing game with max-heap operations",
)
