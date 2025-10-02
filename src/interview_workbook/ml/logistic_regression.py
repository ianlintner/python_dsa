from __future__ import annotations

import math
from typing import List, Sequence


def _sigmoid(z: float) -> float:
    # Stable sigmoid
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _add_bias(x: List[List[float]]) -> List[List[float]]:
    return [[1.0] + row for row in x]


class LogisticRegressionBinary:
    """
    Binary logistic regression with L2 regularization (pure Python).
    y is expected to be 0/1.
    """

    def __init__(
        self,
        lr: float = 0.1,
        epochs: int = 1000,
        l2: float = 0.0,
        fit_intercept: bool = True,
        tol: float = 0.0,
    ) -> None:
        self.lr = lr
        self.epochs = epochs
        self.l2 = l2
        self.fit_intercept = fit_intercept
        self.tol = tol
        self.coef_: List[float] = []
        self.intercept_: float = 0.0

    def fit(self, X: List[List[float]], y: Sequence[int]) -> "LogisticRegressionBinary":
        n = len(X)
        if n == 0:
            raise ValueError("Empty dataset")
        Xb = _add_bias(X) if self.fit_intercept else X
        d = len(Xb[0])

        w = [0.0] * d
        for _ in range(self.epochs):
            # Predictions
            logits = [sum(wj * xj for wj, xj in zip(w, xi)) for xi in Xb]
            probs = [_sigmoid(z) for z in logits]

            # Gradient: X^T (p - y) / n + l2 * w (no penalty on bias)
            grad = [0.0] * d
            for j in range(d):
                grad[j] = sum(Xb[i][j] * (probs[i] - y[i]) for i in range(n)) / n
                if self.l2 > 0 and (not self.fit_intercept or j > 0):
                    grad[j] += self.l2 * w[j]

            old_w = w[:]
            w = [wj - self.lr * gj for wj, gj in zip(w, grad)]
            if (
                self.tol > 0
                and sum((wj - owj) ** 2 for wj, owj in zip(w, old_w)) < self.tol
            ):
                break

        if self.fit_intercept:
            self.intercept_ = w[0]
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def predict_proba(self, X: List[List[float]]) -> List[float]:
        if self.fit_intercept:
            Xb = _add_bias(X)
            w = [self.intercept_, *self.coef_]
        else:
            Xb = X
            w = self.coef_
        logits = [sum(wj * xj for wj, xj in zip(w, xi)) for xi in Xb]
        return [_sigmoid(z) for z in logits]

    def predict(self, X: List[List[float]]) -> List[int]:
        return [1 if p >= 0.5 else 0 for p in self.predict_proba(X)]
