from __future__ import annotations

import math
import random
from typing import Any

Point = tuple[float, float]
LabeledPoint = tuple[float, float, int]


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _dsigmoid(y: float) -> float:
    # derivative with respect to pre-activation if y is sigmoid(z): y * (1 - y)
    return y * (1.0 - y)


def _tanh(x: float) -> float:
    return math.tanh(x)


def _dtanh(y: float) -> float:
    # derivative if y = tanh(x): 1 - y^2
    return 1.0 - y * y


def _rand_uniform(rng: random.Random, a: float, b: float) -> float:
    return a + (b - a) * rng.random()


def _color_bound(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def generate_blobs(n: int, seed: int | None) -> list[LabeledPoint]:
    rng = random.Random(seed)
    # two Gaussian-ish blobs
    c1 = (0.35, 0.35)
    c2 = (0.65, 0.65)
    s1 = 0.10
    s2 = 0.10
    out: list[LabeledPoint] = []
    for i in range(n):
        if i % 2 == 0:
            x = _color_bound(rng.gauss(c1[0], s1))
            y = _color_bound(rng.gauss(c1[1], s1))
            out.append((x, y, 0))
        else:
            x = _color_bound(rng.gauss(c2[0], s2))
            y = _color_bound(rng.gauss(c2[1], s2))
            out.append((x, y, 1))
    return out


def generate_moons(n: int, seed: int | None) -> list[LabeledPoint]:
    rng = random.Random(seed)
    # Two interleaving half-circles in [0,1]^2
    out: list[LabeledPoint] = []
    for i in range(n):
        t = _rand_uniform(rng, 0.0, math.pi)
        noise = 0.06
        if i % 2 == 0:
            # first moon centered around (0.5, 0.5)
            x = 0.5 + 0.35 * math.cos(t) + _rand_uniform(rng, -noise, noise)
            y = 0.55 + 0.25 * math.sin(t) + _rand_uniform(rng, -noise, noise)
            out.append((_color_bound(x), _color_bound(y), 0))
        else:
            # second moon shifted
            x = 0.5 + 0.35 * math.cos(t) + 0.20 + _rand_uniform(rng, -noise, noise)
            y = 0.45 - 0.25 * math.sin(t) + _rand_uniform(rng, -noise, noise)
            out.append((_color_bound(x), _color_bound(y), 1))
    return out


def generate_dataset(
    kind: str = "blobs", n: int = 200, seed: int | None = None
) -> list[LabeledPoint]:
    if kind == "moons":
        return generate_moons(n, seed)
    return generate_blobs(n, seed)


# Simple 1-hidden-layer MLP for 2D -> 1 (binary classification) without numpy
class TinyMLP:
    def __init__(self, hidden: int, lr: float, seed: int | None = None) -> None:
        self.h = max(1, int(hidden))
        self.lr = float(lr)
        self.rng = random.Random(seed)
        # weights: W1: h x 2, b1: h, W2: 1 x h, b2: 1
        self.W1: list[list[float]] = [
            [self.rng.uniform(-1.0, 1.0) * 0.5 for _ in range(2)] for _ in range(self.h)
        ]
        self.b1: list[float] = [0.0 for _ in range(self.h)]
        self.W2: list[float] = [
            self.rng.uniform(-1.0, 1.0) * 0.5 for _ in range(self.h)
        ]  # shape (h,)
        self.b2: float = 0.0

    def forward(self, x: Point) -> tuple[list[float], float]:
        # x: (2,)
        # z1 = W1 x + b1
        z1 = [self.W1[i][0] * x[0] + self.W1[i][1] * x[1] + self.b1[i] for i in range(self.h)]
        a1 = [_tanh(z) for z in z1]
        # z2 = W2 a1 + b2
        z2 = sum(self.W2[i] * a1[i] for i in range(self.h)) + self.b2
        yhat = _sigmoid(z2)
        return a1, yhat

    def backward_update(self, x: Point, y: int) -> float:
        # Forward
        a1, yhat = self.forward(x)
        # Binary cross-entropy loss derivative: dL/dz2 = (yhat - y)
        # Note: for sigmoid + BCE, derivative simplifies to (yhat - y)
        dz2 = yhat - float(y)
        # Gradients for W2, b2
        dW2 = [dz2 * a1[i] for i in range(self.h)]
        db2 = dz2
        # Backprop to hidden: dz1_i = (W2_i * dz2) * dtanh(a1_i)
        dz1 = [(self.W2[i] * dz2) * _dtanh(a1[i]) for i in range(self.h)]
        # Gradients for W1 and b1
        dW1 = [[dz1[i] * x[0], dz1[i] * x[1]] for i in range(self.h)]
        db1 = dz1[:]

        # SGD update
        for i in range(self.h):
            self.W2[i] -= self.lr * dW2[i]
        self.b2 -= self.lr * db2
        for i in range(self.h):
            self.W1[i][0] -= self.lr * dW1[i][0]
            self.W1[i][1] -= self.lr * dW1[i][1]
            self.b1[i] -= self.lr * db1[i]

        # loss for monitoring (BCE)
        eps = 1e-9
        loss = -(float(y) * math.log(yhat + eps) + (1.0 - float(y)) * math.log(1.0 - yhat + eps))
        return loss

    def predict_proba(self, x: Point) -> float:
        _, yhat = self.forward(x)
        return yhat


def _frame(epoch: int, loss: float, grid_probs: list[list[float]]) -> dict[str, Any]:
    return {"epoch": epoch, "loss": loss, "grid": grid_probs}


def _make_grid_probs(model: TinyMLP, res: int = 32) -> list[list[float]]:
    # Compute probabilities on a res x res grid in [0,1]x[0,1]
    out: list[list[float]] = []
    for j in range(res):
        row: list[float] = []
        y = j / (res - 1) if res > 1 else 0.0
        for i in range(res):
            x = i / (res - 1) if res > 1 else 0.0
            p = model.predict_proba((x, y))
            row.append(p)
        out.append(row)
    return out


def visualize(
    dataset: str = "blobs",
    n: int = 200,
    hidden: int = 8,
    lr: float = 0.5,
    epochs: int = 50,
    seed: int | None = None,
    grid: int = 32,
) -> dict[str, Any]:
    # Generate dataset
    pts = generate_dataset(dataset, n=n, seed=seed)

    # Initialize model
    model = TinyMLP(hidden=hidden, lr=lr, seed=seed)

    # Train for 'epochs' over all points (1 pass per epoch, shuffled)
    rng = random.Random(seed)
    frames: list[dict[str, Any]] = []
    losses: list[float] = []
    max_frames = 60  # cap frames to manage payload
    capture_every = max(1, epochs // max_frames)

    for epoch in range(1, epochs + 1):
        rng.shuffle(pts)
        total_loss = 0.0
        for x, y, lbl in pts:
            total_loss += model.backward_update((x, y), lbl)
        avg_loss = total_loss / max(1, len(pts))
        losses.append(avg_loss)

        if epoch == 1 or epoch % capture_every == 0 or epoch == epochs:
            grid_probs = _make_grid_probs(model, res=max(8, min(64, grid)))
            frames.append(_frame(epoch=epoch, loss=avg_loss, grid_probs=grid_probs))

    # Serialize dataset for front-end
    points = [{"x": x, "y": y, "label": lbl} for (x, y, lbl) in pts]
    return {
        "algorithm": "nn_binary",
        "name": "MLP Binary Classifier (1 hidden layer, tanh + sigmoid)",
        "dataset": dataset,
        "n": n,
        "hidden": hidden,
        "lr": lr,
        "epochs": epochs,
        "seed": seed,
        "grid": grid,
        "frames": frames,
        "points": points,
        "losses": losses,
    }
