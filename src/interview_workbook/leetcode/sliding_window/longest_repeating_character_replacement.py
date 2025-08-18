"""
Longest Repeating Character Replacement - LeetCode Problem

You are given a string s and an integer k. You can choose any character of the string and change it 
to any other uppercase English letter. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing 
the above operations.
"""

from collections import defaultdict
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """
        Find longest repeating character replacement using sliding window.
        
        Time Complexity: O(n) - single pass through string
        Space Complexity: O(1) - at most 26 characters in frequency map
        
        Args:
            s: Input string of uppercase English letters
            k: Maximum number of character replacements allowed
            
        Returns:
            int: Length of longest substring with same character after replacements
        """
        char_count = defaultdict(int)
        left = 0
        max_length = 0
        max_char_count = 0
        
        for right in range(len(s)):
            # Add current character to frequency map
            char_count[s[right]] += 1
            max_char_count = max(max_char_count, char_count[s[right]])
            
            # Current window size
            window_size = right - left + 1
            
            # If we need more than k replacements, shrink window
            if window_size - max_char_count > k:
                char_count[s[left]] -= 1
                left += 1
            
            # Update maximum length
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def characterReplacementOptimized(self, s: str, k: int) -> int:
        """
        Optimized version that doesn't update max_char_count when shrinking.
        
        Time Complexity: O(n) - single pass
        Space Complexity: O(1) - at most 26 characters
        """
        char_count = defaultdict(int)
        left = 0
        max_char_count = 0
        
        for right in range(len(s)):
            char_count[s[right]] += 1
            max_char_count = max(max_char_count, char_count[s[right]])
            
            # If current window is invalid, slide the window
            if right - left + 1 - max_char_count > k:
                char_count[s[left]] -= 1
                left += 1
        
        # The final window size is the answer
        return len(s) - left
    
    def characterReplacementBruteForce(self, s: str, k: int) -> int:
        """
        Brute force approach checking all possible substrings (not optimal).
        
        Time Complexity: O(n²) - nested loops with character counting
        Space Complexity: O(1) - frequency array
        """
        max_length = 0
        n = len(s)
        
        for i in range(n):
            char_count = defaultdict(int)
            max_char_freq = 0
            
            for j in range(i, n):
                char_count[s[j]] += 1
                max_char_freq = max(max_char_freq, char_count[s[j]])
                
                window_size = j - i + 1
                replacements_needed = window_size - max_char_freq
                
                if replacements_needed <= k:
                    max_length = max(max_length, window_size)
                else:
                    break  # No point checking longer substrings from this start
        
        return max_length


def demo():
    """Demonstrate Longest Repeating Character Replacement solution with test cases."""
    solution = Solution()
    
    test_cases = [
        TestCase(
            input_args=("ABAB", 2), 
            expected=4,
            description="Replace B's to get 'AAAA'"
        ),
        TestCase(
            input_args=("AABABBA", 1), 
            expected=4,
            description="Replace one character to get 'AAAA' or 'BBBB'"
        ),
        TestCase(
            input_args=("AAAA", 2), 
            expected=4,
            description="Already all same characters"
        ),
        TestCase(
            input_args=("ABCDEF", 1), 
            expected=2,
            description="All different characters - can get length 2"
        ),
        TestCase(
            input_args=("A", 1), 
            expected=1,
            description="Single character"
        ),
        TestCase(
            input_args=("AABCABCBB", 2), 
            expected=5,
            description="Complex case with multiple options"
        ),
        TestCase(
            input_args=("ABABACB", 3), 
            expected=7,
            description="Can replace entire string"
        ),
        TestCase(
            input_args=("AAABBBCCC", 2), 
            expected=5,
            description="Groups of same characters"
        ),
        TestCase(
            input_args=("ABCABC", 2), 
            expected=4,
            description="Repeating pattern"
        ),
    ]
    
    results = run_test_cases(solution.characterReplacement, test_cases)
    
    return create_demo_output(
        title="Longest Repeating Character Replacement",
        description="Find longest repeating character substring with at most k replacements",
        results=results,
        complexity_analysis={
            "time": "O(n) - single pass through string with sliding window",
            "space": "O(1) - at most 26 characters in frequency map"
        },
        key_insights=[
            "Sliding window with character frequency tracking",
            "Key insight: window_size - max_char_count = replacements needed",
            "Shrink window when replacements exceed k",
            "max_char_count tracks most frequent character in current window"
        ],
        common_pitfalls=[
            "Remember to update max_char_count when adding characters",
            "Window becomes invalid when replacements needed > k",
            "Consider that we want the longest valid window",
            "Optimization: don't need to recalculate max_char_count when shrinking"
        ],
        follow_up_questions=[
            "What if we could replace with any character, not just uppercase letters?",
            "How would you modify to find the actual substring, not just length?",
            "What if k could be negative or zero?",
            "Can you solve for lowercase letters or mixed case?"
        ]
    )


# Register this problem
register_problem(
    id=424,
    slug="longest-repeating-character-replacement",
    title="Longest Repeating Character Replacement",
    category=Category.SLIDING_WINDOW,
    difficulty=Difficulty.MEDIUM,
    tags={"hash-table", "string", "sliding-window"},
    module="src.interview_workbook.leetcode.sliding_window.longest_repeating_character_replacement",
    url="https://leetcode.com/problems/longest-repeating-character-replacement/",
    notes="Sliding window with character frequency and replacement counting"
)
