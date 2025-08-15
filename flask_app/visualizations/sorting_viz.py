from __future__ import annotations

import random
from typing import Any


def _snap(
    arr: list[int], a: int | None = None, b: int | None = None, op: str = ""
) -> dict[str, Any]:
    # Return a JSON-serializable snapshot
    return {"arr": arr[:], "a": a, "b": b, "op": op}


def generate_array(n: int = 30, seed: int | None = None, unique: bool = True) -> list[int]:
    """
    Generate a random array for visualization.
    - If unique: values are 1..n shuffled
    - Else: values are random in [1, n]
    """
    rng = random.Random(seed)
    if unique:
        arr = list(range(1, n + 1))
        rng.shuffle(arr)
        return arr
    return [rng.randint(1, n) for _ in range(n)]


def bubble_sort_frames(arr: list[int], max_steps: int = 20000) -> list[dict[str, Any]]:
    a = arr[:]
    frames: list[dict[str, Any]] = [_snap(a)]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            frames.append(_snap(a, j, j + 1, "compare"))
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                frames.append(_snap(a, j, j + 1, "swap"))
            if len(frames) >= max_steps:
                return frames
        if not swapped:
            break
    frames.append(_snap(a))
    return frames


def insertion_sort_frames(arr: list[int], max_steps: int = 20000) -> list[dict[str, Any]]:
    a = arr[:]
    frames: list[dict[str, Any]] = [_snap(a)]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        frames.append(_snap(a, j, i, "key"))
        while j >= 0 and a[j] > key:
            frames.append(_snap(a, j, i, "compare"))
            a[j + 1] = a[j]
            frames.append(_snap(a, j, j + 1, "shift"))
            j -= 1
            if len(frames) >= max_steps:
                return frames
        a[j + 1] = key
        frames.append(_snap(a, j + 1, i, "insert"))
    frames.append(_snap(a))
    return frames


def quick_sort_frames(
    arr: list[int], max_steps: int = 40000, randomized: bool = True
) -> list[dict[str, Any]]:
    a = arr[:]
    frames: list[dict[str, Any]] = [_snap(a)]

    rng = random.Random()

    def partition(lo: int, hi: int) -> int:
        nonlocal frames
        if randomized:
            p = rng.randint(lo, hi)
            a[p], a[hi] = a[hi], a[p]
            frames.append(_snap(a, p, hi, "choose-pivot"))
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            frames.append(_snap(a, j, hi, "compare-pivot"))
            if a[j] <= pivot:
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    frames.append(_snap(a, i, j, "swap"))
                i += 1
            if len(frames) >= max_steps:
                return i
        a[i], a[hi] = a[hi], a[i]
        frames.append(_snap(a, i, hi, "swap-pivot"))
        return i

    def qs(lo: int, hi: int) -> None:
        if lo >= hi or len(frames) >= max_steps:
            return
        p = partition(lo, hi)
        qs(lo, p - 1)
        qs(p + 1, hi)

    qs(0, len(a) - 1)
    frames.append(_snap(a))
    return frames


ALGORITHMS = {
    "bubble": {
        "name": "Bubble Sort",
        "frames": bubble_sort_frames,
        "default_n": 30,
    },
    "insertion": {
        "name": "Insertion Sort",
        "frames": insertion_sort_frames,
        "default_n": 30,
    },
    "quick": {
        "name": "Quick Sort",
        "frames": quick_sort_frames,
        "default_n": 40,
    },
}


def visualize(
    algorithm_key: str, n: int = 30, seed: int | None = None, unique: bool = True
) -> dict[str, Any]:
    algo = ALGORITHMS.get(algorithm_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algorithm_key}'")

    arr = generate_array(n=n, seed=seed, unique=unique)
    frames = algo["frames"](arr)
    max_val = max(arr) if arr else 1
    return {
        "algorithm": algorithm_key,
        "name": algo["name"],
        "n": n,
        "max": max_val,
        "frames": frames,
        "seed": seed,
        "unique": unique,
    }
