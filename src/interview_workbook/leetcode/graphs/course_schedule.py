"""
Course Schedule

TODO: Add problem description
"""


from collections import defaultdict, deque

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
    """TODO: Implement demo function."""
    pass


# TODO: Register the problem with correct parameters
# register_problem(
#     id=0,
#     slug="course_schedule",
#     title="Course Schedule",
#     category=Category.UNKNOWN,
#     difficulty=Difficulty.UNKNOWN,
#     tags=[],
#     url="",
#     notes="")
