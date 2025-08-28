"""
Longest Consecutive Sequence - LeetCode Problem

Given an unsorted array of integers nums, return the length of the longest consecutive
elements sequence.

You must write an algorithm that runs in O(n) time.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
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
        input_args=input_args=([100, 4, 200, 1, 3, 2],,
    ),
            expected=4,
            description="Basic case - sequence [1,2,3,4]",
        ),
        TestCase(
        input_args=input_args=([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],,
    ),
            expected=9,
            description="Long sequence [0,1,2,3,4,5,6,7,8]",
        ),
        TestCase(
        input_args=input_args=([1, 2, 0, 1],,
    ), expected=3, description="With duplicates - sequence [0,1,2]"
        ),
        TestCase(
        input_args=input_args=([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],,
    ),
            expected=7,
            description="Negative numbers - sequence [-1,0,1,3,4,5,6]",
        ),
        TestCase(
        input_args=input_args=([],,
    ), expected=0, description="Empty array"),
        TestCase(
        input_args=input_args=([1],,
    ), expected=1, description="Single element"),
        TestCase(
        input_args=input_args=([1, 3, 5, 7],,
    ), expected=1, description="No consecutive numbers"),
        TestCase(
        input_args=input_args=([2, 20, 4, 10, 3, 4, 5],
    ),
            expected=4,
            description="Sequence [2,3,4,5] with duplicates",
        ),
    ]

    # Execute test cases manually
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()

            nums = test_case.input_args[0]
            actual = solution.longestConsecutive(nums)

            end_time = time.perf_counter()

            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": f"nums={nums}",
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": actual == test_case.expected,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": f"nums={test_case.input_args[0]}",
                    "expected": test_case.expected,
                    "actual": f"Error: {str(e)}",
                    "passed": False,
                    "time_ms": 0,
                }
            )

    # Format results as test results string
    test_results_lines = ["=== Longest Consecutive Sequence ===", ""]
    passed_count = 0
    total_time = sum(r["time_ms"] for r in results)

    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: {result['expected']}")
        test_results_lines.append(f"  Got: {result['actual']}")
        test_results_lines.append(f"  Time: {result['time_ms']:.3f}ms")
        test_results_lines.append("")
        if result["passed"]:
            passed_count += 1

    test_results_lines.append(f"Results: {passed_count}/{len(results)} passed")
    test_results_lines.append(f"Total time: {total_time:.3f}ms")

    if passed_count == len(results):
        test_results_lines.append("🎉 All tests passed!")
    else:
        test_results_lines.append(f"❌ {len(results) - passed_count} test(s) failed")

    test_results_str = "\n".join(test_results_lines)

    approach_notes = """
Key Insights:
• Hash set provides O(1) lookup to check consecutive numbers
• Only start counting from sequence beginnings (num-1 not in set)
• Each number is visited at most twice (once in outer loop, once in inner)
• Sorting approach is simpler but O(n log n) time complexity

Common Pitfalls:
• Remember to handle duplicates correctly
• Only start sequences from the beginning (optimization key)
• Empty array edge case returns 0
• Don't count the same sequence multiple times

Follow-up Questions:
• How would you handle very large integers?
• Can you find all consecutive sequences, not just the longest?
• What if you need to return the actual sequence, not just length?
• How would you optimize for mostly consecutive arrays?
"""

    return create_demo_output(
        problem_title="Longest Consecutive Sequence",
        test_results=test_results_str,
        time_complexity="O(n) - each element visited at most twice",
        space_complexity="O(n) - hash set storage for all unique elements",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=128,
    slug="longest-consecutive-sequence",
    title="Longest Consecutive Sequence",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hash-table", "union-find"],
    url="https://leetcode.com/problems/longest-consecutive-sequence/",
    notes="Hash set approach for O(n) consecutive sequence detection",
)
