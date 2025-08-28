"""
LeetCode 207: Course Schedule

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.

Example 2:
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should
also have finished course 1. So it is impossible.

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All the pairs prerequisites[i] are unique.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determine if all courses can be completed using topological sort (Kahn's algorithm).

        Key insight: This is a cycle detection problem in a directed graph. If there's a cycle,
        some courses depend on themselves (directly or indirectly), making completion impossible.

        Approach: Use BFS-based topological sort. Start with courses that have no prerequisites
        (in-degree = 0), then gradually remove them and decrease in-degrees of dependent courses.

        Time: O(V + E) where V = numCourses, E = len(prerequisites)
        Space: O(V + E) for adjacency list and in-degree array

        Args:
            numCourses: Total number of courses (0 to numCourses-1)
            prerequisites: List of [course, prerequisite] pairs

        Returns:
            True if all courses can be completed, False if there's a cycle
        """
        from collections import defaultdict, deque

        # Build adjacency list and calculate in-degrees
        graph = defaultdict(list)  # prerequisite -> [courses that depend on it]
        in_degree = [0] * numCourses  # count of prerequisites for each course

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            in_degree[course] += 1

        # Find all courses with no prerequisites (in-degree = 0)
        queue = deque()
        for course in range(numCourses):
            if in_degree[course] == 0:
                queue.append(course)

        completed_courses = 0

        # Process courses using topological sort
        while queue:
            # Take a course with no remaining prerequisites
            current_course = queue.popleft()
            completed_courses += 1

            # Remove this course as prerequisite for its dependent courses
            for dependent_course in graph[current_course]:
                in_degree[dependent_course] -= 1

                # If dependent course now has no prerequisites, add to queue
                if in_degree[dependent_course] == 0:
                    queue.append(dependent_course)

        # If we completed all courses, there was no cycle
        return completed_courses == numCourses

    def canFinishDFS(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Cycle detection using DFS with three colors (white-gray-black).

        White (0): Unvisited node
        Gray (1): Currently being processed (in recursion stack)
        Black (2): Completely processed

        If we encounter a gray node during DFS, we found a cycle.

        Time: O(V + E)
        Space: O(V + E) for adjacency list and color array + O(V) recursion stack
        """
        from collections import defaultdict

        # Build adjacency list (prerequisite -> courses that depend on it)
        graph = defaultdict(list)
        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)

        # Color coding: 0=white (unvisited), 1=gray (processing), 2=black (done)
        color = [0] * numCourses

        def has_cycle(course: int) -> bool:
            """DFS helper to detect cycle starting from given course."""
            if color[course] == 1:  # Gray - found back edge (cycle)
                return True
            if color[course] == 2:  # Black - already processed, no cycle
                return False

            # Mark as gray (currently processing)
            color[course] = 1

            # Check all dependent courses
            for dependent in graph[course]:
                if has_cycle(dependent):
                    return True

            # Mark as black (completely processed)
            color[course] = 2
            return False

        # Check each course for cycles
        for course in range(numCourses):
            if color[course] == 0:  # Unvisited
                if has_cycle(course):
                    return False

        return True

    def canFinishUnionFind(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Alternative approach using Union-Find, though less natural for this problem.

        This approach is more complex and less efficient than topological sort,
        but demonstrates how Union-Find can be adapted for cycle detection.

        Time: O(E * α(V)) where α is inverse Ackermann function
        Space: O(V) for parent array
        """
        # Build adjacency list for DFS-based cycle detection
        from collections import defaultdict

        graph = defaultdict(list)
        for course, prerequisite in prerequisites:
            graph[course].append(prerequisite)

        # Use DFS to detect cycles in the dependency graph
        visited = [0] * numCourses  # 0=unvisited, 1=processing, 2=done

        def dfs(course: int) -> bool:
            """Returns True if cycle detected."""
            if visited[course] == 1:  # Currently processing - cycle found
                return True
            if visited[course] == 2:  # Already processed - no cycle
                return False

            visited[course] = 1  # Mark as processing

            for prerequisite in graph[course]:
                if dfs(prerequisite):
                    return True

            visited[course] = 2  # Mark as done
            return False

        # Check each course
        for course in range(numCourses):
            if visited[course] == 0:
                if dfs(course):
                    return False

        return True


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to course scheduling.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 207: Course Schedule - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        (2, [[1, 0]], "Simple linear dependency: 0 -> 1"),
        (2, [[1, 0], [0, 1]], "Circular dependency: 0 <-> 1"),
        (4, [[1, 0], [2, 1], [3, 2]], "Linear chain: 0 -> 1 -> 2 -> 3"),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], "DAG with multiple paths"),
        (3, [[0, 1], [0, 2], [1, 2]], "Multiple prerequisites for same course"),
        (1, [], "Single course with no prerequisites"),
        (3, [], "Multiple courses with no prerequisites"),
        (3, [[1, 0], [1, 2], [0, 1]], "Cycle with additional dependency"),
        (4, [[2, 0], [1, 0], [3, 1], [3, 2], [1, 3]], "Complex cycle"),
    ]

    for num_courses, prerequisites, description in test_cases:
        demo_parts.append(f"\nTest Case: {description}")
        demo_parts.append(f"Courses: {num_courses}, Prerequisites: {prerequisites}")

        # Test different approaches
        result1 = solution.canFinish(num_courses, prerequisites)
        result2 = solution.canFinishDFS(num_courses, prerequisites)
        result3 = solution.canFinishUnionFind(num_courses, prerequisites)

        demo_parts.append(f"Topological Sort (Kahn's): {result1}")
        demo_parts.append(f"DFS Cycle Detection: {result2}")
        demo_parts.append(f"Union-Find Approach: {result3}")
        demo_parts.append(f"All approaches consistent: {result1 == result2 == result3}")

        # Explain the dependency structure
        if prerequisites:
            demo_parts.append("Dependency structure:")
            for course, prereq in prerequisites:
                demo_parts.append(f"  Course {course} requires Course {prereq}")

        if not result1:
            demo_parts.append("❌ Contains cycle - impossible to complete all courses")
        else:
            demo_parts.append("✅ No cycles - all courses can be completed")

    # Algorithm analysis
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nKahn's Algorithm (Topological Sort):")
    demo_parts.append("  • Time: O(V + E) - visit each vertex and edge once")
    demo_parts.append("  • Space: O(V + E) - adjacency list + in-degree array")
    demo_parts.append("  • Pros: Intuitive, produces topological order, BFS-based")
    demo_parts.append("  • Cons: Requires extra space for in-degree tracking")

    demo_parts.append("\nDFS Cycle Detection:")
    demo_parts.append("  • Time: O(V + E) - DFS traversal of graph")
    demo_parts.append("  • Space: O(V + E) - adjacency list + color array + recursion stack")
    demo_parts.append("  • Pros: Classic cycle detection, memory efficient for sparse graphs")
    demo_parts.append("  • Cons: Recursion stack can be deep, harder to get ordering")

    demo_parts.append("\nUnion-Find Approach:")
    demo_parts.append("  • Time: O(E * α(V)) - α is inverse Ackermann")
    demo_parts.append("  • Space: O(V) - parent array only")
    demo_parts.append("  • Pros: Good for incremental updates, path compression")
    demo_parts.append("  • Cons: Unnatural for this problem, doesn't give topological order")

    # Topological sort concepts
    demo_parts.append("\n=== Topological Sort Concepts ===")
    demo_parts.append("**Definition**: Linear ordering of vertices in a DAG such that for every")
    demo_parts.append("directed edge (u,v), vertex u comes before v in the ordering.")
    demo_parts.append("")
    demo_parts.append("**Key Properties**:")
    demo_parts.append("• Only possible in Directed Acyclic Graphs (DAGs)")
    demo_parts.append("• Multiple valid orderings may exist")
    demo_parts.append("• If cycle exists, no topological ordering is possible")
    demo_parts.append("• Used for scheduling, dependency resolution, build systems")

    # Kahn's vs DFS comparison
    demo_parts.append("\n=== Kahn's Algorithm vs DFS ===")
    demo_parts.append("**Kahn's Algorithm (BFS-based)**:")
    demo_parts.append("• Start with nodes having in-degree 0")
    demo_parts.append("• Remove nodes and update in-degrees")
    demo_parts.append("• Natural for finding lexicographically smallest ordering")
    demo_parts.append("• Easy to understand and implement")
    demo_parts.append("")
    demo_parts.append("**DFS-based Topological Sort**:")
    demo_parts.append("• Use post-order DFS traversal")
    demo_parts.append("• Reverse the post-order gives topological order")
    demo_parts.append("• More memory efficient for sparse graphs")
    demo_parts.append("• Natural for recursive problems")

    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. **Course Scheduling**: University course prerequisites")
    demo_parts.append("2. **Build Systems**: Compile dependencies (Make, Maven, npm)")
    demo_parts.append("3. **Task Scheduling**: Project management with dependencies")
    demo_parts.append("4. **Package Management**: Software package dependencies")
    demo_parts.append("5. **Spreadsheet Recalculation**: Cell formula dependencies")
    demo_parts.append("6. **Symbol Resolution**: Compiler dependency analysis")
    demo_parts.append("7. **Database Query Optimization**: Join order optimization")

    # Common pitfalls and edge cases
    demo_parts.append("\n=== Common Pitfalls & Edge Cases ===")
    demo_parts.append("**Edge Cases**:")
    demo_parts.append("• No courses (numCourses = 0)")
    demo_parts.append("• No prerequisites (empty prerequisites list)")
    demo_parts.append("• Self-loops (course depends on itself)")
    demo_parts.append("• Multiple edges between same pair of courses")
    demo_parts.append("")
    demo_parts.append("**Common Mistakes**:")
    demo_parts.append("• Confusing prerequisite direction (a->b vs b->a)")
    demo_parts.append("• Not handling disconnected components")
    demo_parts.append("• Forgetting to check if all courses are processed")
    demo_parts.append("• Incorrect cycle detection in DFS")

    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        input_data={"numCourses": 2, "prerequisites": [[1, 0]]},
        expected_output=True,
        description="Simple linear dependency",
    ),
    TestCase(
        input_data={"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]},
        expected_output=False,
        description="Circular dependency",
    ),
    TestCase(
        input_data={"numCourses": 4, "prerequisites": [[1, 0], [2, 1], [3, 2]]},
        expected_output=True,
        description="Linear chain of dependencies",
    ),
    TestCase(
        input_data={"numCourses": 4, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2]]},
        expected_output=True,
        description="DAG with multiple paths",
    ),
    TestCase(
        input_data={"numCourses": 1, "prerequisites": []},
        expected_output=True,
        description="Single course with no prerequisites",
    ),
    TestCase(
        input_data={"numCourses": 3, "prerequisites": []},
        expected_output=True,
        description="Multiple courses with no prerequisites",
    ),
    TestCase(
        input_data={"numCourses": 3, "prerequisites": [[1, 0], [1, 2], [0, 1]]},
        expected_output=False,
        description="Cycle with additional dependency",
    ),
    TestCase(
        input_data={"numCourses": 3, "prerequisites": [[0, 1], [0, 2], [1, 2]]},
        expected_output=True,
        description="Multiple prerequisites for same course",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def test_function(numCourses, prerequisites):
        solution = Solution()
        return solution.canFinish(numCourses, prerequisites)

    run_test_cases(test_function, TEST_CASES)


# Register the problem
register_problem(
    slug="course-schedule",
    leetcode_num=207,
    title="Course Schedule",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=Solution().canFinish,
    test_func=test_solution,
    demo_func=create_demo_output,
)
