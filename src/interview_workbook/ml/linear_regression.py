from __future__ import annotations

from typing import List, Sequence


def _matvec(a: List[List[float]], v: Sequence[float]) -> List[float]:
    return [sum(ai * vi for ai, vi in zip(row, v)) for row in a]


def _add_bias(x: List[List[float]]) -> List[List[float]]:
    return [[1.0] + row for row in x]


class LinearRegressionGD:
    """
    Linear regression trained with gradient descent (MSE loss, optional L2).
    Pure Python implementation; suitable for small instructional datasets.
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

    def fit(self, X: List[List[float]], y: Sequence[float]) -> "LinearRegressionGD":
        n = len(X)
        if n == 0:
            raise ValueError("Empty dataset")
        Xb = _add_bias(X) if self.fit_intercept else X
        d = len(Xb[0])

        # Initialize weights
        w = [0.0] * d

        for _ in range(self.epochs):
            # Predictions and residuals
            y_hat = _matvec(Xb, w)
            residuals = [yh - yt for yh, yt in zip(y_hat, y)]

            # Gradient: (X^T (Xw - y)) / n + l2 * w (no penalty on bias)
            grad = [0.0] * d
            for j in range(d):
                grad[j] = sum(Xb[i][j] * residuals[i] for i in range(n)) / n
                if self.l2 > 0 and (not self.fit_intercept or j > 0):
                    grad[j] += self.l2 * w[j]

            # Update
            old_w = w[:]
            w = [wj - self.lr * gj for wj, gj in zip(w, grad)]

            # Early stop if tiny update
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

    def predict(self, X: List[List[float]]) -> List[float]:
        if self.fit_intercept:
            Xb = _add_bias(X)
            w = [self.intercept_, *self.coef_]
        else:
            Xb = X
            w = self.coef_
        return _matvec(Xb, w)
