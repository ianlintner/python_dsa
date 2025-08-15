from __future__ import annotations

import random
from typing import Any


def _snap(arr: list[int], op: str = "", **markers: Any) -> dict[str, Any]:
    """
    Create a JSON-serializable snapshot of array state plus marker indices.
    Markers can include: lo, hi, mid, l, r, win_l, win_r, best_l, best_r, found, sum
    """
    snap: dict[str, Any] = {"arr": arr[:], "op": op}
    for k, v in markers.items():
        # Keep as-is; front-end handles None and numbers
        snap[k] = v
    return snap


def generate_array(
    n: int = 30, seed: int | None = None, unique: bool = True, sorted_: bool = True
) -> list[int]:
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
    arr: list[int], target: int, max_steps: int = 20000
) -> list[dict[str, Any]]:
    a = arr[:]
    frames: list[dict[str, Any]] = [_snap(a, "init", lo=0, hi=len(a) - 1, mid=None, found=False)]
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
    arr_sorted: list[int], target: int, max_steps: int = 20000
) -> list[dict[str, Any]]:
    a = sorted(arr_sorted[:])
    left, right = 0, len(a) - 1
    frames: list[dict[str, Any]] = [_snap(a, "init", l=left, r=right, sum=None)]
    steps = 0
    while left < right and steps < max_steps:
        s = a[left] + a[right]
        frames.append(_snap(a, "check", l=left, r=right, sum=s, target=target))
        if s == target:
            frames.append(_snap(a, "found", l=left, r=right, sum=s, target=target))
            return frames
        if s < target:
            left += 1
            frames.append(_snap(a, "move-left", l=left, r=right, sum=None, target=target))
        else:
            right -= 1
            frames.append(_snap(a, "move-right", l=left, r=right, sum=None, target=target))
        steps += 1
    frames.append(_snap(a, "not-found", l=left, r=right, sum=None, target=target))
    return frames


def sliding_window_min_len_geq_frames(
    arr: list[int], target: int, max_steps: int = 20000
) -> list[dict[str, Any]]:
    """
    Classic: minimum length of subarray with sum >= target.
    Frames show expanding/shrinking window [win_l, win_r] and best window when updated.
    """
    a = arr[:]
    frames: list[dict[str, Any]] = [
        _snap(a, "init", win_l=0, win_r=-1, best_l=None, best_r=None, s=0, target=target)
    ]
    n = len(a)
    s = 0
    best = (10**9, None, None)  # (len, l, r)
    left = 0
    steps = 0
    for r in range(n):
        s += a[r]
        frames.append(
            _snap(
                a, "expand", win_l=left, win_r=r, best_l=best[1], best_r=best[2], s=s, target=target
            )
        )
        while s >= target and steps < max_steps:
            if r - left + 1 < best[0]:
                best = (r - left + 1, left, r)
                frames.append(
                    _snap(
                        a,
                        "best",
                        win_l=left,
                        win_r=r,
                        best_l=best[1],
                        best_r=best[2],
                        s=s,
                        target=target,
                    )
                )
            s -= a[left]
            left += 1
            frames.append(
                _snap(
                    a,
                    "shrink",
                    win_l=left,
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
        _snap(
            a, "done", win_l=left, win_r=n - 1, best_l=best[1], best_r=best[2], s=s, target=target
        )
    )
    return frames


ALGORITHMS: dict[str, dict[str, Any]] = {
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
    seed: int | None = None,
    target: int | None = None,
) -> dict[str, Any]:
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        raise ValueError(f"Unknown algorithm '{algo_key}'")
    needs_sorted = bool(algo.get("needs_sorted"))
    arr = generate_array(n=n, seed=seed, unique=False, sorted_=needs_sorted)

    if target is None:
        rng = random.Random(seed)
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
