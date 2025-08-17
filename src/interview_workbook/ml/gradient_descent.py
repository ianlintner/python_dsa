from __future__ import annotations

import random
from typing import Callable, Iterable, List, Optional, Sequence

Vector = List[float]


def _vec_sub(a: Sequence[float], b: Sequence[float]) -> Vector:
    return [x - y for x, y in zip(a, b)]


def _scalar_mul(s: float, v: Sequence[float]) -> Vector:
    return [s * x for x in v]


def _l2_norm_sq(v: Sequence[float]) -> float:
    return sum(x * x for x in v)


def batch_gradient_descent(
    grad_fn: Callable[[Vector], Vector],
    init_params: Sequence[float],
    lr: float = 0.01,
    epochs: int = 1000,
    tol: float = 1e-8,
    callback: Optional[Callable[[int, Vector, Vector], None]] = None,
) -> Vector:
    """
    Generic batch gradient descent.
    - grad_fn(params) -> gradient vector
    - init_params: initial parameter vector
    - lr: learning rate
    - tol: stops early when ||grad||^2 < tol
    - callback(t, params, grad): optional hook per epoch
    """
    params = list(init_params)
    for t in range(epochs):
        g = grad_fn(params)
        if _l2_norm_sq(g) < tol:
            if callback:
                callback(t, params, g)
            break
        params = _vec_sub(params, _scalar_mul(lr, g))
        if callback:
            callback(t, params, g)
    return params


def sgd(
    grad_sample_fn: Callable[[Vector, object], Vector],
    init_params: Sequence[float],
    data: Iterable[object],
    lr: float = 0.01,
    epochs: int = 10,
    shuffle: bool = True,
    callback: Optional[Callable[[int, int, Vector, Vector], None]] = None,
) -> Vector:
    """
    Stochastic gradient descent.
    - grad_sample_fn(params, sample) -> gradient for a single sample
    - data: iterable of training samples
    - callback(epoch, step, params, grad)
    """
    params = list(init_params)
    data_list = list(data)
    for epoch in range(epochs):
        if shuffle:
            random.shuffle(data_list)
        for step, sample in enumerate(data_list):
            g = grad_sample_fn(params, sample)
            params = _vec_sub(params, _scalar_mul(lr, g))
            if callback:
                callback(epoch, step, params, g)
    return params


def minibatch_sgd(
    grad_batch_fn: Callable[[Vector, Sequence[object]], Vector],
    init_params: Sequence[float],
    data: Sequence[object],
    batch_size: int = 32,
    lr: float = 0.01,
    epochs: int = 10,
    shuffle: bool = True,
    callback: Optional[Callable[[int, int, Vector, Vector], None]] = None,
) -> Vector:
    """
    Mini-batch SGD.
    - grad_batch_fn(params, batch) -> gradient for a mini-batch
    - data: sequence for efficient batching
    - callback(epoch, batch_index, params, grad)
    """
    params = list(init_params)
    n = len(data)
    indices = list(range(n))
    for epoch in range(epochs):
        if shuffle:
            random.shuffle(indices)
        for b, i in enumerate(range(0, n, batch_size)):
            batch_idx = indices[i : i + batch_size]
            batch = [data[j] for j in batch_idx]
            g = grad_batch_fn(params, batch)
            params = _vec_sub(params, _scalar_mul(lr, g))
            if callback:
                callback(epoch, b, params, g)
    return params
