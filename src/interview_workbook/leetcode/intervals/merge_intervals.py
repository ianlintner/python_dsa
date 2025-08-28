"""
LeetCode 56: Merge Intervals
https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [start_i, end_i], 
merge all overlapping intervals, and return an array of the non-overlapping intervals 
that cover all the intervals in the input.
"""

from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def merge_sort_and_merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Sort intervals by start time then merge overlapping ones.
        
        Strategy:
        1. Sort intervals by start time
        2. Iterate through sorted intervals
        3. If current interval overlaps with last merged, extend the end
        4. Otherwise, add current interval to result
        
        Time: O(n log n) - sorting dominates
        Space: O(1) - excluding output array
        """
        if not intervals:
            return []
        
        # Sort by start time
        intervals.sort(key=lambda x: x[0])
        
        merged = [intervals[0]]
        
        for current in intervals[1:]:
            last_merged = merged[-1]
            
            # Check if current overlaps with last merged interval
            if current[0] <= last_merged[1]:
                # Overlapping - merge by extending the end time
                last_merged[1] = max(last_merged[1], current[1])
            else:
                # No overlap - add current interval
                merged.append(current)
        
        return merged

    def merge_one_pass_optimized(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Optimized version with single pass after sorting.
        
        Time: O(n log n) - sorting
        Space: O(1) - excluding output
        """
        if not intervals:
            return []
        
        intervals.sort()
        result = []
        
        for interval in intervals:
            # If result is empty or no overlap with last interval
            if not result or result[-1][1] < interval[0]:
                result.append(interval)
            else:
                # Overlapping - merge by updating end time
                result[-1][1] = max(result[-1][1], interval[1])
        
        return result

    def merge_stack_based(self, intervals: list[list[int]]) -> list[list[int]]:
        """
        Stack-based approach for merging intervals.
        
        Time: O(n log n) - sorting
        Space: O(n) - stack storage
        """
        if not intervals:
            return []
        
        intervals.sort()
        stack = [intervals[0]]
        
        for i in range(1, len(intervals)):
            top = stack[-1]
            current = intervals[i]
            
            # If intervals don't overlap
            if top[1] < current[0]:
                stack.append(current)
            else:
                # Overlapping - merge intervals
                stack[-1] = [top[0], max(top[1], current[1])]
        
        return stack

    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        """Main solution using sort and merge approach"""
        return self.merge_sort_and_merge(intervals)


def create_demo_output() -> str:
    """Generate demonstration output for Merge Intervals problem"""
    
    examples = [
        {
            "input": [[1,3],[2,6],[8,10],[15,18]],
            "description": "Standard case with overlapping intervals"
        },
        {
            "input": [[1,4],[4,5]],
