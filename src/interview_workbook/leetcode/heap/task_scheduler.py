"""
LeetCode 621: Task Scheduler

You are given an array of CPU tasks, each represented by letters A to Z, and a cooling time, n.
Each cycle, the CPU can complete a task or be idle. Tasks can be completed in any order,
but there's a constraint: identical tasks must be separated by at least n intervals due to cooling time.

Return the minimum number of intervals required to complete all tasks.

Examples:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B

    Input: tasks = ["A","A","A","B","B","B"], n = 0
    Output: 6
    Explanation: No cooling time, so tasks can be completed immediately

    Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
    Output: 16

Constraints:
    1 <= tasks.length <= 10^4
    tasks[i] is an uppercase English letter.
    0 <= n <= 100
"""

import heapq
from collections import Counter, deque
from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Find minimum intervals using heap-based greedy approach.

        Algorithm:
        1. Count task frequencies using Counter
        2. Use max-heap to always process most frequent tasks first
        3. Use queue to track tasks in cooling period
        4. Each cycle: process available task or idle

        Time Complexity: O(m log k) where m is total intervals, k is unique tasks
        Space Complexity: O(k) for heap and queue
        """
        if n == 0:
            # No cooling time needed
            return len(tasks)

        # Count task frequencies
        task_counts = Counter(tasks)

        # Max-heap (use negative values for max behavior)
        max_heap = [-count for count in task_counts.values()]
        heapq.heapify(max_heap)

        # Queue to track tasks in cooling period: (count, available_time)
        cooling_queue = deque()

        time = 0

        while max_heap or cooling_queue:
            time += 1

            # Check if any task finished cooling
            if cooling_queue and cooling_queue[0][1] <= time:
                count, _ = cooling_queue.popleft()
                heapq.heappush(max_heap, count)

            # Process most frequent available task
            if max_heap:
                count = heapq.heappop(max_heap)
                count += 1  # Decrease count (was negative)

                # If task has more instances, add to cooling queue
                if count < 0:
                    cooling_queue.append((count, time + n + 1))
            # else: CPU is idle this cycle

        return time

    def leastIntervalMath(self, tasks: List[str], n: int) -> int:
        """
        Mathematical approach using task frequency analysis.

        Key insight: The bottleneck is the most frequent task and cooling time.

        Algorithm:
        1. Find the most frequent task count (max_freq)
        2. Count how many tasks have max frequency (max_count)
        3. Calculate minimum time based on most frequent task slots
        4. Return max of calculated time and total tasks

        Time Complexity: O(k) where k is unique tasks
        Space Complexity: O(k) for counter
        """
        if n == 0:
            return len(tasks)

        # Count task frequencies
        task_counts = Counter(tasks)
        max_freq = max(task_counts.values())
        max_count = sum(1 for count in task_counts.values() if count == max_freq)

        # The most frequent task creates (max_freq - 1) complete cycles
        # Each cycle needs (n + 1) time slots
        # Plus the final execution of max_count tasks
        min_time = (max_freq - 1) * (n + 1) + max_count

        # The actual time is at least the total number of tasks
        return max(min_time, len(tasks))

    def leastIntervalSimulation(self, tasks: List[str], n: int) -> int:
        """
        Direct simulation approach for understanding.

        Algorithm:
        1. Track when each task type can next be executed
        2. At each time step, execute the most frequent available task
        3. Continue until all tasks are completed

        Time Complexity: O(m) where m is total execution time
        Space Complexity: O(k) for task tracking
        """
        if n == 0:
            return len(tasks)

        task_counts = Counter(tasks)
        task_next_time = {task: 0 for task in task_counts}

        time = 0
        remaining_tasks = len(tasks)

        while remaining_tasks > 0:
            # Find the most frequent task that can be executed now
            best_task = None
            max_count = 0

            for task, count in task_counts.items():
                if count > 0 and task_next_time[task] <= time:
                    if count > max_count:
                        max_count = count
                        best_task = task

            if best_task:
                # Execute the best task
                task_counts[best_task] -= 1
                task_next_time[best_task] = time + n + 1
                remaining_tasks -= 1

            time += 1

        return time


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    # Test cases for demonstration
    test_cases = [
        (["A", "A", "A", "B", "B", "B"], 2, "Basic alternating pattern"),
        (["A", "A", "A", "B", "B", "B"], 0, "No cooling time needed"),
        (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2, "One dominant task"),
        (["A", "B", "C", "D", "E", "F"], 2, "All different tasks"),
        (["A", "A", "B", "B"], 1, "Two pairs with minimal cooling"),
    ]

    output = []
    output.append("=== LeetCode 621: Task Scheduler ===\n")

    for tasks, n, desc in test_cases:
        output.append(f"Test: {desc}")
        output.append(f"Input: tasks = {tasks}, n = {n}")

        # Show task analysis
        task_counts = Counter(tasks)
        output.append(f"Task frequencies: {dict(task_counts)}")

        # Test all approaches
        result1 = solution.leastInterval(tasks, n)
        result2 = solution.leastIntervalMath(tasks, n)
        result3 = solution.leastIntervalSimulation(tasks, n)

        output.append(f"Heap approach: {result1} intervals")
        output.append(f"Math approach: {result2} intervals")
        output.append(f"Simulation: {result3} intervals")

        # Show scheduling pattern for small examples
        if len(tasks) <= 10:
            output.append("Optimal schedule visualization:")
            schedule = simulate_schedule(tasks, n)
            output.append(f"  {' -> '.join(schedule)}")

        output.append("")

    # Performance analysis
    output.append("=== Performance Analysis ===")
    output.append("Heap-based Approach:")
    output.append("  • Time: O(m log k) - m intervals, k unique tasks")
    output.append("  • Space: O(k) - heap and cooling queue")
    output.append("  • Best for: Understanding the scheduling process")
    output.append("")

    output.append("Mathematical Approach:")
    output.append("  • Time: O(k) - count tasks and find maximum")
    output.append("  • Space: O(k) - task counter only")
    output.append("  • Best for: Optimal time and space complexity")
    output.append("")

    output.append("Simulation Approach:")
    output.append("  • Time: O(m) - simulate each time step")
    output.append("  • Space: O(k) - task tracking")
    output.append("  • Best for: Detailed schedule generation")
    output.append("")

    # Algorithm insights
    output.append("=== Key Insights ===")
    output.append("1. **Greedy Strategy**: Always schedule most frequent available task")
    output.append("2. **Math Optimization**: Most frequent task determines minimum time")
    output.append("3. **Cooling Management**: Track when each task becomes available")
    output.append("4. **Idle Time**: Occurs when no tasks are available due to cooling")
    output.append("")

    # Mathematical formula explanation
    output.append("=== Mathematical Formula ===")
    output.append("For tasks with max frequency `max_freq` appearing `max_count` times:")
    output.append("  • Complete cycles: (max_freq - 1)")
    output.append("  • Time per cycle: (n + 1)")
    output.append("  • Final execution: max_count")
    output.append("  • Formula: max((max_freq-1)*(n+1)+max_count, total_tasks)")
    output.append("")

    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **CPU Scheduling**: Process scheduling with resource constraints")
    output.append("• **Manufacturing**: Machine scheduling with setup/cooldown times")
    output.append("• **Resource Management**: Server request handling with rate limiting")
    output.append("• **Task Queues**: Job scheduling with dependency constraints")
    output.append("• **Cache Management**: Request scheduling to avoid cache conflicts")

    return "\n".join(output)


def simulate_schedule(tasks: List[str], n: int) -> List[str]:
    """Helper function to generate actual schedule for visualization."""
    if n == 0:
        return tasks

    task_counts = Counter(tasks)
    task_next_time = {task: 0 for task in task_counts}
    schedule = []
    time = 0

    while sum(task_counts.values()) > 0:
        best_task = None
        max_count = 0

        for task, count in task_counts.items():
            if count > 0 and task_next_time[task] <= time:
                if count > max_count:
                    max_count = count
                    best_task = task

        if best_task:
            schedule.append(best_task)
            task_counts[best_task] -= 1
            task_next_time[best_task] = time + n + 1
        else:
            schedule.append("idle")

        time += 1

        # Limit schedule length for display
        if len(schedule) > 20:
            schedule.append("...")
            break

    return schedule


# Test cases
TEST_CASES = [
    TestCase(
        input_data={"tasks": ["A", "A", "A", "B", "B", "B"], "n": 2},
        expected=8,
        description="Basic example with alternating pattern",
    ),
    TestCase(
        input_data={"tasks": ["A", "A", "A", "B", "B", "B"], "n": 0},
        expected=6,
        description="No cooling time - execute immediately",
    ),
    TestCase(
        input_data={"tasks": ["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], "n": 2},
        expected=16,
        description="One task dominates frequency",
    ),
    TestCase(
        input_data={"tasks": ["A", "B", "C", "D", "E", "F"], "n": 2},
        expected=6,
        description="All different tasks",
    ),
    TestCase(
        input_data={"tasks": ["A", "A", "B", "B"], "n": 1},
        expected=4,
        description="Two pairs with minimal cooling",
    ),
    TestCase(input_data={"tasks": ["A"], "n": 1}, expected=1, description="Single task"),
    TestCase(
        input_data={"tasks": ["A", "A"], "n": 3},
        expected=5,
        description="Same task with large cooling time",
    ),
    TestCase(
        input_data={"tasks": ["A", "B", "A", "B", "A", "B"], "n": 0},
        expected=6,
        description="Alternating tasks with no cooling",
    ),
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            result = func(test_case.input_data["tasks"], test_case.input_data["n"])
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Heap Approach", solution.leastInterval)
    run_tests("Math Approach", solution.leastIntervalMath)
    run_tests("Simulation Approach", solution.leastIntervalSimulation)

    # Run standard test framework
    run_test_cases(
        TEST_CASES, lambda tc: solution.leastInterval(tc.input_data["tasks"], tc.input_data["n"])
    )


# Register the problem
register_problem(
    slug="task_scheduler",
    leetcode_num=621,
    title="Task Scheduler",
    difficulty=Difficulty.MEDIUM,
    category=Category.HEAP,
    solution_func=lambda tasks, n: Solution().leastInterval(tasks, n),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["array", "hash-table", "greedy", "sorting", "heap", "counting"],
    notes="Greedy scheduling problem using heap for optimal task ordering",
)
