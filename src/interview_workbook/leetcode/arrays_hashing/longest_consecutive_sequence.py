"""
LeetCode 128. Longest Consecutive Sequence
Category: Arrays & Hashing
"""

import random


def longest_consecutive(nums: list[int]) -> int:
    """
    Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
    Must run in O(n).
    """
    num_set = set(nums)
    longest = 0

    for num in num_set:
        if num - 1 not in num_set:  # start of a sequence
            length = 1
            while num + length in num_set:
                length += 1
            longest = max(longest, length)

    return longest


def demo() -> str:
    """Deterministic demo run."""
    random.seed(0)  # Ensure determinism
    sample = [100, 4, 200, 1, 3, 2]
    result = longest_consecutive(sample)
    print(f"Input: {sample}, Longest consecutive sequence length: {result}")
    return f"Longest consecutive sequence length of {sample} is {result}"
