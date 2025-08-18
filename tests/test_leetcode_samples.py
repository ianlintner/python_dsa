"""
Tests for LeetCode problem sample cases and demo functionality.
"""

import pytest

from interview_workbook.leetcode._runner import run_test_cases, TestCase


def test_two_sum_samples():
    """Test Two Sum problem with its sample cases."""
    from interview_workbook.leetcode.arrays_hashing.two_sum import Solution, test_cases
    
    solution = Solution()
    
    # Run all test cases
    for test_case in test_cases:
        result = solution.twoSum(*test_case.input_args)
        assert result == test_case.expected, f"Failed on {test_case.description}"
    
    # Test specific cases
    assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert solution.twoSum([3, 2, 4], 6) == [1, 2]
    assert solution.twoSum([3, 3], 6) == [0, 1]


def test_valid_palindrome_samples():
    """Test Valid Palindrome problem with its sample cases."""
    from interview_workbook.leetcode.two_pointers.valid_palindrome import Solution, test_cases
    
    solution = Solution()
    
    # Run all test cases
    for test_case in test_cases:
        result = solution.isPalindrome(*test_case.input_args)
        assert result == test_case.expected, f"Failed on {test_case.description}"
    
    # Test specific cases
    assert solution.isPalindrome("A man, a plan, a canal: Panama") == True
    assert solution.isPalindrome("race a car") == False
    assert solution.isPalindrome("") == True
    assert solution.isPalindrome("a") == True


def test_best_time_to_buy_sell_stock_samples():
    """Test Best Time to Buy and Sell Stock problem with its sample cases."""
    from interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock import Solution, test_cases
    
    solution = Solution()
    
    # Run all test cases
    for test_case in test_cases:
        result = solution.maxProfit(*test_case.input_args)
        assert result == test_case.expected, f"Failed on {test_case.description}"
    
    # Test specific cases  
    assert solution.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert solution.maxProfit([7, 6, 4, 3, 1]) == 0
    assert solution.maxProfit([1, 2]) == 1


def test_demo_functions_run():
    """Test that demo functions execute without errors."""
    # Import and run each demo
    from interview_workbook.leetcode.arrays_hashing import two_sum
    from interview_workbook.leetcode.two_pointers import valid_palindrome
    from interview_workbook.leetcode.sliding_window import best_time_to_buy_sell_stock
    
    # Each demo should return a string and not raise exceptions
    result1 = two_sum.demo()
    assert isinstance(result1, str)
    assert "Two Sum" in result1
    assert "✓ PASS" in result1 or "All tests passed" in result1
    
    result2 = valid_palindrome.demo()
    assert isinstance(result2, str)
    assert "Valid Palindrome" in result2
    assert "✓ PASS" in result2 or "All tests passed" in result2
    
    result3 = best_time_to_buy_sell_stock.demo()
    assert isinstance(result3, str)
    assert "Best Time to Buy and Sell Stock" in result3
    assert "✓ PASS" in result3 or "All tests passed" in result3


def test_test_runner_infrastructure():
    """Test the TestCase and run_test_cases infrastructure."""
    # Create a simple test function
    def add(a: int, b: int) -> int:
        return a + b
    
    # Create test cases
    test_cases = [
        TestCase((2, 3), 5, "Basic addition"),
        TestCase((0, 0), 0, "Zero addition"),
        TestCase((-1, 1), 0, "Negative addition"),
    ]
    
    # Run the test cases
    results = run_test_cases(add, test_cases, "Addition Test", show_details=True)
    
    # Verify results format
    assert isinstance(results, str)
    assert "Addition Test" in results
    assert "3/3 passed" in results
    assert "All tests passed" in results


def test_test_case_failures():
    """Test that test runner correctly identifies failures."""
    def always_returns_zero(x: int) -> int:
        return 0
    
    test_cases = [
        TestCase((5,), 0, "Should pass"),
        TestCase((3,), 3, "Should fail"),  
    ]
    
    results = run_test_cases(always_returns_zero, test_cases, "Failure Test")
    
    assert "1/2 passed" in results
    assert "1 test(s) failed" in results
    assert "✓ PASS" in results  # At least one should pass
    assert "✗ FAIL" in results  # At least one should fail


@pytest.mark.parametrize("problem_module,expected_demo_content", [
    ("interview_workbook.leetcode.arrays_hashing.two_sum", ["Two Sum", "O(n)", "hashmap"]),
    ("interview_workbook.leetcode.two_pointers.valid_palindrome", ["Valid Palindrome", "O(n)", "two pointers"]),
    ("interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock", ["Best Time", "O(n)", "sliding window"]),
])
def test_demo_content_quality(problem_module, expected_demo_content):
    """Test that demos contain expected educational content."""
    import importlib
    
    module = importlib.import_module(problem_module)
    demo_output = module.demo()
    
    # Check for expected content (case insensitive)
    demo_lower = demo_output.lower()
    for expected in expected_demo_content:
        assert expected.lower() in demo_lower, f"Demo missing expected content: {expected}"
    
    # Should contain complexity analysis
    assert "time:" in demo_lower
    assert "space:" in demo_lower
    
    # Should show test results
    assert "test case" in demo_lower
    

def test_solution_classes_exist():
    """Test that all seed problems have Solution classes with expected methods."""
    from interview_workbook.leetcode.arrays_hashing import two_sum
    from interview_workbook.leetcode.two_pointers import valid_palindrome 
    from interview_workbook.leetcode.sliding_window import best_time_to_buy_sell_stock
    
    # Two Sum
    assert hasattr(two_sum, 'Solution')
    solution1 = two_sum.Solution()
    assert hasattr(solution1, 'twoSum')
    assert callable(solution1.twoSum)
    
    # Valid Palindrome
    assert hasattr(valid_palindrome, 'Solution')
    solution2 = valid_palindrome.Solution()
    assert hasattr(solution2, 'isPalindrome')
    assert callable(solution2.isPalindrome)
    
    # Best Time to Buy and Sell Stock
    assert hasattr(best_time_to_buy_sell_stock, 'Solution')
    solution3 = best_time_to_buy_sell_stock.Solution()
    assert hasattr(solution3, 'maxProfit')
    assert callable(solution3.maxProfit)


def test_edge_cases():
    """Test edge cases for the implemented problems."""
    from interview_workbook.leetcode.arrays_hashing.two_sum import Solution as TwoSumSolution
    from interview_workbook.leetcode.two_pointers.valid_palindrome import Solution as PalindromeSolution
    from interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock import Solution as StockSolution
    
    # Two Sum edge cases
    two_sum = TwoSumSolution()
    # Should handle minimum case
    result = two_sum.twoSum([1, 2], 3)
    assert result == [0, 1]
    
    # Palindrome edge cases
    palindrome = PalindromeSolution()
    assert palindrome.isPalindrome("") == True  # Empty string
    assert palindrome.isPalindrome("a") == True  # Single char
    assert palindrome.isPalindrome(".,") == True  # Non-alphanumeric only
    
    # Stock edge cases  
    stock = StockSolution()
    assert stock.maxProfit([]) == 0  # Empty array
    assert stock.maxProfit([5]) == 0  # Single price
    assert stock.maxProfit([5, 5, 5]) == 0  # No profit opportunity


def test_test_case_descriptions():
    """Test that test cases have meaningful descriptions."""
    from interview_workbook.leetcode.arrays_hashing.two_sum import test_cases as two_sum_cases
    from interview_workbook.leetcode.two_pointers.valid_palindrome import test_cases as palindrome_cases
    from interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock import test_cases as stock_cases
    
    all_test_cases = two_sum_cases + palindrome_cases + stock_cases
    
    for test_case in all_test_cases:
        assert test_case.description  # Non-empty description
        assert len(test_case.description) > 5  # Reasonable length
        assert test_case.description[0].isupper()  # Starts with capital letter
