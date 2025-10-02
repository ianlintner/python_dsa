def next_greater_elements(nums: list[int]) -> list[int]:
    """
    Next Greater Element for each element in array (to the right).

    Time: O(n)
    Space: O(n)

    Returns indices of next greater element; -1 if none.
    """
    n = len(nums)
    res = [-1] * n
    stack: list[int] = []  # store indices, values are increasing by index stack

    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            idx = stack.pop()
            res[idx] = i
        stack.append(i)
    return res


def next_greater_elements_values(nums: list[int]) -> list[int]:
    """
    Variant returning the values instead of indices. -1 if none.
    For each position i, returns nums[next_greater_index[i]] or -1 if not found.
    """
    idxs = next_greater_elements(nums)
    return [nums[j] if j != -1 else -1 for j in idxs]


def daily_temperatures(temps: list[int]) -> list[int]:
    """
    LeetCode 739: Daily Temperatures.
    For each day, how many days until a warmer temperature.

    Time: O(n)
    Space: O(n)
    """
    n = len(temps)
    ans = [0] * n
    stack: list[int] = []  # decreasing stack of indices by temperature
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


def largest_rectangle_area(heights: list[int]) -> int:
    """
    LeetCode 84: Largest Rectangle in Histogram.

    Monotonic increasing stack of indices (by height).

    Time: O(n)
    Space: O(n)
    """
    stack: list[int] = []  # indices of ascending heights
    max_area = 0
    # Append sentinel height 0 at the end to flush the stack
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            height = heights[top]
            # width extends to i; left boundary is stack[-1] after pop
            left = stack[-1] if stack else -1
            width = i - left - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area


def trap_rain_water(heights: list[int]) -> int:
    """
    LeetCode 42: Trapping Rain Water using monotonic stack.

    Time: O(n)
    Space: O(n)
    """
    stack: list[int] = []  # indices; heights at indices are non-decreasing
    water = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(heights[left], h) - heights[bottom]
            if bounded_height > 0:
                water += bounded_height * width
        stack.append(i)
    return water


def demo():
    print("Monotonic Stack/Queue Patterns Demo")
    print("=" * 45)

    nums = [2, 1, 2, 4, 3]
    print(f"Array: {nums}")
    nge_idx = next_greater_elements(nums)
    nge_vals = next_greater_elements_values(nums)
    print(f"Next greater indices: {nge_idx}")
    print(f"Next greater values:  {nge_vals}")
    print()

    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"Daily temperatures: {temps}")
    print(f"Days to warmer:     {daily_temperatures(temps)}")
    print()

    hist = [2, 1, 5, 6, 2, 3]
    print(f"Histogram: {hist}")
    print(f"Largest rectangle area: {largest_rectangle_area(hist)}")
    print()

    elevation = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Elevation map: {elevation}")
    print(f"Trapped rain water: {trap_rain_water(elevation)}")
    print()

    print("Notes & Interview Tips:")
    print("  - Monotonic stack is used for next greater/smaller element patterns.")
    print("  - For 'spans' and 'wait until greater', store indices and compute distances.")
    print("  - For histogram area, flush with sentinel 0 to process all bars.")
    print("  - For water trapping, compute bounded areas between taller bars.")


if __name__ == "__main__":
    demo()
