"""
Course Schedule Ii

TODO: Add problem description
"""

from collections import defaultdict, deque

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, numCourses, prerequisites):
        """Topological sort: return valid order of courses or [] if impossible."""
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for dest, src in prerequisites:
            graph[src].append(dest)
            indegree[dest] += 1

        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        order = []

        while queue:
            course = queue.popleft()
            order.append(course)
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    queue.append(nei)

        return order if len(order) == numCourses else []


def demo():
    """Run a demo for the Course Schedule II problem."""
    solver = Solution()
    numCourses = 4
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    result = solver.solve(numCourses, prerequisites)
    return str(result)


register_problem(
    id=210,
    slug="course_schedule_ii",
    title="Course Schedule II",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["dfs", "bfs", "graph", "topological_sort"],
    url="https://leetcode.com/problems/course-schedule-ii/",
    notes="",
)
