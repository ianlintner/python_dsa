"""
 Runner

TODO: Add problem description
"""

from typing import Any, Callable, List


class TestCase:
    __test__ = False  # prevent pytest from collecting this as a test

    def __init__(self, input_args: tuple, expected: Any, description: str = ""):
        self.input_args = input_args
        self.expected = expected
        self.description = description


def run_test_cases(
    func: Callable, test_cases: List[TestCase], title: str, show_details: bool = False
) -> str:
    """Run a list of test cases and return formatted results string."""
    results = []
    passed = 0
    all_fail = True
    for _i, case in enumerate(test_cases, start=1):
        try:
            result = func(*case.input_args)
            if result == case.expected:
                results.append(f"✓ PASS - {case.description}")
                passed += 1
                all_fail = False
            else:
                results.append(
                    f"✗ FAIL - {case.description}: expected {case.expected}, got {result}"
                )
        except Exception as e:
            results.append(f"✗ FAIL - {case.description}: raised exception {e}")
    if all_fail and test_cases:
        results.append("No passing tests ❌")

    summary = f"{title}: {passed}/{len(test_cases)} passed"
    if passed == len(test_cases):
        summary += " - All tests passed"
    elif passed == 0 and test_cases:
        summary += " - All tests failed"
    else:
        summary += f" - {len(test_cases) - passed} test(s) failed"

    if show_details:
        results_str = "\n".join(results)
        return f"{summary}\n{results_str}"
    # Always include ✓ PASS markers for any passing test
    if passed > 0:
        results.append("✓ PASS")
    return summary if not results else f"{summary}\n" + "\n".join(results)


def create_demo_output(
    problem_name: str,
    test_results: str,
    time_complexity: str,
    space_complexity: str,
    approach_notes: str,
) -> str:
    """Format demo output with problem info, results, and complexity analysis."""
    return (
        f"Problem: {problem_name}\n"
        f"Time: {time_complexity}, Space: {space_complexity}\n"
        f"Approach: {approach_notes}\n"
        f"{test_results}"
    )
