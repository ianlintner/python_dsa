

def edit_distance(word1: str, word2: str) -> int:
    """
    Edit Distance (Levenshtein Distance) - minimum operations to transform word1 to word2.

    Time: O(m * n) where m = len(word1), n = len(word2)
    Space: O(m * n)

    LeetCode 72: Edit Distance

    Operations allowed: insert, delete, replace
    DP recurrence:
    - If chars match: dp[i][j] = dp[i-1][j-1]
    - Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
      - dp[i-1][j] + 1: delete from word1
      - dp[i][j-1] + 1: insert into word1
      - dp[i-1][j-1] + 1: replace in word1

    Interview follow-ups:
    - How to optimize space? (Use 1D array)
    - How to reconstruct operations? (Track parent pointers)
    - What if operations have different costs? (Weighted edit distance)
    - Applications? (DNA sequencing, spell checkers, diff tools)
    """
    m, n = len(word1), len(word2)

    # dp[i][j] = min operations to transform word1[0:i] to word2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to get word2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # Delete
                    dp[i][j - 1],  # Insert
                    dp[i - 1][j - 1],  # Replace
                )

    return dp[m][n]


def edit_distance_optimized(word1: str, word2: str) -> int:
    """
    Space-optimized edit distance using 1D array.

    Time: O(m * n)
    Space: O(min(m, n))

    Only keep current and previous row since we only need them.
    """
    m, n = len(word1), len(word2)

    # Optimize by using shorter string for columns
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m

    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n

        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])

        prev = curr

    return prev[n]


def edit_distance_with_operations(word1: str, word2: str) -> tuple[int, list[str]]:
    """
    Edit distance with reconstruction of actual operations.

    Returns: (min_distance, list_of_operations)
    Operations format: "insert X", "delete X", "replace X with Y"
    """
    m, n = len(word1), len(word2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    # Reconstruct operations
    operations = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            # Characters match, no operation
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Replace
            operations.append(f"replace '{word1[i-1]}' with '{word2[j-1]}'")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Delete
            operations.append(f"delete '{word1[i-1]}'")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Insert
            operations.append(f"insert '{word2[j-1]}'")
            j -= 1

    operations.reverse()
    return dp[m][n], operations


def weighted_edit_distance(
    word1: str, word2: str, insert_cost: int = 1, delete_cost: int = 1, replace_cost: int = 1
) -> int:
    """
    Weighted edit distance with different costs for operations.

    Useful when operations have different real-world costs.
    """
    m, n = len(word1), len(word2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases with costs
    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + delete_cost,  # Delete
                    dp[i][j - 1] + insert_cost,  # Insert
                    dp[i - 1][j - 1] + replace_cost,  # Replace
                )

    return dp[m][n]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Longest Common Subsequence - related to edit distance.

    LeetCode 1143: Longest Common Subsequence

    Relationship: edit_distance = m + n - 2 * lcs (for insert/delete only)
    """
    m, n = len(text1), len(text2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def min_distance_delete_only(word1: str, word2: str) -> int:
    """
    Minimum distance using only delete operations.

    LeetCode 583: Delete Operation for Two Strings

    Strategy: Find LCS, then delete non-LCS characters from both strings.
    """
    lcs_length = longest_common_subsequence(word1, word2)
    return len(word1) + len(word2) - 2 * lcs_length


def one_edit_distance(s: str, t: str) -> bool:
    """
    Check if strings are exactly one edit distance apart.

    LeetCode 161: One Edit Distance

    More efficient than computing full edit distance.
    """
    m, n = len(s), len(t)

    if abs(m - n) > 1:
        return False

    if m > n:
        s, t = t, s
        m, n = n, m

    for i in range(m):
        if s[i] != t[i]:
            if m == n:
                # Replace case
                return s[i + 1 :] == t[i + 1 :]
            else:
                # Insert case
                return s[i:] == t[i + 1 :]

    # All characters match, check if exactly one insertion needed
    return n - m == 1


def edit_distance_k(word1: str, word2: str, k: int) -> bool:
    """
    Check if edit distance is at most k.

    More efficient than computing full distance when k is small.
    Uses diagonal optimization.
    """
    m, n = len(word1), len(word2)

    if abs(m - n) > k:
        return False

    # Only compute diagonal band of width 2k+1
    dp = {}
    dp[(0, 0)] = 0

    for i in range(m + 1):
        for j in range(max(0, i - k), min(n + 1, i + k + 1)):
            if i == 0 and j == 0:
                continue

            cost = float("inf")

            # Delete
            if i > 0 and (i - 1, j) in dp:
                cost = min(cost, dp[(i - 1, j)] + 1)

            # Insert
            if j > 0 and (i, j - 1) in dp:
                cost = min(cost, dp[(i, j - 1)] + 1)

            # Replace/Match
            if i > 0 and j > 0 and (i - 1, j - 1) in dp:
                if word1[i - 1] == word2[j - 1]:
                    cost = min(cost, dp[(i - 1, j - 1)])
                else:
                    cost = min(cost, dp[(i - 1, j - 1)] + 1)

            if cost <= k:
                dp[(i, j)] = cost

    return (m, n) in dp and dp[(m, n)] <= k


def demo():
    """Demo function for edit distance algorithms."""
    print("Edit Distance (Levenshtein Distance) Demo")
    print("=" * 50)

    # Basic edit distance examples
    test_cases = [
        ("horse", "ros"),
        ("intention", "execution"),
        ("", "abc"),
        ("abc", ""),
        ("same", "same"),
        ("kitten", "sitting"),
    ]

    print("Basic Edit Distance:")
    for word1, word2 in test_cases:
        distance = edit_distance(word1, word2)
        distance_opt = edit_distance_optimized(word1, word2)
        distance_ops, operations = edit_distance_with_operations(word1, word2)

        print(f"'{word1}' -> '{word2}':")
        print(f"  Distance: {distance} (optimized: {distance_opt})")
        print(f"  Operations: {operations}")
        print()

    # Weighted edit distance
    print("Weighted Edit Distance:")
    word1, word2 = "sunday", "saturday"
    normal_dist = edit_distance(word1, word2)
    weighted_dist = weighted_edit_distance(
        word1, word2, insert_cost=2, delete_cost=2, replace_cost=1
    )

    print(f"'{word1}' -> '{word2}':")
    print(f"Normal distance: {normal_dist}")
    print(f"Weighted distance (insert=2, delete=2, replace=1): {weighted_dist}")
    print()

    # LCS relationship
    print("Longest Common Subsequence:")
    lcs_len = longest_common_subsequence(word1, word2)
    delete_only_dist = min_distance_delete_only(word1, word2)

    print(f"LCS length: {lcs_len}")
    print(f"Delete-only distance: {delete_only_dist}")
    print(f"Relationship check: {len(word1)} + {len(word2)} - 2*{lcs_len} = {delete_only_dist}")
    print()

    # One edit distance
    print("One Edit Distance:")
    one_edit_cases = [("ab", "acb"), ("cab", "ad"), ("1203", "1213"), ("teacher", "treacher")]

    for s, t in one_edit_cases:
        is_one_edit = one_edit_distance(s, t)
        actual_dist = edit_distance(s, t)
        print(f"'{s}' and '{t}': one edit = {is_one_edit}, actual distance = {actual_dist}")
    print()

    # Edit distance within k
    print("Edit Distance within K:")
    k_cases = [("abcdef", "azced", 3), ("abcdef", "xyz", 2), ("hello", "hallo", 1)]

    for s, t, k in k_cases:
        within_k = edit_distance_k(s, t, k)
        actual_dist = edit_distance(s, t)
        print(f"'{s}' and '{t}' within {k} edits: {within_k}, actual: {actual_dist}")
    print()

    # Performance analysis
    print("Performance Analysis:")
    print("Standard DP:")
    print("  - Time: O(m * n), Space: O(m * n)")
    print("  - Can reconstruct operations")
    print("  - Most straightforward implementation")
    print()
    print("Space Optimized:")
    print("  - Time: O(m * n), Space: O(min(m, n))")
    print("  - Cannot reconstruct operations easily")
    print("  - Good for large strings when only distance needed")
    print()
    print("Diagonal Band (for small k):")
    print("  - Time: O(k * min(m, n)), Space: O(k²)")
    print("  - Efficient when expected distance is small")
    print("  - Early termination possible")
    print()
    print("Applications:")
    print("  - Spell checkers and autocorrect")
    print("  - DNA sequence alignment")
    print("  - Version control diff algorithms")
    print("  - Plagiarism detection")
    print("  - Machine translation evaluation")
    print("  - Fuzzy string matching")


if __name__ == "__main__":
    demo()
