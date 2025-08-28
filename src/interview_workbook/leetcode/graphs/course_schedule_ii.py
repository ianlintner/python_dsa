"""
LeetCode 210: Course Schedule II

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you
must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return the ordering of courses you should take to finish all courses. If there are many valid
answers, return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished
course 0. So the correct course order is [0,1].

Example 2:
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished
both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,2,1,3]. Another correct ordering is [0,1,2,3].

Example 3:
Input: numCourses = 1, prerequisites = []
Output: [0]

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- ai != bi
- All the pairs prerequisites[i] are unique.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase
from .._types import Category, Difficulty


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Find a valid course ordering using topological sort (Kahn's algorithm).

        This extends Course Schedule I by returning the actual ordering instead of just
        checking if completion is possible.

        Time: O(V + E) where V = numCourses, E = len(prerequisites)
        Space: O(V + E) for adjacency list, in-degree array, and result list

        Args:
            numCourses: Total number of courses (0 to numCourses-1)
            prerequisites: List of [course, prerequisite] pairs

        Returns:
            Valid course ordering, or empty list if impossible
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

        course_order = []

        # Process courses using topological sort
        while queue:
            # Take a course with no remaining prerequisites
            current_course = queue.popleft()
            course_order.append(current_course)

            # Remove this course as prerequisite for its dependent courses
            for dependent_course in graph[current_course]:
                in_degree[dependent_course] -= 1

                # If dependent course now has no prerequisites, add to queue
                if in_degree[dependent_course] == 0:
                    queue.append(dependent_course)

        # Return ordering if all courses processed, empty list if cycle exists
        return course_order if len(course_order) == numCourses else []

    def findOrderDFS(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Find course ordering using DFS-based topological sort.

        Uses post-order DFS traversal. The reverse of post-order gives topological order.
        Also detects cycles using three-color approach.

        Time: O(V + E)
        Space: O(V + E) for adjacency list + O(V) for recursion and result
        """
        from collections import defaultdict

        # Build adjacency list (prerequisite -> courses that depend on it)
        graph = defaultdict(list)
        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)

        # Color coding: 0=white (unvisited), 1=gray (processing), 2=black (done)
        color = [0] * numCourses
        post_order = []
        has_cycle = False

        def dfs(course: int) -> None:
            """DFS helper for topological sort with cycle detection."""
            nonlocal has_cycle

            if has_cycle:  # Early termination if cycle found
                return

            if color[course] == 1:  # Gray - found back edge (cycle)
                has_cycle = True
                return

            if color[course] == 2:  # Black - already processed
                return

            # Mark as gray (currently processing)
            color[course] = 1

            # Visit all dependent courses
            for dependent in graph[course]:
                dfs(dependent)

            # Mark as black (completely processed) and add to post-order
            color[course] = 2
            post_order.append(course)

        # Visit all courses to handle disconnected components
        for course in range(numCourses):
            if color[course] == 0:  # Unvisited
                dfs(course)

        # Return reverse of post-order if no cycle, empty list otherwise
        return post_order[::-1] if not has_cycle else []

    def findOrderLexicographical(
        self, numCourses: int, prerequisites: List[List[int]]
    ) -> List[int]:
        """
        Find lexicographically smallest valid ordering using modified Kahn's algorithm.

        Instead of using a queue (FIFO), use a min-heap to always process the
        smallest numbered course first among those with in-degree 0.

        Time: O(V log V + E) due to heap operations
        Space: O(V + E)
        """
        import heapq
        from collections import defaultdict

        # Build adjacency list and calculate in-degrees
        graph = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            in_degree[course] += 1

        # Use min-heap instead of queue for lexicographic ordering
        heap = []
        for course in range(numCourses):
            if in_degree[course] == 0:
                heapq.heappush(heap, course)

        course_order = []

        while heap:
            # Always take the smallest numbered course
            current_course = heapq.heappop(heap)
            course_order.append(current_course)

            # Process dependent courses
            for dependent_course in graph[current_course]:
                in_degree[dependent_course] -= 1

                if in_degree[dependent_course] == 0:
                    heapq.heappush(heap, dependent_course)

        return course_order if len(course_order) == numCourses else []


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to course ordering.

    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()

    demo_parts = []
    demo_parts.append("=== LeetCode 210: Course Schedule II - Comprehensive Demo ===\n")

    # Test cases with detailed analysis
    test_cases = [
        (2, [[1, 0]], "Simple linear dependency"),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], "DAG with multiple valid orderings"),
        (1, [], "Single course with no prerequisites"),
        (3, [], "Multiple courses with no prerequisites"),
        (2, [[1, 0], [0, 1]], "Circular dependency (impossible)"),
        (4, [[1, 0], [2, 1], [3, 2]], "Linear chain"),
        (6, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3], [5, 4]], "Complex DAG"),
        (3, [[0, 1], [0, 2], [1, 2]], "Multiple prerequisites for same course"),
    ]

    for num_courses, prerequisites, description in test_cases:
        demo_parts.append(f"\nTest Case: {description}")
        demo_parts.append(f"Courses: {num_courses}, Prerequisites: {prerequisites}")

        # Test different approaches
        result1 = solution.findOrder(num_courses, prerequisites)
        result2 = solution.findOrderDFS(num_courses, prerequisites)
        result3 = solution.findOrderLexicographical(num_courses, prerequisites)

        demo_parts.append(f"Kahn's Algorithm: {result1}")
        demo_parts.append(f"DFS-based: {result2}")
        demo_parts.append(f"Lexicographical: {result3}")

        # Verify all results are valid (same length indicates same success/failure)
        valid_lengths = [len(result1), len(result2), len(result3)]
        consistent = len(set(valid_lengths)) == 1
        demo_parts.append(f"All approaches consistent: {consistent}")

        if result1:
            # Verify it's a valid topological ordering
            def is_valid_ordering(order, prereqs):
                pos = {course: i for i, course in enumerate(order)}
                return all(pos[prereq] < pos[course] for course, prereq in prereqs)

            valid = is_valid_ordering(result1, prerequisites)
            demo_parts.append(f"✅ Valid topological ordering: {valid}")
        else:
            demo_parts.append("❌ No valid ordering exists (contains cycle)")

    # Algorithm comparison
    demo_parts.append("\n=== Algorithm Analysis ===")

    demo_parts.append("\nKahn's Algorithm (BFS-based):")
    demo_parts.append("  • Time: O(V + E) - optimal for topological sort")
    demo_parts.append("  • Space: O(V + E) - adjacency list + queue")
    demo_parts.append("  • Pros: Intuitive, produces one valid ordering")
    demo_parts.append("  • Cons: Ordering depends on queue processing order")

    demo_parts.append("\nDFS-based Topological Sort:")
    demo_parts.append("  • Time: O(V + E) - single DFS traversal")
    demo_parts.append("  • Space: O(V + E) - adjacency list + recursion stack")
    demo_parts.append("  • Pros: Memory efficient, natural recursive structure")
    demo_parts.append("  • Cons: Requires post-order reversal, deeper recursion")

    demo_parts.append("\nLexicographically Smallest:")
    demo_parts.append("  • Time: O(V log V + E) - heap operations add log factor")
    demo_parts.append("  • Space: O(V + E) - same as Kahn's + heap")
    demo_parts.append("  • Pros: Deterministic output, smallest course numbers first")
    demo_parts.append("  • Cons: Slower due to heap operations")

    # Key differences from Course Schedule I
    demo_parts.append("\n=== Differences from Course Schedule I ===")
    demo_parts.append("1. **Return Value**: Course Schedule I returns boolean, II returns ordering")
    demo_parts.append("2. **Space Requirement**: Need to store the actual ordering")
    demo_parts.append("3. **Multiple Solutions**: Many valid orderings may exist")
    demo_parts.append("4. **Output Format**: Empty array indicates impossibility")

    # Applications and variations
    demo_parts.append("\n=== Topological Sort Applications ===")
    demo_parts.append("1. **Task Scheduling**: Project management with dependencies")
    demo_parts.append("2. **Build Systems**: Determining compilation order")
    demo_parts.append("3. **Curriculum Planning**: Course sequencing in education")
    demo_parts.append("4. **Package Installation**: Resolving software dependencies")
    demo_parts.append("5. **Database Operations**: Transaction ordering")
    demo_parts.append("6. **Symbol Resolution**: Compiler dependency analysis")

    # Implementation tips
    demo_parts.append("\n=== Implementation Tips ===")
    demo_parts.append("1. **Cycle Detection**: Essential - return empty array if cycle exists")
    demo_parts.append("2. **Multiple Orderings**: Problem may have many valid solutions")
    demo_parts.append("3. **Isolated Nodes**: Handle courses with no dependencies")
    demo_parts.append("4. **Edge Direction**: Prerequisite → Course (not Course → Prerequisite)")
    demo_parts.append("5. **Validation**: Verify result length equals numCourses")

    return "\n".join(demo_parts)


# Test cases
TEST_CASES = [
    TestCase(
        input_data={"numCourses": 2, "prerequisites": [[1, 0]]},
        expected_output=[0, 1],
        description="Simple linear dependency",
    ),
    TestCase(
        input_data={"numCourses": 4, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2]]},
        expected_output=[0, 1, 2, 3],  # One possible valid ordering
        description="DAG with multiple valid orderings",
    ),
    TestCase(
        input_data={"numCourses": 1, "prerequisites": []},
        expected_output=[0],
        description="Single course with no prerequisites",
    ),
    TestCase(
        input_data={"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]},
        expected_output=[],
        description="Circular dependency (impossible)",
    ),
    TestCase(
        input_data={"numCourses": 3, "prerequisites": []},
        expected_output=[0, 1, 2],  # Any permutation is valid
        description="Multiple courses with no prerequisites",
    ),
]


def test_solution():
    """Test the solution with all test cases."""

    def is_valid_topological_order(
        order: List[int], num_courses: int, prerequisites: List[List[int]]
    ) -> bool:
        """Verify if the given order is a valid topological ordering."""
        if len(order) != num_courses:
            return len(order) == 0  # Empty array is valid only if impossible

        # Check if it contains all courses
        if set(order) != set(range(num_courses)):
            return False

        # Check if prerequisite order is respected
        position = {course: i for i, course in enumerate(order)}
        return all(position[prereq] < position[course] for course, prereq in prerequisites)

    def test_function(numCourses, prerequisites):
        solution = Solution()
        result = solution.findOrder(numCourses, prerequisites)
        return (
            result if is_valid_topological_order(result, numCourses, prerequisites) else "INVALID"
        )

    # Modified test cases to check validity rather than exact match
    modified_cases = []
    for case in TEST_CASES:
        expected = case.expected_output
        # For valid cases, we just need to verify the structure
        modified_case = TestCase(
            input_data=case.input_data,
            expected_output=expected if expected else [],  # Keep empty for impossible cases
            description=case.description,
        )
        modified_cases.append(modified_case)

    def validate_test_function(numCourses, prerequisites):
        solution = Solution()
        result = solution.findOrder(numCourses, prerequisites)
        return is_valid_topological_order(result, numCourses, prerequisites)

    # Run custom validation instead of exact matching
    print("Testing Course Schedule II...")
    for case in modified_cases:
        args = case.input_data
        is_valid = validate_test_function(**args)
        expected_valid = len(case.expected_output) > 0 or (
            len(case.expected_output) == 0 and "impossible" in case.description.lower()
        )

        status = "✅ PASS" if is_valid == expected_valid else "❌ FAIL"
        print(f"{status}: {case.description}")


# Register the problem
register_problem(
    slug="course-schedule-ii",
    leetcode_num=210,
    title="Course Schedule II",
    difficulty=Difficulty.MEDIUM,
    category=Category.GRAPHS,
    solution_func=Solution().findOrder,
    test_func=test_solution,
    demo_func=create_demo_output,
)
