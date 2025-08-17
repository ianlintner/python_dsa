from __future__ import annotations

import math
from typing import List


def relu(x: float) -> float:
    """ReLU activation function."""
    return max(0.0, x)


def relu_array(x: List[float]) -> List[float]:
    """ReLU applied element-wise to an array."""
    return [relu(xi) for xi in x]


def relu_derivative(x: float) -> float:
    """Derivative of ReLU."""
    return 1.0 if x > 0 else 0.0


def sigmoid(x: float) -> float:
    """Sigmoid activation function."""
    if x >= 0:
        ez = math.exp(-x)
        return 1.0 / (1.0 + ez)
    ez = math.exp(x)
    return ez / (1.0 + ez)


def sigmoid_array(x: List[float]) -> List[float]:
    """Sigmoid applied element-wise to an array."""
    return [sigmoid(xi) for xi in x]


def sigmoid_derivative(x: float) -> float:
    """Derivative of sigmoid (assumes x is sigmoid output)."""
    return x * (1.0 - x)


def tanh(x: float) -> float:
    """Hyperbolic tangent activation function."""
    return math.tanh(x)


def tanh_array(x: List[float]) -> List[float]:
    """Tanh applied element-wise to an array."""
    return [tanh(xi) for xi in x]


def tanh_derivative(x: float) -> float:
    """Derivative of tanh (assumes x is tanh output)."""
    return 1.0 - x * x


def softmax(x: List[float]) -> List[float]:
    """Softmax activation function."""
    # Stable softmax
    x_max = max(x)
    exp_x = [math.exp(xi - x_max) for xi in x]
    sum_exp = sum(exp_x)
    return [e / sum_exp for e in exp_x]
