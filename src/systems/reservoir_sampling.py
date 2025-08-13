import random
from typing import Iterable, Iterator, List, Optional, Tuple

def reservoir_sample_one(stream: Iterable[int], seed: Optional[int] = None) -> Optional[int]:
    """
    Reservoir sampling for k=1 (Algorithm R).
    Each element in the stream has equal probability 1/n to be selected.
    
    Time: O(n), Space: O(1)
    """
    if seed is not None:
        random.seed(seed)
    sample = None
    for i, x in enumerate(stream, start=1):
        # Replace current sample with probability 1/i
        if random.randrange(i) == 0:
            sample = x
    return sample

def reservoir_sample_k(stream: Iterable[int], k: int, seed: Optional[int] = None) -> List[int]:
    """
    Reservoir sampling for arbitrary k (Algorithm R generalized).
    Returns a list of k sampled items with equal probability among all n choose k subsets.
    
    Time: O(n), Space: O(k)
    """
    if k <= 0:
        return []
    if seed is not None:
        random.seed(seed)
    it = iter(stream)
    reservoir: List[int] = []
    # Fill initial reservoir
    try:
        for _ in range(k):
            reservoir.append(next(it))
    except StopIteration:
        return reservoir  # stream had < k elements
    # Process remaining items
    idx = k
    for x in it:
        idx += 1
        j = random.randrange(idx)  # 0..idx-1
        if j < k:
            reservoir[j] = x
    return reservoir

def reservoir_sample_k_weighted(stream: Iterable[Tuple[int, float]], k: int, seed: Optional[int] = None) -> List[int]:
    """
    Weighted reservoir sampling (Efraimidis-Spirakis algorithm):
    Input: stream of (item, weight>0). Each item has selection probability proportional to weight.
    Returns k sampled items without replacement.
    
    Idea: Assign key = U^(1/weight) where U~Uniform(0,1). Keep top-k by key.
    
    Time: O(n log k), Space: O(k)
    """
    import heapq
    if k <= 0:
        return []
    if seed is not None:
        random.seed(seed)
    heap: List[Tuple[float, int]] = []  # min-heap of (key, item)
    for item, w in stream:
        if w <= 0:
            # Skip non-positive weights
            continue
        u = random.random()
        key = u ** (1.0 / w)
        if len(heap) < k:
            heapq.heappush(heap, (key, item))
        else:
            if key > heap[0][0]:
                heapq.heapreplace(heap, (key, item))
    # return items (unordered)
    return [item for _, item in heap]

def infinite_stream(start: int = 0) -> Iterator[int]:
    """Helper generator for an infinite stream of integers."""
    x = start
    while True:
        yield x
        x += 1

def demo():
    print("Reservoir Sampling Demo")
    print("=" * 35)
    
    data = list(range(1, 101))  # 1..100
    
    # k=1 sampling
    s = reservoir_sample_one(data, seed=42)
    print(f"k=1 sample from 1..100 (seed=42): {s}")
    
    # k=10 uniform sampling
    samp10 = reservoir_sample_k(data, 10, seed=42)
    print(f"k=10 uniform sample from 1..100 (seed=42): {sorted(samp10)}")
    
    # Weighted sampling: favor larger numbers (weight = value)
    weighted_stream = [(x, float(x)) for x in data]
    w_samp = reservoir_sample_k_weighted(weighted_stream, 10, seed=42)
    print(f"k=10 weighted sample (weights=x): {sorted(w_samp)}  (bias towards larger x)")
    
    # Sampling from a stream that is too small
    small = [10, 20, 30]
    print(f"Reservoir sample k=5 from small stream {small}: {reservoir_sample_k(small, 5, seed=1)}")
    
    # Infinite stream sampling demonstration (take first 1000 values)
    inf = infinite_stream(0)
    # We can't consume infinite streams entirely; simulate consuming first 1000
    import itertools
    inf_sample = reservoir_sample_k(itertools.islice(inf, 1000), 5, seed=123)
    print(f"Reservoir sample k=5 from first 1000 ints: {sorted(inf_sample)}")
    
    print()
    print("Notes & Interview Tips:")
    print("  - Reservoir sampling selects a uniform sample from a stream without knowing its length in advance.")
    print("  - k=1: replace current sample with probability 1/i at i-th element.")
    print("  - k>1: keep initial k items; for i>k, replace random index < k with probability k/i.")
    print("  - Weighted variant (Efraimidis-Spirakis) supports probabilities proportional to weights.")

if __name__ == '__main__':
    demo()
