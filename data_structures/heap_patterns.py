import heapq
from collections import Counter
from typing import Iterable, Iterator, List, Optional, Tuple

def k_largest(nums: List[int], k: int) -> List[int]:
    """
    Return k largest elements using a min-heap of size k.
    Time: O(n log k), Space: O(k)
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums, reverse=True)
    heap = nums[:k]
    heapq.heapify(heap)  # min-heap
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Return k most frequent elements.
    Strategy: frequency map + min-heap of size k on (freq, num).
    Time: O(n log k), Space: O(n)
    """
    if k <= 0:
        return []
    freq = Counter(nums)
    heap: List[Tuple[int, int]] = []
    for num, f in freq.items():
        if len(heap) < k:
            heapq.heappush(heap, (f, num))
        else:
            if f > heap[0][0]:
                heapq.heapreplace(heap, (f, num))
    # Return numbers sorted by frequency desc
    heap.sort(reverse=True)
    return [num for _, num in heap]

def merge_k_sorted(arrs: List[List[int]]) -> List[int]:
    """
    Merge k sorted lists into one sorted list.
    Time: O(N log k), N = total elements. Space: O(k)
    """
    res: List[int] = []
    heap: List[Tuple[int, int, int]] = []  # (value, list_index, element_index)
    for i, arr in enumerate(arrs):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    while heap:
        val, i, j = heapq.heappop(heap)
        res.append(val)
        nj = j + 1
        if nj < len(arrs[i]):
            heapq.heappush(heap, (arrs[i][nj], i, nj))
    return res

class MedianMaintenance:
    """
    Maintain median of a stream using two heaps:
      - max-heap for lower half (store negatives to simulate max-heap)
      - min-heap for upper half
    Supports O(log n) insert and O(1) median query.
    """
    def __init__(self):
        self.low: List[int] = []   # max-heap (store -x)
        self.high: List[int] = []  # min-heap

    def add(self, x: int) -> None:
        if not self.low or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
        else:
            heapq.heappush(self.high, x)
        # Rebalance so that |len(low) - len(high)| <= 1
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        elif len(self.high) > len(self.low) + 1:
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        if not self.low and not self.high:
            raise ValueError("No elements")
        if len(self.low) == len(self.high):
            return (-self.low[0] + self.high[0]) / 2.0
        return float(-self.low[0]) if len(self.low) > len(self.high) else float(self.high[0])

def demo():
    print("Heap / Priority Queue Patterns Demo")
    print("=" * 40)

    nums = [5, 1, 9, 3, 7, 8, 2, 6, 4]
    print(f"Array: {nums}")
    print(f"k_largest k=3 -> {k_largest(nums, 3)}")
    print()

    nums2 = [1,1,1,2,2,3,3,3,3,4,5,5,5]
    print(f"Array for top_k_frequent: {nums2}")
    print(f"top_k_frequent k=2 -> {top_k_frequent(nums2, 2)}")
    print()

    arrs = [[1,4,7], [2,5,8], [3,6,9,10]]
    print(f"merge_k_sorted({arrs}) -> {merge_k_sorted(arrs)}")
    print()

    print("Median maintenance:")
    mm = MedianMaintenance()
    stream = [5, 15, 1, 3]
    for x in stream:
        mm.add(x)
        print(f"  add({x}) -> median {mm.median()}")
    print()

    print("Notes & Interview Tips:")
    print("  - For k largest/smallest, keep a bounded heap of size k.")
    print("  - For top-k frequent, heap on frequency; Counter + heapq.nlargest is another option.")
    print("  - Merge k sorted lists with a heap of next candidates for O(N log k).")
    print("  - Median maintenance uses two heaps; keep sizes within 1 of each other.")

if __name__ == "__main__":
    demo()
