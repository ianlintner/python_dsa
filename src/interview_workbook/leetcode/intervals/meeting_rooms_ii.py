"""
LeetCode 253: Meeting Rooms II

Given an array of meeting time intervals intervals where intervals[i] = [starti, endi],
return the minimum number of conference rooms required.

Examples:
    Input: intervals = [[0,30],[5,10],[15,20]]
    Output: 2

    Input: intervals = [[7,10],[2,4]]
    Output: 1

Constraints:
    1 <= intervals.length <= 10^4
    0 <= starti < endi <= 10^6
"""

import heapq
from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Find minimum number of meeting rooms using min-heap approach.

        Algorithm:
        1. Sort intervals by start time
        2. Use min-heap to track end times of ongoing meetings
        3. For each meeting:
           - If heap is empty or current start < earliest end, need new room
           - Otherwise, reuse room by removing earliest end time
           - Add current meeting's end time to heap
        4. Heap size represents number of rooms needed

        Time Complexity: O(n log n) - sorting + heap operations
        Space Complexity: O(n) - heap storage
        """
        if not intervals:
            return 0

        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        # Min-heap to store end times of ongoing meetings
        heap = []

        for start, end in intervals:
            # If current meeting starts after earliest meeting ends,
            # we can reuse that room
            if heap and start >= heap[0]:
                heapq.heappop(heap)

            # Add current meeting's end time
            heapq.heappush(heap, end)

        # Number of rooms equals heap size
        return len(heap)

    def minMeetingRoomsEvents(self, intervals: List[List[int]]) -> int:
        """
        Alternative approach using event points (sweep line).

        Algorithm:
        1. Create events for each start (+1) and end (-1)
        2. Sort events by time (end events before start for same time)
        3. Sweep through events tracking concurrent meetings
        4. Maximum concurrent meetings = minimum rooms needed

        Time Complexity: O(n log n) - sorting events
        Space Complexity: O(n) - events array
        """
        if not intervals:
            return 0

        events = []
        for start, end in intervals:
            events.append((start, 1))  # Meeting starts
            events.append((end, -1))  # Meeting ends

        # Sort by time, with end events (-1) before start events (1) for same time
        events.sort(key=lambda x: (x[0], x[1]))

        concurrent_meetings = 0
        max_rooms = 0

        for time, event_type in events:
            concurrent_meetings += event_type
            max_rooms = max(max_rooms, concurrent_meetings)

        return max_rooms

    def minMeetingRoomsBruteForce(self, intervals: List[List[int]]) -> int:
        """
        Brute force approach checking all time points.

        Algorithm:
        1. For each unique time point, count overlapping meetings
        2. Return maximum count

        Time Complexity: O(n²) - for each interval, check all others
        Space Complexity: O(n) - to store time points
        """
        if not intervals:
            return 0

        # Get all unique time points
        times = set()
        for start, end in intervals:
            times.add(start)
            times.add(end)

        max_rooms = 0
        for time in times:
            # Count meetings active at this time
            active_meetings = 0
            for start, end in intervals:
                if start <= time < end:
                    active_meetings += 1
            max_rooms = max(max_rooms, active_meetings)

        return max_rooms


def create_demo_output() -> str:
    """Create comprehensive demo showing different approaches and analysis."""
    solution = Solution()

    # Test cases for demonstration
    test_cases = [
        ([[0, 30], [5, 10], [15, 20]], "Basic overlapping meetings"),
        ([[7, 10], [2, 4]], "Non-overlapping meetings"),
        ([[1, 2], [2, 3], [3, 4]], "Adjacent meetings"),
        ([[9, 10], [4, 9], [4, 17]], "Multiple overlaps"),
        ([[1, 5], [8, 9], [8, 9]], "Same time meetings"),
        ([[0, 30]], "Single meeting"),
        ([], "No meetings"),
    ]

    output = []
    output.append("=== LeetCode 253: Meeting Rooms II ===\n")

    for intervals, desc in test_cases:
        if not intervals:
            continue

        output.append(f"Test: {desc}")
        output.append(f"Input: intervals = {intervals}")

        # Test all three approaches
        result1 = solution.minMeetingRooms(intervals.copy() if intervals else [])
        result2 = solution.minMeetingRoomsEvents(intervals.copy() if intervals else [])
        result3 = solution.minMeetingRoomsBruteForce(intervals.copy() if intervals else [])

        output.append(f"Min-Heap approach: {result1}")
        output.append(f"Events approach: {result2}")
        output.append(f"Brute Force approach: {result3}")
        output.append("")

    # Performance analysis
    output.append("=== Algorithm Comparison ===")
    output.append("Min-Heap Approach:")
    output.append("  • Time: O(n log n) - Sort intervals + heap operations")
    output.append("  • Space: O(n) - Heap storage")
    output.append("  • Best for: General case, intuitive room allocation")
    output.append("")

    output.append("Events (Sweep Line) Approach:")
    output.append("  • Time: O(n log n) - Sort events")
    output.append("  • Space: O(n) - Events array")
    output.append("  • Best for: Understanding overlap patterns")
    output.append("")

    output.append("Brute Force Approach:")
    output.append("  • Time: O(n²) - Check all time points")
    output.append("  • Space: O(n) - Time points set")
    output.append("  • Best for: Small inputs, educational purposes")
    output.append("")

    # Algorithm insights
    output.append("=== Key Insights ===")
    output.append("1. **Room Reuse**: A room becomes available when a meeting ends")
    output.append("2. **Optimal Scheduling**: Always reuse the earliest available room")
    output.append("3. **Peak Concurrency**: Maximum rooms needed = maximum concurrent meetings")
    output.append("4. **Event Processing**: Start/end events help track concurrency changes")
    output.append("")

    # Real-world applications
    output.append("=== Real-World Applications ===")
    output.append("• **Resource Allocation**: Conference rooms, equipment scheduling")
    output.append("• **CPU Scheduling**: Process scheduling with resource constraints")
    output.append("• **Event Management**: Managing simultaneous events")
    output.append("• **Capacity Planning**: Server resources, bandwidth allocation")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_args=([[0, 30], [5, 10], [15, 20]],),
        expected=2,
        description="Basic overlapping meetings - need 2 rooms",
    ),
    TestCase(
        input_args=([[7, 10], [2, 4]],),
        expected=1,
        description="Non-overlapping meetings - need 1 room",
    ),
    TestCase(
        input_args=([[1, 2], [2, 3], [3, 4]],),
        expected=1,
        description="Adjacent meetings (end time = start time) - need 1 room",
    ),
    TestCase(
        input_args=([[9, 10], [4, 9], [4, 17]],),
        expected=2,
        description="Multiple overlapping patterns",
    ),
    TestCase(
        input_args=([[1, 5], [8, 9], [8, 9]],),
        expected=2,
        description="Same time meetings - need 2 rooms",
    ),
    TestCase(
        input_args=([[0, 30]],),
        expected=1,
        description="Single meeting - need 1 room",
    ),
    TestCase(
        input_args=([],),
        expected=0,
        description="No meetings - need 0 rooms",
    ),
    TestCase(
        input_args=([[1, 3], [2, 4], [3, 5], [4, 6]],),
        expected=2,
        description="Overlapping chain of meetings",
    ),
    TestCase(
        input_args=([[1, 10], [2, 3], [4, 5], [6, 7], [8, 9]],),
        expected=2,
        description="One long meeting with multiple short ones inside",
    ),
]


def test_solution():
    """Test all solution approaches."""
    solution = Solution()

    def run_tests(func_name: str, func):
        print(f"\nTesting {func_name}:")
        for i, test_case in enumerate(TEST_CASES):
            intervals_copy = test_case.input_args[0].copy()
            result = func(intervals_copy)
            status = "✓" if result == test_case.expected else "✗"
            print(f"  Test {i + 1}: {status} - {test_case.description}")
            if result != test_case.expected:
                print(f"    Expected: {test_case.expected}, Got: {result}")

    run_tests("Min-Heap Approach", solution.minMeetingRooms)
    run_tests("Events Approach", solution.minMeetingRoomsEvents)
    run_tests("Brute Force Approach", solution.minMeetingRoomsBruteForce)

    # Run standard test framework
    run_test_cases(
        solution.minMeetingRooms,
        TEST_CASES,
        "Meeting Rooms II",
    )


# Register the problem
register_problem(
    slug="meeting_rooms_ii",
    leetcode_num=253,
    title="Meeting Rooms II",
    difficulty=Difficulty.MEDIUM,
    category=Category.INTERVALS,
    solution_func=lambda intervals: Solution().minMeetingRooms(intervals),
    test_func=test_solution,
    demo_func=create_demo_output,
    tags=["intervals", "heap", "sorting", "greedy", "sweep-line"],
    notes="Classic interval scheduling problem with multiple approaches",
)
