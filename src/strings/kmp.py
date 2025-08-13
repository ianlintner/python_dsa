from typing import List


def build_lps_array(pattern: str) -> List[int]:
    """
    Build the Longest Proper Prefix which is also Suffix (LPS) array.

    Time: O(m) where m = len(pattern)
    Space: O(m)

    The LPS array is the key to KMP's efficiency.
    lps[i] = length of longest proper prefix of pattern[0..i] which is also suffix.

    Interview follow-ups:
    - Why is this O(m) and not O(m²)? (The while loop doesn't reset j to 0)
    - What's a "proper" prefix? (Prefix that's not the entire string)
    - How does this help in pattern matching? (Tells us how far to skip)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Don't increment i here, we need to check pattern[i] again
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt string matching algorithm.

    Time: O(n + m) where n = len(text), m = len(pattern)
    Space: O(m) for LPS array

    Returns: List of starting indices where pattern is found in text

    Key insight: When mismatch occurs, use LPS array to determine
    how many characters we can skip instead of starting over.

    Interview follow-ups:
    - Why is this better than naive? (No backtracking in text)
    - When would you use this vs other algorithms? (Long patterns, multiple searches)
    - What if pattern is longer than text? (Return empty list)
    """
    if not pattern or not text:
        return []

    n, m = len(text), len(pattern)
    if m > n:
        return []

    # Build LPS array
    lps = build_lps_array(pattern)

    matches = []
    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Found a match
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches


def kmp_search_first_occurrence(text: str, pattern: str) -> int:
    """
    Find first occurrence of pattern in text using KMP.

    Returns: Index of first match, or -1 if not found
    """
    matches = kmp_search(text, pattern)
    return matches[0] if matches else -1


def naive_string_search(text: str, pattern: str) -> List[int]:
    """
    Naive string matching for comparison.

    Time: O(n * m) worst case
    Space: O(1)

    This is what you'd naturally write, but it's inefficient for large inputs.
    """
    if not pattern or not text:
        return []

    n, m = len(text), len(pattern)
    matches = []

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1

        if j == m:
            matches.append(i)

    return matches


def kmp_count_occurrences(text: str, pattern: str) -> int:
    """Count total occurrences of pattern in text."""
    return len(kmp_search(text, pattern))


def kmp_search_case_insensitive(text: str, pattern: str) -> List[int]:
    """Case-insensitive KMP search."""
    return kmp_search(text.lower(), pattern.lower())


def find_period_of_string(s: str) -> int:
    """
    Find the shortest period of a string using KMP's LPS array.

    A string has period p if s[i] = s[i + p] for all valid i.

    Time: O(n)
    Space: O(n)

    Example: "abcabcabc" has period 3
    """
    n = len(s)
    lps = build_lps_array(s)

    # The period is n - lps[n-1]
    period = n - lps[n - 1]

    # Check if this is actually a period (string might not be periodic)
    if n % period == 0:
        return period
    else:
        return n  # String is not periodic, period is the entire length


def is_rotation(s1: str, s2: str) -> bool:
    """
    Check if s2 is a rotation of s1 using KMP.

    Key insight: s2 is a rotation of s1 iff s2 is a substring of s1 + s1

    Time: O(n)
    Space: O(n)

    Example: "waterbottle" is a rotation of "erbottlewat"
    """
    if len(s1) != len(s2):
        return False

    if len(s1) == 0:
        return True

    # Check if s2 is substring of s1 + s1
    doubled = s1 + s1
    return kmp_search_first_occurrence(doubled, s2) != -1


def longest_prefix_suffix(s: str) -> int:
    """
    Find length of longest proper prefix which is also suffix.

    This is just the last element of the LPS array.
    """
    if not s:
        return 0

    lps = build_lps_array(s)
    return lps[-1]


def kmp_multiple_patterns(text: str, patterns: List[str]) -> dict[str, List[int]]:
    """
    Search for multiple patterns in text using KMP.

    For many patterns, consider using Aho-Corasick algorithm instead.
    """
    results = {}
    for pattern in patterns:
        results[pattern] = kmp_search(text, pattern)
    return results


def demo():
    """Demo function for KMP algorithm."""
    print("KMP String Matching Demo")
    print("=" * 40)

    # Basic pattern matching
    text = "ABABDABACDABABCABCABCABCABC"
    pattern = "ABABCABCABCABC"

    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print()

    # Show LPS array construction
    lps = build_lps_array(pattern)
    print("LPS array construction:")
    print(f"Pattern: {pattern}")
    print(f"LPS:     {lps}")
    print()

    # Compare KMP vs naive
    kmp_matches = kmp_search(text, pattern)
    naive_matches = naive_string_search(text, pattern)

    print(f"KMP matches: {kmp_matches}")
    print(f"Naive matches: {naive_matches}")
    print(f"Match: {kmp_matches == naive_matches}")
    print()

    # Performance comparison for repeated pattern
    repeated_text = "AAAAAAAAAAAAAAAAAAAAAAAAB"
    repeated_pattern = "AAAAB"

    print(f"Repeated pattern example:")
    print(f"Text: {repeated_text}")
    print(f"Pattern: {repeated_pattern}")

    kmp_result = kmp_search(repeated_text, repeated_pattern)
    naive_result = naive_string_search(repeated_text, repeated_pattern)

    print(f"KMP result: {kmp_result}")
    print(f"Naive result: {naive_result}")
    print()

    # String period detection
    periodic_strings = ["abcabcabc", "aaaa", "abcdef", "abababab"]

    print("String period detection:")
    for s in periodic_strings:
        period = find_period_of_string(s)
        print(f"'{s}' has period {period}")
    print()

    # Rotation detection
    rotation_pairs = [
        ("waterbottle", "erbottlewat"),
        ("abcde", "cdeab"),
        ("abcde", "abced"),
        ("", ""),
    ]

    print("Rotation detection:")
    for s1, s2 in rotation_pairs:
        is_rot = is_rotation(s1, s2)
        print(f"'{s2}' is rotation of '{s1}': {is_rot}")
    print()

    # Multiple patterns
    multi_text = "she sells seashells by the seashore"
    multi_patterns = ["she", "sea", "shell", "shore"]

    multi_results = kmp_multiple_patterns(multi_text, multi_patterns)
    print(f"Multiple pattern search in: '{multi_text}'")
    for pattern, matches in multi_results.items():
        print(f"  '{pattern}': {matches}")
    print()

    # Edge cases
    print("Edge cases:")
    edge_cases = [("", "abc"), ("abc", ""), ("abc", "abcd"), ("same", "same")]

    for text, pattern in edge_cases:
        result = kmp_search(text, pattern)
        print(f"Text: '{text}', Pattern: '{pattern}' -> {result}")


if __name__ == "__main__":
    demo()
