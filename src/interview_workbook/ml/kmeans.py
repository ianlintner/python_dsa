from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence

Point = List[float]


def _dist2(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def _mean(points: List[Point]) -> Point:
    if not points:
        raise ValueError("Cannot compute mean of empty set")
    d = len(points[0])
    s = [0.0] * d
    for p in points:
        for j in range(d):
            s[j] += p[j]
    return [v / len(points) for v in s]


def _kmeanspp_init(X: List[Point], k: int, rng: random.Random) -> List[Point]:
    centroids = [rng.choice(X)]
    while len(centroids) < k:
        # Compute D(x)^2
        d2 = []
        for x in X:
            m = min(_dist2(x, c) for c in centroids)
            d2.append(m)
        total = sum(d2)
        # Sample proportional to D(x)^2
        r = rng.random() * total if total > 0 else 0.0
        s = 0.0
        chosen = X[0]
        for x, w in zip(X, d2):
            s += w
            if s >= r:
                chosen = x[:]
                break
        centroids.append(chosen)
    return centroids


class KMeans:
    """K-Means clustering (Lloyd's algorithm) with k-means++ init."""

    def __init__(
        self,
        n_clusters: int,
        max_iter: int = 100,
        tol: float = 1e-4,
        init: str = "k-means++",
        random_state: Optional[int] = None,
    ) -> None:
        if n_clusters <= 0:
            raise ValueError("n_clusters must be > 0")
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.init = init
        self.random_state = random_state
        self.cluster_centers_: List[Point] = []
        self.labels_: List[int] = []

    def fit(self, X: List[Point]) -> "KMeans":
        if not X:
            raise ValueError("Empty dataset")
        rng = random.Random(self.random_state)

        if self.init == "k-means++":
            centroids = _kmeanspp_init(X, self.n_clusters, rng)
        else:
            centroids = rng.sample(X, self.n_clusters)

        for _ in range(self.max_iter):
            # Assign
            labels = [
                min(range(self.n_clusters), key=lambda c: _dist2(x, centroids[c]))
                for x in X
            ]
            # Recompute
            new_centroids: List[Point] = []
            for c in range(self.n_clusters):
                members = [x for x, lbl in zip(X, labels) if lbl == c]
                if members:
                    new_centroids.append(_mean(members))
                else:
                    # Reinitialize empty cluster
                    new_centroids.append(rng.choice(X)[:])

            # Check movement
            shift = sum(
                math.sqrt(_dist2(a, b)) for a, b in zip(centroids, new_centroids)
            )
            centroids = new_centroids
            if shift < self.tol:
                break

        self.cluster_centers_ = centroids
        self.labels_ = [
            min(range(self.n_clusters), key=lambda c: _dist2(x, centroids[c]))
            for x in X
        ]
        return self

    def predict(self, X: List[Point]) -> List[int]:
        if not self.cluster_centers_:
            raise RuntimeError("Model not fitted")
        return [
            min(
                range(self.n_clusters),
                key=lambda c: _dist2(x, self.cluster_centers_[c]),
            )
            for x in X
        ]
