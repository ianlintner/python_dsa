"""
LeetCode 252: Meeting Rooms
https://leetcode.com/problems/meeting-rooms/

Given an array of meeting time intervals where intervals[i] = [start_i, end_i], 
determine if a person could attend all meetings.
"""

from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def canAttendMeetings_sort_and_check(self, intervals: list[list[int]]) -> bool:
        """
        Sort intervals by start time and check for overlaps.
        
        Strategy:
        1. Sort intervals by start time
        2. Check each adjacent pair for overlap
        3. Return false if any overlap found
        
        Time: O(n log n) - sorting dominates
        Space: O(1) - excluding input
        """
        if len(intervals) <= 1:
            return True
        
        # Sort by start time
        intervals.sort(key=lambda x: x[0])
        
        # Check each adjacent pair for overlap
        for i in range(1, len(intervals)):
            # If previous meeting ends after current meeting starts
            if intervals[i-1][1] > intervals[i][0]:
                return False  # Overlap found
        
        return True

    def canAttendMeetings_optimized(self, intervals: list[list[int]]) -> bool:
        """
        Optimized version with early termination.
        
        Time: O(n log n) - sorting
        Space: O(1) - excluding input
        """
        if len(intervals) <= 1:
            return True
        
        # Sort by start time
        intervals.sort()
        
        # Check for overlaps with single loop
        for i in range(1, len(intervals)):
            if intervals[i-1][1] > intervals[i][0]:
                return False
        
        return True

    def canAttendMeetings_brute_force(self, intervals: list[list[int]]) -> bool:
        """
        Brute force approach: Check every pair of intervals.
        
        Time: O(n²) - check all pairs
        Space: O(1) - no extra space
        """
        n = len(intervals)
        
        for i in range(n):
            for j in range(i + 1, n):
                # Check if intervals i and j overlap
                start1, end1 = intervals[i]
                start2, end2 = intervals[j]
                
                # Two intervals overlap if one starts before the other ends
                if max(start1, start2) < min(end1, end2):
                    return False
        
        return True

    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        """Main solution using sort and check approach"""
        return self.canAttendMeetings_sort_and_check(intervals)


def create_demo_output() -> str:
    """Generate demonstration output for Meeting Rooms problem"""
    
    examples = [
        {
            "input": [[0,30],[5,10],[15,20]],
            "description": "Overlapping meetings - cannot attend all"
        },
        {
            "input": [[7,10],[2,4]],
            "description": "Non-overlapping meetings - can attend all"
        },
        {
            "input": [],
            "description": "No meetings - can attend all"
        },
        {
            "input": [[1,5]],
            "description": "Single meeting - can attend"
        },
        {
            "input": [[1,4],[4,5]],
            "description": "Adjacent meetings (touching) - can attend"
        },
        {
            "input": [[1,5],[2,3],[4,6]],
            "description": "Multiple overlaps - cannot attend"
        }
    ]
    
    output = ["=== Meeting Rooms (LeetCode 252) ===\n"]
    output.append("Determine if a person can attend all meetings (no overlaps)\n")
    
    solution = Solution()
    
    for i, example in enumerate(examples, 1):
        original_intervals = example["input"][:]
        
        output.append(f"Example {i}: {example['description']}")
        output.append(f"Meeting intervals: {original_intervals}")
        
        # Test sort and check approach
        intervals_copy1 = [interval[:] for interval in original_intervals]
        result1 = solution.canAttendMeetings_sort_and_check(intervals_copy1)
        output.append(f"Sort & check result: {result1}")
        
        # Show sorted intervals for clarity
        if original_intervals:
            sorted_intervals = sorted(original_intervals)
            output.append(f"Sorted intervals: {sorted_intervals}")
            
            # Show overlap analysis
            overlaps = []
            for j in range(1, len(sorted_intervals)):
                if sorted_intervals[j-1][1] > sorted_intervals[j][0]:
                    overlaps.append(f"{sorted_intervals[j-1]} overlaps with {sorted_intervals[j]}")
            
            if overlaps:
                output.append(f"Overlaps found: {'; '.join(overlaps)}")
            else:
                output.append("No overlaps found")
        
        # Test optimized approach
        intervals_copy2 = [interval[:] for interval in original_intervals]
        result2 = solution.canAttendMeetings_optimized(intervals_copy2)
        output.append(f"Optimized result: {result2} (should match)")
        
        # Test brute force (for smaller examples)
        if len(original_intervals) <= 5:
            intervals_copy3 = [interval[:] for interval in original_intervals]
            result3 = solution.canAttendMeetings_brute_force(intervals_copy3)
            output.append(f"Brute force result: {result3} (should match)")
        
        output.append("")
    
    # Algorithm comparison
    output.append("=== Algorithm Analysis ===")
    output.append("1. Sort and Check:")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Most efficient for this problem")
    output.append("   - Sort enables linear scan for overlaps")
    
    output.append("2. Optimized Sort:")
    output.append("   - Time: O(n log n), Space: O(1)")
    output.append("   - Same complexity, cleaner code")
    output.append("   - Uses default sort (by start time)")
    
    output.append("3. Brute Force:")
    output.append("   - Time: O(n²), Space: O(1)")
    output.append("   - Check all pairs directly")
    output.append("   - Good for understanding overlap condition")
    
    output.append("\nKey Insight: Sorting enables efficient overlap detection")
    output.append("Pattern: Sort by start time, check adjacent pairs")
    
    # Overlap condition explanation
    output.append("\n=== Overlap Detection ===")
    output.append("Two intervals [a,b] and [c,d] overlap if:")
    output.append("- max(a,c) < min(b,d)")
    output.append("- Equivalent: a < d AND c < b")
    output.append("- For sorted intervals: previous_end > current_start")
    
    output.append("\nNote: Intervals [a,b] and [b,c] do NOT overlap")
    output.append("(touching at endpoints is allowed)")
    
    return '\n'.join(output)


# Test cases
TEST_CASES = [
    TestCase(
        input_data=[[0,30],[5,10],[15,20]],
        expected=False,
        description="Overlapping meetings"
    ),
    TestCase(
        input_data=[[7,10],[2,4]],
        expected=True,
        description="Non-overlapping meetings"
    ),
    TestCase(
        input_data=[],
        expected=True,
        description="No meetings"
    ),
    TestCase(
        input_data=[[1,5]],
        expected=True,
        description="Single meeting"
    ),
    TestCase(
        input_data=[[1,4],[4,5]],
        expected=True,
        description="Adjacent meetings (touching endpoints)"
    ),
    TestCase(
        input_data=[[1,5],[2,3],[4,6]],
        expected=False,
        description="Multiple overlapping meetings"
    ),
    TestCase(
        input_data=[[1,2],[3,4],[5,6]],
        expected=True,
        description="All non-overlapping"
    ),
    TestCase(
        input_data=[[1,3],[2,4]],
        expected=False,
        description="Simple overlap case"
    ),
    TestCase(
        input_data=[[0,1],[1,2],[2,3],[3,4]],
        expected=True,
        description="Chain of adjacent meetings"
    )
]


def test_solution():
    """Test function for Meeting Rooms"""
    solution = Solution()
    
    def test_can_attend_meetings(intervals, expected, description):
        # Create copy to avoid modifying original
        intervals_copy = [interval[:] for interval in intervals]
        result = solution.canAttendMeetings(intervals_copy)
        return result == expected
    
    test_cases_formatted = [
        TestCase(
            input_data=tc.input_data,
            expected=tc.expected,
            description=tc.description
        ) for tc in TEST_CASES
    ]
    
    return run_test_cases(test_can_attend_meetings, test_cases_formatted)


# Register the problem
register_problem(
    slug="meeting_rooms",
    leetcode_num=252,
    title="Meeting Rooms",
    difficulty=Difficulty.EASY,
    category=Category.INTERVALS,
    solution_func=Solution().canAttendMeetings,
