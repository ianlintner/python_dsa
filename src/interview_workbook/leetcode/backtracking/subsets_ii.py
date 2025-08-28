"""
LeetCode 90: Subsets II

Given an integer array nums that may contain duplicates, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.

Example 1:
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]

Example 2:
Input: nums = [0]
Output: [[],[0]]

Constraints:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
"""

from typing import List
from .._runner import TestCase, run_test_cases
from .._registry import register_problem
from .._types import Category, Difficulty


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all unique subsets from array with duplicates using backtracking.
        
        Key insight: Sort array first, then skip duplicates at same recursion level.
        When we encounter a duplicate element, we only use it if we used the previous
        occurrence of the same element.
        
        Time: O(2^n * n) where n = len(nums). Each subset takes O(n) to copy.
        Space: O(n) recursion depth, O(2^n * n) for output storage.
        
        Args:
            nums: Array of integers (may contain duplicates)
            
        Returns:
            List of all unique subsets
        """
        result = []
        nums.sort()  # Sort to handle duplicates easily
        
        def backtrack(start: int, current_subset: List[int]) -> None:
            """Backtrack helper to generate all unique subsets."""
            # Add current subset to result
            result.append(current_subset[:])
            
            # Try adding each remaining element
            for i in range(start, len(nums)):
                # Skip duplicates: if current element equals previous element
                # and we're not at the start position, skip it
                # This ensures we only use duplicates in ascending order
                if i > start and nums[i] == nums[i - 1]:
                    continue
                    
                # Choose: add current element
                current_subset.append(nums[i])
                
                # Explore: recurse with next position
                backtrack(i + 1, current_subset)
                
                # Unchoose: remove current element
                current_subset.pop()
        
        backtrack(0, [])
        return result
    
    def subsetsWithDupIterative(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all unique subsets iteratively with duplicate handling.
        
        Approach: For each element, if it's a duplicate, only add to subsets
        that were created in the previous iteration (when we added the first
        occurrence of this element).
        
        Time: O(2^n * n) - same as backtracking
        Space: O(2^n * n) for storing all subsets
        """
        nums.sort()
        result = [[]]  # Start with empty subset
        
        i = 0
        while i < len(nums):
            # Count consecutive duplicates
            count = 1
            while i + count < len(nums) and nums[i + count] == nums[i]:
                count += 1
            
            # For current element, create new subsets by adding 1, 2, ..., count
            # copies to existing subsets
            prev_size = len(result)
            for c in range(1, count + 1):
                for j in range(prev_size):
                    new_subset = result[j] + [nums[i]] * c
                    result.append(new_subset)
            
            i += count
        
        return result
    
    def subsetsWithDupBitmask(self, nums: List[int]) -> List[List[int]]:
        """
        Generate subsets using bitmask approach with deduplication.
        
        Note: This approach generates all possible combinations first,
        then removes duplicates. Less efficient but demonstrates the concept.
        
        Time: O(2^n * n log(2^n)) due to sorting for deduplication
        Space: O(2^n * n) for all subsets
        """
        n = len(nums)
        result = []
        
        # Generate all possible subsets using bitmask
        for mask in range(2**n):
            subset = []
            for i in range(n):
                if mask & (1 << i):
                    subset.append(nums[i])
            result.append(sorted(subset))  # Sort for consistent comparison
        
        # Remove duplicates by converting to set of tuples
        unique_subsets = set(tuple(subset) for subset in result)
        return [list(subset) for subset in unique_subsets]


def create_demo_output() -> str:
    """
    Create comprehensive demo showing different approaches to subsets with duplicates.
    
    Returns:
        Formatted string with examples, performance analysis, and insights.
    """
    solution = Solution()
    
    demo_parts = []
    demo_parts.append("=== LeetCode 90: Subsets II - Comprehensive Demo ===\n")
    
    # Test cases with analysis
    test_cases = [
        ([1, 2, 2], "Classic case with duplicates"),
        ([0], "Single element"),
        ([1, 2, 3], "No duplicates"),
        ([4, 4, 4, 1, 4], "Multiple duplicates"),
        ([1, 1, 2, 2], "Two pairs of duplicates")
    ]
    
    for nums, description in test_cases:
        demo_parts.append(f"\nTest Case: {nums} ({description})")
        demo_parts.append(f"Input: nums = {nums}")
        
        # Show different approaches
        result1 = solution.subsetsWithDup(nums)
        result2 = solution.subsetsWithDupIterative(nums)
        result3 = solution.subsetsWithDupBitmask(nums)
        
        demo_parts.append(f"Backtracking result: {len(result1)} subsets")
        demo_parts.append(f"  {sorted(result1)}")
        demo_parts.append(f"Iterative result: {len(result2)} subsets")
        demo_parts.append(f"  {sorted(result2)}")
        demo_parts.append(f"Bitmask result: {len(result3)} subsets") 
        demo_parts.append(f"  {sorted(result3)}")
        
        # Verify all approaches give same result
        s1, s2, s3 = set(map(tuple, result1)), set(map(tuple, result2)), set(map(tuple, result3))
        demo_parts.append(f"All approaches consistent: {s1 == s2 == s3}")
    
    # Mathematical analysis
    demo_parts.append("\n=== Mathematical Analysis ===")
    demo_parts.append("For array with duplicates, subset count depends on duplicate pattern:")
    demo_parts.append("- If element appears k times, we can choose 0, 1, 2, ..., k copies")
    demo_parts.append("- Total subsets = ∏(count_i + 1) for each unique element i")
    
    # Example calculation
    nums = [1, 2, 2]
    demo_parts.append(f"\nExample: {nums}")
    demo_parts.append("- Element 1 appears 1 time → can choose 0 or 1 copy (2 choices)")
    demo_parts.append("- Element 2 appears 2 times → can choose 0, 1, or 2 copies (3 choices)")
    demo_parts.append("- Total subsets = 2 × 3 = 6")
    
    # Performance comparison
    demo_parts.append("\n=== Performance Comparison ===")
    demo_parts.append("Backtracking Approach:")
    demo_parts.append("  + Most intuitive and commonly used")
    demo_parts.append("  + Natural duplicate handling with sorting")
    demo_parts.append("  - Recursion overhead")
    
    demo_parts.append("\nIterative Approach:")
    demo_parts.append("  + No recursion overhead")
    demo_parts.append("  + Efficient duplicate handling")
    demo_parts.append("  - More complex logic")
    
    demo_parts.append("\nBitmask Approach:")
    demo_parts.append("  + Educational value")
    demo_parts.append("  - Inefficient due to duplicate generation and removal")
    demo_parts.append("  - Only practical for small inputs")
    
    # Real-world applications
    demo_parts.append("\n=== Real-World Applications ===")
    demo_parts.append("1. Feature Selection: Choose subsets of features for ML models")
    demo_parts.append("2. Resource Allocation: Different combinations of available resources")
    demo_parts.append("3. Menu Planning: Combinations of ingredients with quantity constraints")
    demo_parts.append("4. Portfolio Management: Different asset combinations")
    demo_parts.append("5. A/B Testing: Different feature combinations to test")
    
    return "\n".join(demo_parts)


# Comprehensive test cases
TEST_CASES = [
    TestCase(
        input_data={"nums": [1, 2, 2]},
        expected_output=[[],[1],[1,2],[1,2,2],[2],[2,2]],
        description="Basic case with duplicates"
    ),
    TestCase(
        input_data={"nums": [0]},
        expected_output=[[], [0]],
        description="Single element"
    ),
    TestCase(
        input_data={"nums": [1, 2, 3]},
        expected_output=[[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]],
        description="No duplicates - should work like regular subsets"
    ),
    TestCase(
        input_data={"nums": [4, 4, 4, 1, 4]},
        expected_output=[[], [1], [4], [1,4], [4,4], [1,4,4], [4,4,4], [1,4,4,4], [4,4,4,4], [1,4,4,4,4]],
        description="Many duplicates"
    ),
    TestCase(
        input_data={"nums": [1, 1, 2, 2]},
        expected_output=[[], [1], [2], [1,1], [1,2], [2,2], [1,1,2], [1,2,2], [1,1,2,2]],
        description="Two pairs of duplicates"
    ),
]


def test_solution():
    """Test the solution with all test cases."""
    def normalize_output(subsets):
        """Normalize output by sorting each subset and the list of subsets."""
        return sorted([sorted(subset) for subset in subsets])
    
    def test_function(nums):
        solution = Solution()
        result = solution.subsetsWithDup(nums)
        return normalize_output(result)
    
    # Normalize expected outputs
    normalized_test_cases = []
    for case in TEST_CASES:
        normalized_case = TestCase(
            input_data=case.input_data,
            expected_output=normalize_output(case.expected_output),
            description=case.description
        )
        normalized_test_cases.append(normalized_case)
    
    run_test_cases(test_function, normalized_test_cases)


# Register the problem
register_problem(
    slug="subsets-ii",
    leetcode_num=90,
    title="Subsets II",
    difficulty=Difficulty.MEDIUM,
    category=Category.BACKTRACKING,
    solution_func=Solution().subsetsWithDup,
    test_func=test_solution,
    demo_func=create_demo_output
)
