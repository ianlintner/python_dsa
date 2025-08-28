"""
LeetCode 763: Partition Labels

You are given a string s. We want to partition the string into as many parts as possible
so that each letter appears in at most one part.

Note that the partition is done so that after concatenating all the parts in order,
the resultant string should be the original string.

Return a list of integers representing the size of these parts.

Time Complexity: O(n)
Space Complexity: O(1) - at most 26 characters
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, run_test_cases
from .._types import Category, Difficulty


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        """
        Greedy approach: Find the rightmost occurrence of each character,
        then use two pointers to determine partition boundaries.

        Strategy:
        1. Record the last occurrence index of each character
        2. Use two pointers to track current partition range
        3. Extend partition end to include all occurrences of characters in current partition
        4. When we reach the end of current partition, record its size and start new partition

        Key insight: A partition is complete when we've seen all occurrences
        of every character that appears in the partition.

        Time: O(n) - Two passes through the string
        Space: O(1) - Dictionary with at most 26 entries for lowercase letters
        """
        # Record the last occurrence of each character
        last_occurrence = {char: i for i, char in enumerate(s)}

        partitions = []
        partition_start = 0
        partition_end = 0

        for i, char in enumerate(s):
            # Extend current partition to include all occurrences of current character
            partition_end = max(partition_end, last_occurrence[char])

            # If we've reached the end of current partition
            if i == partition_end:
                partitions.append(partition_end - partition_start + 1)
                partition_start = i + 1

        return partitions

    def partitionLabelsBruteForce(self, s: str) -> List[int]:
        """
        Brute force approach: For each possible starting position, find the minimum
        partition that contains all occurrences of characters in that range.

        This is less efficient but demonstrates the problem-solving process.

        Time: O(n²) - For each position, potentially scan to end of string
        Space: O(n) - Store character sets for each partition
        """
        partitions = []
        i = 0

        while i < len(s):
            chars_in_partition = set()
            j = i

            # Keep expanding partition until all characters are contained
            while j < len(s):
                chars_in_partition.add(s[j])

                # Check if all occurrences of characters in partition are included
                can_end_here = True
                for char in chars_in_partition:
                    # Find if this character appears after current position
                    if s.rfind(char) > j:
                        can_end_here = False
                        break

                if can_end_here:
                    break
                j += 1

            partitions.append(j - i + 1)
            i = j + 1

        return partitions

    def partitionLabelsOptimized(self, s: str) -> List[int]:
        """
        Alternative implementation with cleaner logic and early termination opportunities.

        Uses the same greedy strategy but with more explicit boundary tracking.

        Time: O(n) - Two passes through the string
        Space: O(1) - Dictionary with at most 26 entries
        """
        # Build last occurrence map
        last_index = {}
        for i, char in enumerate(s):
            last_index[char] = i

        result = []
        start = 0
        end = 0

        for i in range(len(s)):
            # Update the end boundary to include all occurrences of current character
            end = max(end, last_index[s[i]])

            # If current index reaches the end boundary, we can close this partition
            if i == end:
                result.append(end - start + 1)
                start = end + 1

        return result


def create_demo_output() -> str:
    """
    Create comprehensive demo output showing different partition scenarios.
    """
    solution = Solution()

    demos = []

    # Test case 1: Standard case with multiple partitions
    s1 = "ababcbacadefegdehijhklij"
    result1 = solution.partitionLabels(s1)
    demos.append(f"Input: '{s1}'")
    demos.append(f"Partitions: {result1}")
    demos.append("Analysis: 'ababcbaca' + 'defegde' + 'hijhklij'")
    demos.append("- First partition contains all 'a', 'b', 'c'")
    demos.append("- Second partition contains all 'd', 'e', 'f', 'g'")
    demos.append("- Third partition contains all remaining characters")
    demos.append("")

    # Test case 2: Single character repeated
    s2 = "aaaa"
    result2 = solution.partitionLabels(s2)
    demos.append(f"Input: '{s2}'")
    demos.append(f"Partitions: {result2}")
    demos.append("Analysis: All same character → single partition")
    demos.append("")

    # Test case 3: All unique characters
    s3 = "abcdef"
    result3 = solution.partitionLabels(s3)
    demos.append(f"Input: '{s3}'")
    demos.append(f"Partitions: {result3}")
    demos.append("Analysis: All unique → each character is its own partition")
    demos.append("")

    # Test case 4: Overlapping character ranges
    s4 = "abccba"
    result4 = solution.partitionLabels(s4)
    demos.append(f"Input: '{s4}'")
    demos.append(f"Partitions: {result4}")
    demos.append("Analysis: Characters 'a', 'b', 'c' all overlap → single partition")
    demos.append("")

    # Test case 5: Sequential non-overlapping groups
    s5 = "aabbcc"
    result5 = solution.partitionLabels(s5)
    demos.append(f"Input: '{s5}'")
    demos.append(f"Partitions: {result5}")
    demos.append("Analysis: Each character pair forms independent partition")
    demos.append("")

    # Algorithm analysis
    demos.append("=== Algorithm Analysis ===")
    demos.append("Greedy Strategy:")
    demos.append("1. Pre-compute last occurrence of each character")
    demos.append("2. Traverse string while tracking current partition boundary")
    demos.append("3. Extend boundary to include all occurrences of seen characters")
    demos.append("4. Close partition when we reach its boundary")
    demos.append("5. This is optimal because:")
    demos.append("   - Any earlier split would break character containment")
    demos.append("   - Any later split would create unnecessarily large partitions")
    demos.append("")

    demos.append("Key Insights:")
    demos.append("- A partition is 'complete' when we've processed all occurrences")
    demos.append("  of every character that appears in it")
    demos.append("- The rightmost occurrence determines the minimum partition size")
    demos.append("- Greedy choice: close partition as soon as possible")
    demos.append("- This maximizes the number of partitions (problem requirement)")
    demos.append("")

    # Visual example with indices
    demos.append("=== Visual Example ===")
    example_str = "ababcbacadefegdehijhklij"
    last_occurrence = {char: i for i, char in enumerate(example_str)}

    demos.append(f"String: {example_str}")
    demos.append(f"Indices: {''.join(str(i % 10) for i in range(len(example_str)))}")
    demos.append("")
    demos.append("Last occurrences:")
    for char in sorted(set(example_str)):
        demos.append(f"  '{char}': index {last_occurrence[char]}")
    demos.append("")

    # Show partition building process
    demos.append("Partition building process:")
    partition_end = 0
    partition_start = 0
    for i, char in enumerate(example_str):
        old_end = partition_end
        partition_end = max(partition_end, last_occurrence[char])
        if partition_end != old_end:
            demos.append(f"  i={i}, char='{char}' → extend partition end to {partition_end}")

        if i == partition_end:
            demos.append(
                f"  i={i}: partition complete [{partition_start}:{i}] = '{example_str[partition_start : i + 1]}'"
            )
            partition_start = i + 1

    # Performance comparison
    import time

    large_string = "".join(chr(ord("a") + (i % 26)) for i in range(10000))

    # Time optimized approach
    start_time = time.time()
    for _ in range(1000):
        solution.partitionLabels(large_string)
    optimized_time = time.time() - start_time

    # Time brute force approach (smaller string for reasonable runtime)
    small_string = "".join(chr(ord("a") + (i % 26)) for i in range(100))
    start_time = time.time()
    for _ in range(100):
        solution.partitionLabelsBruteForce(small_string)
    brute_time = time.time() - start_time

    demos.append("")
    demos.append("=== Performance Comparison ===")
    demos.append(f"Optimized approach (1000 runs, 10000 chars): {optimized_time:.6f}s")
    demos.append(f"Brute force (100 runs, 100 chars): {brute_time:.6f}s")
    demos.append("Optimized: O(n) time, O(1) space")
    demos.append("Brute force: O(n²) time, O(n) space")
    demos.append("")

    # Real-world applications
    demos.append("=== Applications ===")
    demos.append("- Data processing: partition logs by unique identifiers")
    demos.append("- Database sharding: group records to minimize cross-shard queries")
    demos.append("- Text processing: segment documents by topic/theme boundaries")
    demos.append("- Memory management: partition memory regions by access patterns")
    demos.append("- Network routing: segment traffic flows by destination groups")
    demos.append("- Compiler design: partition symbol scopes for optimization")

    return "\n".join(demos)


# Test cases
TEST_CASES = [
    TestCase(
        input=["ababcbacadefegdehijhklij"],
        expected=[9, 7, 8],
        description="Standard case with three partitions",
    ),
    TestCase(
        input=["eccbbbbdec"], expected=[10], description="All characters overlap - single partition"
    ),
    TestCase(
        input=["abcdef"],
        expected=[1, 1, 1, 1, 1, 1],
        description="All unique characters - each is own partition",
    ),
    TestCase(input=["a"], expected=[1], description="Single character"),
    TestCase(input=["aa"], expected=[2], description="Repeated single character"),
    TestCase(input=["aabbcc"], expected=[2, 2, 2], description="Sequential character pairs"),
    TestCase(
        input=["abccba"], expected=[6], description="Interleaved characters - single partition"
    ),
    TestCase(
        input=["eaaaabaaec"],
        expected=[9, 1],
        description="Overlapping with isolated character at end",
    ),
]


def test_solution():
    """Test the partition labels solution with comprehensive test cases."""
    solution = Solution()
    run_test_cases(solution.partitionLabels, TEST_CASES)


# Register the problem
register_problem(
    slug="partition_labels",
    leetcode_num=763,
    title="Partition Labels",
    difficulty=Difficulty.MEDIUM,
    category=Category.GREEDY,
    solution_func=Solution().partitionLabels,
    test_func=test_solution,
    demo_func=create_demo_output,
)
