"""
Task Scheduler

Problem: Task Scheduler
LeetCode link: https://leetcode.com/problems/task-scheduler/
Description: Given a list of tasks represented by characters and a cooling interval n, return the least number of time units required to finish all tasks, where the same tasks must be separated by at least n time units.
"""

import heapq
import random
from collections import Counter

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._runner import TestCase
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        """
        Return the least number of intervals the CPU will take to finish all tasks.

        Uses a max heap to schedule tasks with cooling periods.
        """
        if n == 0:
            return len(tasks)

        counts = Counter(tasks)
        # max heap
        max_heap = [-cnt for cnt in counts.values()]
        heapq.heapify(max_heap)

        time = 0
        while max_heap:
            temp = []
            # fill up a cycle of length n+1
            for _ in range(n + 1):
                if max_heap:
                    cnt = heapq.heappop(max_heap)
                    if cnt + 1 < 0:
                        temp.append(cnt + 1)
                time += 1
                if not max_heap and not temp:
                    break
            for item in temp:
                heapq.heappush(max_heap, item)
        return time


# Example test cases
test_cases = [
    TestCase((["A", "A", "A", "B", "B", "B"], 2), 8, "Standard case with cooldown"),
    TestCase((["A", "A", "A", "B", "B", "B"], 0), 6, "No cooldown"),
    TestCase(
        (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2),
        16,
        "One dominant task",
    ),
]


def demo() -> str:
    """Run test cases for Task Scheduler."""
    random.seed(0)
    sol = Solution()
    outputs = []
    outputs.append("Task Scheduler | LeetCode 621")
    outputs.append("=" * 50)
    outputs.append("Time: O(n log 26) | Space: O(26)")
    outputs.append("Technique: Max-heap with cooling cycle\n")

    for case in test_cases:
        tasks, n = case.input_args
        res = sol.leastInterval(list(tasks), n)
        passed = res == case.expected
        status = "✓ PASS" if passed else "✗ FAIL"
        outputs.append(f"Test Case: {case.description}")
        outputs.append(f"  Input: tasks={list(tasks)}, n={n}")
        outputs.append(f"  Output: {res}")
        outputs.append(f"  Expected: {case.expected}")
        outputs.append(f"  {status}\n")

    result = "\n".join(outputs)
    print(result)
    return result


register_problem(
    id=621,
    slug="task_scheduler",
    title="Task Scheduler",
    category=Category.HEAP,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "hashmap", "greedy", "heap"],
    url="https://leetcode.com/problems/task-scheduler/",
    notes="",
)

if __name__ == "__main__":
    print(demo())
