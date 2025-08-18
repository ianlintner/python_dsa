"""
Permutation in String - LeetCode Problem

Given two strings s1 and s2, return true if s2 contains a permutation of s1, 
or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.
"""

from collections import Counter
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """
        Check if s2 contains a permutation of s1 using sliding window.
        
        Time Complexity: O(n + m) - where n is len(s1), m is len(s2)
        Space Complexity: O(1) - at most 26 characters in frequency maps
        
        Args:
            s1: Pattern string
            s2: Text string to search in
            
        Returns:
            bool: True if s2 contains a permutation of s1, False otherwise
        """
        if len(s1) > len(s2):
            return False
        
        # Create frequency maps
        s1_count = Counter(s1)
        window_count = Counter()
        
        window_size = len(s1)
        
        # Initialize first window
        for i in range(window_size):
            window_count[s2[i]] += 1
        
        # Check if first window matches
        if window_count == s1_count:
            return True
        
        # Slide the window
        for i in range(window_size, len(s2)):
            # Add new character to window
            window_count[s2[i]] += 1
            
            # Remove character going out of window
            left_char = s2[i - window_size]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
            
            # Check if current window matches
            if window_count == s1_count:
                return True
        
        return False
    
    def checkInclusionArray(self, s1: str, s2: str) -> bool:
        """
        Alternative using fixed-size arrays for character counting.
        
        Time Complexity: O(n + m) - single pass through both strings
        Space Complexity: O(1) - fixed size arrays
        """
        if len(s1) > len(s2):
            return False
        
        # Use arrays for character frequency (assuming lowercase letters)
        s1_count = [0] * 26
        window_count = [0] * 26
        
        # Count characters in s1
        for char in s1:
            s1_count[ord(char) - ord('a')] += 1
        
        window_size = len(s1)
        
        # Process first window
        for i in range(window_size):
            window_count[ord(s2[i]) - ord('a')] += 1
        
        if s1_count == window_count:
            return True
        
        # Slide the window
        for i in range(window_size, len(s2)):
            # Add new character
            window_count[ord(s2[i]) - ord('a')] += 1
            
            # Remove old character
            window_count[ord(s2[i - window_size]) - ord('a')] -= 1
            
            if s1_count == window_count:
                return True
        
        return False
    
    def checkInclusionOptimized(self, s1: str, s2: str) -> bool:
        """
        Optimized version tracking number of matches instead of comparing arrays.
        
        Time Complexity: O(n + m)
        Space Complexity: O(1)
        """
        if len(s1) > len(s2):
            return False
        
        s1_count = [0] * 26
        window_count = [0] * 26
        
        # Count characters in s1
        for char in s1:
            s1_count[ord(char) - ord('a')] += 1
        
        window_size = len(s1)
        matches = 0
        
        # Process first window and count initial matches
        for i in range(window_size):
            index = ord(s2[i]) - ord('a')
            window_count[index] += 1
            if window_count[index] == s1_count[index]:
                matches += 1
            elif window_count[index] == s1_count[index] + 1:
                matches -= 1
        
        if matches == 26:
            return True
        
        # Slide the window
        for i in range(window_size, len(s2)):
            # Add new character
            new_index = ord(s2[i]) - ord('a')
            window_count[new_index] += 1
            if window_count[new_index] == s1_count[new_index]:
                matches += 1
            elif window_count[new_index] == s1_count[new_index] + 1:
                matches -= 1
            
            # Remove old character
            old_index = ord(s2[i - window_size]) - ord('a')
            window_count[old_index] -= 1
            if window_count[old_index] == s1_count[old_index]:
                matches += 1
            elif window_count[old_index] == s1_count[old_index] - 1:
                matches -= 1
            
            if matches == 26:
                return True
        
        return False


def demo():
    """Demonstrate Permutation in String solution with test cases."""
    solution = Solution()
    
    test_cases = [
        TestCase(
            input_args=("ab", "eidbaooo"), 
            expected=True,
            description="'ba' is permutation of 'ab'"
        ),
        TestCase(
            input_args=("ab", "eidboaoo"), 
            expected=False,
            description="No permutation of 'ab' exists"
        ),
        TestCase(
            input_args=("a", "ab"), 
            expected=True,
            description="Single character match"
        ),
        TestCase(
            input_args=("ab", "a"), 
            expected=False,
            description="s1 longer than s2"
        ),
        TestCase(
            input_args=("abc", "baxyzabc"), 
            expected=True,
            description="Exact match at end"
        ),
        TestCase(
            input_args=("abc", "bca"), 
            expected=True,
            description="Entire s2 is permutation"
        ),
        TestCase(
            input_args=("aaa", "aaaa"), 
            expected=True,
            description="Repeated characters"
        ),
        TestCase(
            input_args=("abc", "def"), 
            expected=False,
            description="Completely different characters"
        ),
        TestCase(
            input_args=("abcdxabcde", "abcdeabcdx"), 
            expected=True,
            description="Long strings with permutation"
        ),
        TestCase(
            input_args=("hello", "ooolleoooleh"), 
            expected=False,
            description="All characters present but no valid permutation"
        ),
    ]
    
    results = run_test_cases(solution.checkInclusion, test_cases)
    
    return create_demo_output(
        title="Permutation in String",
        description="Check if s2 contains a permutation of s1 using sliding window",
        results=results,
        complexity_analysis={
            "time": "O(n + m) - where n is len(s1), m is len(s2)",
            "space": "O(1) - at most 26 characters in frequency maps"
        },
        key_insights=[
            "Fixed-size sliding window of length len(s1)",
            "Compare character frequencies instead of generating permutations",
            "Counter comparison or array comparison for frequency matching",
            "Optimization: track number of matching frequency counts"
        ],
        common_pitfalls=[
            "Handle case where s1 is longer than s2",
            "Remember to remove character leaving window",
            "Frequency comparison is key - not character order",
            "Be careful with Counter deletion when count reaches 0"
        ],
        follow_up_questions=[
            "How would you find all starting indices of permutations?",
            "What if we needed case-insensitive matching?",
            "Can you optimize further using rolling hash?",
            "How would you handle Unicode characters?"
        ]
    )


# Register this problem
register_problem(
    id=567,
    slug="permutation-in-string",
    title="Permutation in String",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags={"hash-table", "two-pointers", "string", "sliding-window"},
    module="src.interview_workbook.leetcode.sliding_window.permutation_in_string",
    url="https://leetcode.com/problems/permutation-in-string/",
    notes="Fixed-size sliding window with character frequency comparison"
)
