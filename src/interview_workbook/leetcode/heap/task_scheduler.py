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
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def least_interval(self, tasks: list[str], n: int) -> int:
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


def demo() -> str:
    """Demonstration of Task Scheduler algorithm with deterministic seeding."""
    random.seed(0)
    tasks = ["A", "A", "A", "B", "B", "B"]
    n = 2
    sol = Solution()
    result = sol.least_interval(tasks, n)
    return f"Tasks: {tasks}, Cooling: {n}, Minimum intervals: {result}"


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
