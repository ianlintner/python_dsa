"""
LeetCode 57: Insert Interval
https://leetcode.com/problems/insert-interval/

You are given an array of non-overlapping intervals where intervals[i] = [start_i, end_i]
represent the start and end of the ith interval and intervals is sorted in ascending order by start_i.
You are also given an interval newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by start_i
and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion.
"""

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def insert_three_pass(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        """
        Three-pass approach: before, overlapping, after.

        Strategy:
        1. Add all intervals that end before newInterval starts (no overlap)
        2. Merge all intervals that overlap with newInterval
        3. Add all intervals that start after newInterval ends (no overlap)

        Time: O(n) - single pass through all intervals
        Space: O(n) - for result array
        """
        result = []
        i = 0
        n = len(intervals)

        # 1. Add all intervals that end before newInterval starts
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # 2. Merge all overlapping intervals with newInterval
        # Start with newInterval as the base to merge
        merged_start = newInterval[0]
        merged_end = newInterval[1]

        while i < n and intervals[i][0] <= newInterval[1]:
            # Current interval overlaps with newInterval
            merged_start = min(merged_start, intervals[i][0])
            merged_end = max(merged_end, intervals[i][1])
            i += 1

        # Add the merged interval
        result.append([merged_start, merged_end])

        # 3. Add all remaining intervals (they don't overlap)
        while i < n:
            result.append(intervals[i])
            i += 1

        return result

    def insert_one_pass(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        """
        One-pass approach with state tracking.

        Time: O(n) - single pass
        Space: O(n) - result array
        """
        result = []
        placed = False

        for interval in intervals:
            if interval[1] < newInterval[0]:
                # Current interval ends before newInterval starts
                result.append(interval)
            elif interval[0] > newInterval[1]:
                # Current interval starts after newInterval ends
                if not placed:
                    result.append(newInterval)
                    placed = True
                result.append(interval)
            else:
                # Overlapping - merge with newInterval
                newInterval[0] = min(newInterval[0], interval[0])
                newInterval[1] = max(newInterval[1], interval[1])

        # If newInterval hasn't been placed yet, add it
        if not placed:
            result.append(newInterval)

        return result

    def insert_binary_search_optimized(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        """
        Binary search approach to find insertion point, then linear merge.

        Time: O(n) - merge still requires linear scan
        Space: O(n) - result array
        """
        if not intervals:
            return [newInterval]

        # Binary search for the insertion position
        left, right = 0, len(intervals) - 1
        insert_pos = len(intervals)

        while left <= right:
            mid = (left + right) // 2
            if intervals[mid][0] <= newInterval[0]:
                left = mid + 1
            else:
                insert_pos = mid
                right = mid - 1

        # Now merge from the insertion position
        result = []
        merged_interval = newInterval[:]

        # Add intervals before potential overlap
        for i in range(len(intervals)):
            if intervals[i][1] < merged_interval[0]:
                result.append(intervals[i])
            elif intervals[i][0] > merged_interval[1]:
                # No overlap, add merged interval if not added yet
                if merged_interval:
                    result.append(merged_interval)
                    merged_interval = None
                result.append(intervals[i])
            else:
                # Overlapping - merge
                merged_interval[0] = min(merged_interval[0], intervals[i][0])
                merged_interval[1] = max(merged_interval[1], intervals[i][1])

        # Add merged interval if not added yet
        if merged_interval:
            result.append(merged_interval)

        return result

    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        """Main solution using three-pass approach"""
        return self.insert_three_pass(intervals, newInterval)


def create_demo_output() -> str:
    """Generate demonstration output for Insert Interval problem"""

    examples = [
        {
            "intervals": [[1, 3], [6, 9]],
            "newInterval": [2, 5],
            "description": "Insert overlapping interval",
        },
        {
            "intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
            "newInterval": [4, 8],
            "description": "Insert merging multiple intervals",
        },
        {"intervals": [], "newInterval": [5, 7], "description": "Insert into empty array"},
        {
            "intervals": [[1, 5]],
            "newInterval": [6, 8],
            "description": "Insert non-overlapping after",
        },
        {
            "intervals": [[3, 5]],
            "newInterval": [1, 2],
            "description": "Insert non-overlapping before",
        },
    ]

    output = ["=== Insert Interval (LeetCode 57) ===\n"]
    output.append("Insert an interval into a sorted list of non-overlapping intervals\n")

    solution = Solution()

    for i, example in enumerate(examples, 1):
        intervals_orig = example["intervals"]
        new_interval = example["newInterval"]

        output.append(f"Example {i}: {example['description']}")
        output.append(f"Original intervals: {intervals_orig}")
        output.append(f"New interval to insert: {new_interval}")

        # Test three-pass approach
        intervals_copy1 = [interval[:] for interval in intervals_orig]
        result1 = solution.insert_three_pass(intervals_copy1, new_interval[:])
        output.append(f"Three-pass result: {result1}")

        # Test one-pass approach
        intervals_copy2 = [interval[:] for interval in intervals_orig]
        result2 = solution.insert_one_pass(intervals_copy2, new_interval[:])
        output.append(f"One-pass result: {result2} (should match)")

        # Test binary search approach
        intervals_copy3 = [interval[:] for interval in intervals_orig]
        result3 = solution.insert_binary_search_optimized(intervals_copy3, new_interval[:])
        output.append(f"Binary search result: {result3} (should match)")
        output.append("")

    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. Three-pass Approach:")
    output.append("   - Time: O(n), Space: O(n)")
    output.append("   - Clear logic: before, overlap, after")
    output.append("   - Most intuitive and maintainable")

    output.append("2. One-pass Approach:")
    output.append("   - Time: O(n), Space: O(n)")
    output.append("   - State-based processing")
    output.append("   - Good for streaming scenarios")

    output.append("3. Binary Search + Merge:")
    output.append("   - Time: O(n), Space: O(n)")
    output.append("   - Optimizes finding insertion point")
    output.append("   - Still needs linear scan for merging")

    output.append("\nKey Insight: Linear merge is unavoidable")
    output.append("Pattern: Process intervals in three phases")

    # Edge cases demonstration
    output.append("\n=== Edge Cases ===")
    edge_cases = [
        ([], [1, 2], "Empty input"),
        ([[1, 3]], [0, 0], "Point interval before"),
        ([[1, 3]], [4, 4], "Point interval after"),
        ([[1, 3]], [2, 2], "Point interval overlapping"),
        ([[1, 3], [6, 9]], [4, 5], "Insert between existing intervals"),
        ([[1, 2], [3, 5], [6, 7]], [0, 10], "New interval covers all existing"),
    ]

    for intervals, new_interval, description in edge_cases:
        result = solution.insert([interval[:] for interval in intervals], new_interval[:])
        output.append(f"{description}: {intervals} + {new_interval} -> {result}")

    return "\n".join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data=([[1, 3], [6, 9]], [2, 5]),
        expected=[[1, 5], [6, 9]],
        description="Insert overlapping with first interval",
    ),
    TestCase(
        input_data=([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
        expected=[[1, 2], [3, 10], [12, 16]],
        description="Insert merging multiple intervals",
    ),
    TestCase(input_data=([], [5, 7]), expected=[[5, 7]], description="Insert into empty array"),
    TestCase(
        input_data=([[1, 5]], [6, 8]),
        expected=[[1, 5], [6, 8]],
        description="Insert non-overlapping after",
    ),
    TestCase(
        input_data=([[3, 5]], [1, 2]),
        expected=[[1, 2], [3, 5]],
        description="Insert non-overlapping before",
    ),
    TestCase(
        input_data=([[1, 3]], [2, 2]),
        expected=[[1, 3]],
        description="Insert point interval that overlaps",
    ),
    TestCase(
        input_data=([[1, 2], [3, 5], [6, 7]], [0, 10]),
        expected=[[0, 10]],
        description="New interval covers all existing",
    ),
    TestCase(
        input_data=([[1, 5]], [0, 3]),
        expected=[[0, 5]],
        description="Partial overlap extending start",
    ),
]


def test_solution():
    """Test function for Insert Interval"""
    solution = Solution()

    def test_insert(test_data, expected, description):
        intervals, new_interval = test_data
        # Create copies to avoid modifying original data
        intervals_copy = [interval[:] for interval in intervals]
        new_interval_copy = new_interval[:]
        result = solution.insert(intervals_copy, new_interval_copy)
        return result == expected

    test_cases_formatted = [
        TestCase(input_data=tc.input_data, expected=tc.expected, description=tc.description)
        for tc in TEST_CASES
    ]

    return run_test_cases(test_insert, test_cases_formatted)


# Register the problem
register_problem(
    slug="insert_interval",
    leetcode_num=57,
    title="Insert Interval",
    difficulty=Difficulty.MEDIUM,
    category=Category.INTERVALS,
    solution_func=lambda intervals, newInterval: Solution().insert(intervals, newInterval),
    test_func=test_solution,
    demo_func=create_demo_output,
)
