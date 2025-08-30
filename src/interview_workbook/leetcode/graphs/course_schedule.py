"""
Course Schedule

TODO: Add problem description
"""

from collections import defaultdict, deque

from src.interview_workbook.leetcode._registry import register_problem
from src.interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def solve(self, numCourses, prerequisites):
        """Detect cycle in course prerequisite graph (Kahn's algorithm)."""
        graph = defaultdict(list)
        indegree = [0] * numCourses
        for dest, src in prerequisites:
            graph[src].append(dest)
            indegree[dest] += 1

        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        visited = 0

        while queue:
            course = queue.popleft()
            visited += 1
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    queue.append(nei)
        return visited == numCourses


def demo():
    """Run a demo for the Course Schedule problem."""
    solver = Solution()
    numCourses = 2
    prerequisites = [[1, 0]]
    result = solver.solve(numCourses, prerequisites)
    return str(result)


register_problem(
    id=207,
    slug="course_schedule",
    title="Course Schedule",
    category=Category.GRAPHS,
    difficulty=Difficulty.MEDIUM,
    tags=["dfs", "bfs", "graph", "topological_sort"],
    url="https://leetcode.com/problems/course-schedule/",
    notes="",
)
