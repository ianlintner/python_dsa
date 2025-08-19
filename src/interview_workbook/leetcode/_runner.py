"""
Common runner utilities for LeetCode problem demos and testing.
"""

import importlib
import time
from typing import Any, Callable

from ._registry import by_slug
from ._types import ProblemMeta


class TestCase:
    """Represents a single test case with input, expected output, and description."""

    def __init__(self, input_args: tuple[Any, ...], expected: Any, description: str = ""):
        self.input_args = input_args
        self.expected = expected
        self.description = description

    def __repr__(self) -> str:
        return f"TestCase({self.input_args}, expected={self.expected}, desc='{self.description}')"


def run_test_case(
    solution_method: Callable[..., Any], test_case: TestCase, show_timing: bool = True
) -> tuple[Any, bool, float]:
    """
    Run a single test case against a solution method.

    Args:
        solution_method: The solution method to test
        test_case: The test case to run
        show_timing: Whether to measure execution time

    Returns:
        Tuple of (result, passed, execution_time_ms)
    """
    start_time = time.perf_counter() if show_timing else 0

    try:
        result = solution_method(*test_case.input_args)
        execution_time = (time.perf_counter() - start_time) * 1000 if show_timing else 0
        passed = result == test_case.expected
        return result, passed, execution_time
    except Exception as e:
        execution_time = (time.perf_counter() - start_time) * 1000 if show_timing else 0
        print(f"Exception during execution: {e}")
        return str(e), False, execution_time


def run_test_cases(
    solution_method: Callable[..., Any],
    test_cases: list[TestCase],
    problem_title: str = "",
    show_details: bool = True,
) -> str:
    """
    Run multiple test cases and return formatted results.

    Args:
        solution_method: The solution method to test
        test_cases: List of test cases to run
        problem_title: Title of the problem for display
        show_details: Whether to show detailed output

    Returns:
        Formatted string with test results
    """
    if not test_cases:
        return "No test cases provided."

    results = []
    passed_count = 0
    total_time = 0.0

    if problem_title:
        results.append(f"=== {problem_title} ===")
    results.append("")

    for i, test_case in enumerate(test_cases, 1):
        result, passed, exec_time = run_test_case(solution_method, test_case)
        total_time += exec_time

        if passed:
            passed_count += 1
            status = "✓ PASS"
        else:
            status = "✗ FAIL"

        if show_details:
            results.append(f"Test Case {i}: {status}")
            if test_case.description:
                results.append(f"  Description: {test_case.description}")
            results.append(f"  Input: {test_case.input_args}")
            results.append(f"  Expected: {test_case.expected}")
            results.append(f"  Got: {result}")
            results.append(f"  Time: {exec_time:.3f}ms")
            results.append("")

    # Summary
    results.append(f"Results: {passed_count}/{len(test_cases)} passed")
    results.append(f"Total time: {total_time:.3f}ms")

    if passed_count == len(test_cases):
        results.append("🎉 All tests passed!")
    else:
        results.append(f"❌ {len(test_cases) - passed_count} test(s) failed")

    return "\n".join(results)


def run_problem_demo(slug: str) -> str:
    """
    Run the demo for a specific problem by slug.

    Args:
        slug: The problem slug identifier

    Returns:
        Demo output as string

    Raises:
        ValueError: If problem not found
        ImportError: If module cannot be imported
    """
    problem = by_slug(slug)
    if not problem:
        raise ValueError(f"Problem with slug '{slug}' not found in registry")

    try:
        # Import the problem module
        module = importlib.import_module(problem["module"])

        # Get the demo function
        if not hasattr(module, "demo"):
            raise ImportError(f"Module {problem['module']} does not have a demo() function")

        # Run the demo
        return module.demo()

    except ImportError as e:
        raise ImportError(f"Failed to import problem module {problem['module']}: {e}") from e


def get_solution_class(problem: ProblemMeta) -> type:
    """
    Get the Solution class for a given problem.

    Args:
        problem: Problem metadata

    Returns:
        The Solution class from the problem module

    Raises:
        ImportError: If module or Solution class cannot be found
    """
    try:
        module = importlib.import_module(problem["module"])

        if not hasattr(module, "Solution"):
            raise ImportError(f"Module {problem['module']} does not have a Solution class")

        return module.Solution

    except ImportError as e:
        raise ImportError(f"Failed to import Solution from {problem['module']}: {e}") from e


def format_complexity_info(time_complexity: str, space_complexity: str) -> str:
    """Format complexity information for display."""
    return f"""
Complexity Analysis:
  Time: {time_complexity}
  Space: {space_complexity}
"""


def create_demo_output(
    problem_title: str,
    test_results: str,
    time_complexity: str = "",
    space_complexity: str = "",
    approach_notes: str = "",
) -> str:
    """
    Create standardized demo output format.

    Args:
        problem_title: Title of the problem
        test_results: Results from running test cases
        time_complexity: Time complexity description
        space_complexity: Space complexity description
        approach_notes: Additional notes about the approach

    Returns:
        Formatted demo output
    """
    output = [test_results]

    if time_complexity and space_complexity:
        output.append(format_complexity_info(time_complexity, space_complexity))

    if approach_notes:
        output.append(f"Approach Notes:\n{approach_notes}")

    return "\n".join(output)
