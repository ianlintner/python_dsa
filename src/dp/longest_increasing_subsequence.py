from typing import List
import bisect


def lis_dp_n2(nums: List[int]) -> int:
    """
    Longest Increasing Subsequence using O(n²) DP.

    Time: O(n²)
    Space: O(n)

    LeetCode 300: Longest Increasing Subsequence

    DP recurrence: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

    This is the more intuitive approach but not optimal for large inputs.
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # dp[i] = length of LIS ending at index i

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_binary_search(nums: List[int]) -> int:
    """
    Longest Increasing Subsequence using binary search optimization.

    Time: O(n log n)
    Space: O(n)

    Key insight: Maintain array where tails[i] = smallest ending element
    of all increasing subsequences of length i+1.

    This is the optimal solution and what interviewers expect at senior level.
    """
    if not nums:
        return 0

    # tails[i] = smallest tail element of all increasing subsequences of length i+1
    tails = []

    for num in nums:
        # Binary search for the position to insert/replace
        pos = bisect.bisect_left(tails, num)

        if pos == len(tails):
            # num is larger than all elements in tails, extend the sequence
            tails.append(num)
        else:
            # Replace the element at pos with num (smaller tail for same length)
            tails[pos] = num

    return len(tails)


def lis_with_reconstruction(nums: List[int]) -> tuple[int, List[int]]:
    """
    Find LIS length and reconstruct the actual subsequence.

    Returns: (length, actual_subsequence)

    This is a common follow-up question in interviews.
    """
    if not nums:
        return 0, []

    n = len(nums)
    dp = [1] * n
    parent = [-1] * n  # Track previous element in LIS

    max_length = 1
    max_index = 0

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

        if dp[i] > max_length:
            max_length = dp[i]
            max_index = i

    # Reconstruct the subsequence
    lis = []
    current = max_index
    while current != -1:
        lis.append(nums[current])
        current = parent[current]

    lis.reverse()
    return max_length, lis


def lis_binary_search_with_reconstruction(nums: List[int]) -> tuple[int, List[int]]:
    """
    O(n log n) LIS with subsequence reconstruction.

    More complex but optimal time complexity.
    """
    if not nums:
        return 0, []

    n = len(nums)
    # tails[i] = (value, original_index) of smallest tail for length i+1
    tails = []
    # dp[i] = length of LIS ending at index i
    dp = [0] * n
    # parent[i] = previous index in LIS ending at i
    parent = [-1] * n

    for i, num in enumerate(nums):
        # Binary search for position
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid][0] < num:
                left = mid + 1
            else:
                right = mid

        pos = left
        dp[i] = pos + 1

        # Set parent pointer
        if pos > 0:
            parent[i] = tails[pos - 1][1]

        # Update or append to tails
        if pos == len(tails):
            tails.append((num, i))
        else:
            tails[pos] = (num, i)

    # Find the ending index of LIS
    max_length = max(dp)
    end_index = dp.index(max_length)

    # Reconstruct
    lis = []
    current = end_index
    while current != -1:
        lis.append(nums[current])
        current = parent[current]

    lis.reverse()
    return max_length, lis


def longest_decreasing_subsequence(nums: List[int]) -> int:
    """
    Longest Decreasing Subsequence - variation of LIS.

    Just reverse the comparison in binary search.
    """
    if not nums:
        return 0

    tails = []

    for num in nums:
        # For decreasing, we want to find rightmost position where tails[i] > num
        pos = bisect.bisect_left(tails, num, key=lambda x: -x)

        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)


def lis_count(nums: List[int]) -> int:
    """
    Count the number of different LIS.

    LeetCode 673: Number of Longest Increasing Subsequence

    More complex DP problem - track both length and count.
    """
    if not nums:
        return 0

    n = len(nums)
    lengths = [1] * n  # Length of LIS ending at i
    counts = [1] * n  # Number of LIS ending at i

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    # Found longer subsequence
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    # Found another subsequence of same length
                    counts[i] += counts[j]

    max_length = max(lengths)
    return sum(counts[i] for i in range(n) if lengths[i] == max_length)


def russian_doll_envelopes(envelopes: List[List[int]]) -> int:
    """
    Russian Doll Envelopes - 2D LIS problem.

    LeetCode 354: Russian Doll Envelopes

    Key insight: Sort by width ascending, height descending.
    Then find LIS on heights.
    """
    if not envelopes:
        return 0

    # Sort by width ascending, height descending
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # Extract heights and find LIS
    heights = [env[1] for env in envelopes]
    return lis_binary_search(heights)


def box_stacking(boxes: List[List[int]]) -> int:
    """
    Box Stacking problem - 3D variation.

    Each box can be rotated, so generate all rotations.
    Then sort by base area and find LIS on heights.
    """
    if not boxes:
        return 0

    # Generate all rotations for each box
    rotations = []
    for length, width, height in boxes:
        # All possible rotations (length, width, height)
        rotations.extend(
            [
                (length, width, height),
                (width, length, height),
                (length, height, width),
                (height, length, width),
                (width, height, length),
                (height, width, length),
            ]
        )

    # Sort by base area (length * width) in descending order
    rotations.sort(key=lambda x: x[0] * x[1], reverse=True)

    n = len(rotations)
    dp = [rot[2] for rot in rotations]  # Initialize with heights

    for i in range(1, n):
        for j in range(i):
            # Can stack if base dimensions are strictly smaller
            if rotations[j][0] > rotations[i][0] and rotations[j][1] > rotations[i][1]:
                dp[i] = max(dp[i], dp[j] + rotations[i][2])

    return max(dp)


def demo():
    """Demo function for LIS algorithms."""
    print("Longest Increasing Subsequence Demo")
    print("=" * 50)

    # Basic LIS examples
    test_arrays = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7, 7, 7, 7],
        [1, 3, 6, 7, 9, 4, 10, 5, 6],
        [],
    ]

    print("Basic LIS Examples:")
    for i, nums in enumerate(test_arrays):
        if not nums:
            print(f"Array {i+1}: [] -> LIS length: 0")
            continue

        length_n2 = lis_dp_n2(nums)
        length_nlogn = lis_binary_search(nums)
        length_recon, subsequence = lis_with_reconstruction(nums)

        print(f"Array {i+1}: {nums}")
        print(f"  O(n²) DP: {length_n2}")
        print(f"  O(n log n): {length_nlogn}")
        print(f"  With reconstruction: {length_recon}, subsequence: {subsequence}")
        print()

    # LIS count example
    print("Number of LIS:")
    count_example = [1, 3, 5, 4, 7]
    lis_len = lis_binary_search(count_example)
    lis_cnt = lis_count(count_example)
    print(f"Array: {count_example}")
    print(f"LIS length: {lis_len}, Count: {lis_cnt}")
    print()

    # Russian Doll Envelopes
    print("Russian Doll Envelopes:")
    envelopes = [[5, 4], [6, 4], [6, 7], [2, 3]]
    max_envelopes = russian_doll_envelopes(envelopes)
    print(f"Envelopes: {envelopes}")
    print(f"Maximum nested envelopes: {max_envelopes}")
    print()

    # Box Stacking
    print("Box Stacking:")
    boxes = [[4, 6, 7], [1, 2, 3], [4, 5, 6], [10, 12, 32]]
    max_height = box_stacking(boxes)
    print(f"Boxes (length, width, height): {boxes}")
    print(f"Maximum stack height: {max_height}")
    print()

    # Performance comparison
    print("Performance Analysis:")
    print("O(n²) DP Approach:")
    print("  - Time: O(n²), Space: O(n)")
    print("  - Easy to understand and implement")
    print("  - Good for small inputs or when you need to reconstruct")
    print()
    print("O(n log n) Binary Search Approach:")
    print("  - Time: O(n log n), Space: O(n)")
    print("  - Optimal for large inputs")
    print("  - Harder to reconstruct subsequence")
    print("  - Uses patience sorting concept")
    print()
    print("Applications:")
    print("  - Stock price analysis (longest increasing trend)")
    print("  - Scheduling problems")
    print("  - Box stacking and similar 3D problems")
    print("  - Bioinformatics (DNA sequence analysis)")
    print("  - Network routing optimization")


if __name__ == "__main__":
    demo()
