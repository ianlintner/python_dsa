from __future__ import annotations

import random
from typing import Any, Dict, List, Optional


def _snap(arr: List[int], op: str = "", **markers: Any) -> Dict[str, Any]:
    """
    Create a JSON-serializable snapshot of array state plus marker indices.
    Markers can include: lo, hi, mid, l, r, win_l, win_r, best_l, best_r, found, sum
    """
    snap: Dict[str, Any] = {"arr": arr[:], "op": op}
    for k, v in markers.items():
        if isinstance(v, (int, type(None))):
            snap[k] = v
        else:
            snap[k] = v
    return snap


def generate_array(
    n: int = 30, seed: Optional[int] = None, unique: bool = True, sorted_: bool = True
) -> List[int]:
    rng = random.Random(seed)
    if unique:
        arr = list(range(1, n + 1))
        rng.shuffle(arr)
    else:
        arr = [rng.randint(1, n) for _ in range(n)]
    if sorted_:
        arr.sort()
    return arr


def binary_search_frames(
    arr: List[int], target: int, max_steps: int = 20000
) -> List[Dict[str, Any]]:
    a = arr[:]
    frames: List[Dict[str, Any]] = [_snap(a, "init", lo=0, hi=len(a) - 1, mid=None, found=False)]
    lo, hi = 0, len(a) - 1
    steps = 0
    while lo <= hi and steps < max_steps:
        mid = (lo + hi) // 2
        frames.append(_snap(a, "check-mid", lo=lo, hi=hi, mid=mid, found=False))
        if a[mid] == target:
            frames.append(_snap(a, "found", lo=lo, hi=hi, mid=mid, found=True))
            return frames
        if a[mid] < target:
            lo = mid + 1
            frames.append(_snap(a, "move-right", lo=lo, hi=hi, mid=mid, found=False))
        else:
            hi = mid - 1
            frames.append(_snap(a, "move-left", lo=lo, hi=hi, mid=mid, found=False))
        steps += 1
    frames.append(_snap(a, "not-found", lo=lo, hi=hi, mid=None, found=False))
    return frames


def two_pointers_sum_frames(
    arr_sorted: List[int], target: int, max_steps: int = 20000
) -> List[Dict[str, Any]]:
    a = sorted(arr_sorted[:])
    l, r = 0, len(a) - 1
    frames: List[Dict[str, Any]] = [_snap(a, "init", l=l, r=r, sum=None)]
    steps = 0
    while l < r and steps < max_steps:
        s = a[l] + a[r]
        frames.append(_snap(a, "check", l=l, r=r, sum=s, target=target))
        if s == target:
            frames.append(_snap(a, "found", l=l, r=r, sum=s, target=target))
            return frames
        if s < target:
            l += 1
            frames.append(_snap(a, "move-left", l=l, r=r, sum=None, target=target))
        else:
            r -= 1
            frames.append(_snap(a, "move-right", l=l, r=r, sum=None, target=target))
        steps += 1
    frames.append(_snap(a, "not-found", l=l, r=r, sum=None, target=target))
    return frames


def sliding_window_min_len_geq_frames(
    arr: List[int], target: int, max_steps: int = 20000
) -> List[Dict[str, Any]]:
    """
    Classic: minimum length of subarray with sum >= target.
    Frames show expanding/shrinking window [win_l, win_r] and best window when updated.
    """
    a = arr[:]
    frames: List[Dict[str, Any]] = [
        _snap(a, "init", win_l=0, win_r=-1, best_l=None, best_r=None, s=0, target=target)
    ]
    n = len(a)
    s = 0
    best = (10**9, None, None)  # (len, l, r)
    l = 0
    steps = 0
    for r in range(n):
        s += a[r]
        frames.append(
            _snap(a, "expand", win_l=l, win_r=r, best_l=best[1], best_r=best[2], s=s, target=target)
        )
        while s >= target and steps < max_steps:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r)
                frames.append(
                    _snap(
                        a,
                        "best",
                        win_l=l,
                        win_r=r,
                        best_l=best[1],
                        best_r=best[2],
                        s=s,
                        target=target,
                    )
                )
            s -= a[l]
            l += 1
            frames.append(
                _snap(
                    a,
                    "shrink",
                    win_l=l,
                    win_r=r,
                    best_l=best[1],
                    best_r=best[2],
                    s=s,
                    target=target,
                )
            )
            steps += 1
        if steps >= max_steps:
            break
        steps += 1
    frames.append(
        _snap(a, "done", win_l=l, win_r=n - 1, best_l=best[1], best_r=best[2], s=s, target=target)
    )
    return frames


ALGORITHMS = {
    "binary_search": {
        "name": "Binary Search",
        "frames": binary_search_frames,
        "needs_sorted": True,
        "default_n": 30,
    },
    "two_pointers_sum": {
        "name": "Two Pointers (Two-Sum in Sorted Array)",
        "frames": two_pointers_sum_frames,
        "needs_sorted": True,
        "default_n": 30,
    },
    "sliding_window_min_len_geq": {
        "name": "Sliding Window (Min Len with Sum ≥ target)",
        "frames": sliding_window_min_len_geq_frames,
        "needs_sorted": False,
        "default_n": 30,
    },
}


def visualize(
    algo_key: str,
    n: int = 30,
    seed: Optional[int] = None,
    target: Optional[int] = None,
) -> Dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    needs_sorted = bool(algo.get("needs_sorted"))
    arr = generate_array(n=n, seed=seed, unique=False, sorted_=needs_sorted)
    if target is None:
        rng = random.Random(seed)
        # Choose a target roughly in range of sums
        if algo_key == "two_pointers_sum":
            if len(arr) >= 2:
                target = arr[0] + arr[-1]
            else:
                target = rng.randint(2, max(3, n))
        elif algo_key == "sliding_window_min_len_geq":
            target = max(1, int(sum(arr) / max(2, n // 3)))
        else:  # binary search
            target = arr[len(arr) // 2] if arr else 1
    frames = algo["frames"](arr, target)  # type: ignore[arg-type]
    max_val = max(arr) if arr else 1
    return {
        "algorithm": algo_key,
        "name": algo["name"],
        "n": n,
        "max": max_val,
        "frames": frames,
        "array": arr,
        "target": target,
    }
