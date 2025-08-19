"""
Longest Consecutive Sequence - LeetCode Problem

Given an unsorted array of integers nums, return the length of the longest consecutive
elements sequence.

You must write an algorithm that runs in O(n) time.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        Find longest consecutive sequence using hash set for O(n) solution.

        Time Complexity: O(n) - each element visited at most twice
        Space Complexity: O(n) - hash set storage

        Args:
            nums: List of integers

        Returns:
            int: Length of longest consecutive sequence
        """
        if not nums:
            return 0

        num_set = set(nums)
        longest_streak = 0

        for num in num_set:
            # Only start counting from the beginning of a sequence
            # If num-1 exists, then num is not the start of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                # Count consecutive numbers starting from current_num
                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                longest_streak = max(longest_streak, current_streak)

        return longest_streak

    def longestConsecutiveSorting(self, nums: List[int]) -> int:
        """
        Alternative solution using sorting (not O(n) but simpler logic).

        Time Complexity: O(n log n) - sorting dominates
        Space Complexity: O(1) - in-place operations after sorting
        """
        if not nums:
            return 0

        nums.sort()
        longest_streak = 1
        current_streak = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:  # Skip duplicates
                if nums[i] == nums[i - 1] + 1:  # Consecutive
                    current_streak += 1
                else:  # Not consecutive, reset streak
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1

        return max(longest_streak, current_streak)

    def longestConsecutiveUnionFind(self, nums: List[int]) -> int:
        """
        Alternative using Union-Find (educational - not optimal for this problem).

        Time Complexity: O(n α(n)) - where α is inverse Ackermann function
        Space Complexity: O(n) - Union-Find structure
        """
        if not nums:
            return 0

        # Simple Union-Find implementation
        parent = {}
        size = {}

        def find(x):
            if x not in parent:
                parent[x] = x
                size[x] = 1
                return x

            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)

            if root_x != root_y:
                # Union by size
                if size[root_x] < size[root_y]:
                    root_x, root_y = root_y, root_x
                parent[root_y] = root_x
                size[root_x] += size[root_y]

        # Initialize all numbers
        num_set = set(nums)
        for num in num_set:
            find(num)

        # Union consecutive numbers
        for num in num_set:
            if num + 1 in num_set:
                union(num, num + 1)

        # Find maximum component size
        return max(size[find(num)] for num in num_set)


def demo():
    """Demonstrate Longest Consecutive Sequence solution with test cases."""
    solution = Solution()

    test_cases = [
        TestCase(
            input_args=([100, 4, 200, 1, 3, 2],),
            expected=4,
            description="Basic case - sequence [1,2,3,4]",
        ),
        TestCase(
            input_args=([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],),
            expected=9,
            description="Long sequence [0,1,2,3,4,5,6,7,8]",
        ),
        TestCase(
            input_args=([1, 2, 0, 1],), expected=3, description="With duplicates - sequence [0,1,2]"
        ),
        TestCase(
            input_args=([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],),
            expected=7,
            description="Negative numbers - sequence [-1,0,1,3,4,5,6]",
        ),
        TestCase(input_args=([]), expected=0, description="Empty array"),
        TestCase(input_args=([1]), expected=1, description="Single element"),
        TestCase(input_args=([1, 3, 5, 7]), expected=1, description="No consecutive numbers"),
        TestCase(
            input_args=([2, 20, 4, 10, 3, 4, 5]),
            expected=4,
            description="Sequence [2,3,4,5] with duplicates",
        ),
    ]

    results = run_test_cases(solution.longestConsecutive, test_cases)

    return create_demo_output(
        title="Longest Consecutive Sequence",
        description="Find longest consecutive sequence using hash set",
        results=results,
        complexity_analysis={
            "time": "O(n) - each element visited at most twice",
            "space": "O(n) - hash set storage for all unique elements",
        },
        key_insights=[
            "Hash set provides O(1) lookup to check consecutive numbers",
            "Only start counting from sequence beginnings (num-1 not in set)",
            "Each number is visited at most twice (once in outer loop, once in inner)",
            "Sorting approach is simpler but O(n log n) time complexity",
        ],
        common_pitfalls=[
            "Remember to handle duplicates correctly",
            "Only start sequences from the beginning (optimization key)",
            "Empty array edge case returns 0",
            "Don't count the same sequence multiple times",
        ],
        follow_up_questions=[
            "How would you handle very large integers?",
            "Can you find all consecutive sequences, not just the longest?",
            "What if you need to return the actual sequence, not just length?",
            "How would you optimize for mostly consecutive arrays?",
        ],
    )


# Register this problem
register_problem(
    id=128,
    slug="longest-consecutive-sequence",
    title="Longest Consecutive Sequence",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags={"array", "hash-table", "union-find"},
    module="src.interview_workbook.leetcode.arrays_hashing.longest_consecutive_sequence",
    url="https://leetcode.com/problems/longest-consecutive-sequence/",
    notes="Hash set approach for O(n) consecutive sequence detection",
)
