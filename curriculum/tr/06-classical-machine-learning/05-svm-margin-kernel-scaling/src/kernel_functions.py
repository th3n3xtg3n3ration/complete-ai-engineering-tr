"""Kernel and hinge-loss utilities for support vector machines."""

from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike, NDArray

def linear_kernel(x: ArrayLike, z: ArrayLike) -> NDArray[np.float64]:
    x_arr = np.atleast_2d(np.asarray(x, dtype=float))
    z_arr = np.atleast_2d(np.asarray(z, dtype=float))
    if x_arr.shape[1] != z_arr.shape[1]:
        raise ValueError("x and z must have the same number of features")
    return x_arr @ z_arr.T

def polynomial_kernel(x: ArrayLike, z: ArrayLike, *, degree: int = 3, gamma: float = 1.0, coef0: float = 1.0) -> NDArray[np.float64]:
    if degree < 1:
        raise ValueError("degree must be at least 1")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    return (gamma * linear_kernel(x, z) + coef0) ** degree

def rbf_kernel(x: ArrayLike, z: ArrayLike, *, gamma: float = 1.0) -> NDArray[np.float64]:
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    x_arr = np.atleast_2d(np.asarray(x, dtype=float))
    z_arr = np.atleast_2d(np.asarray(z, dtype=float))
    if x_arr.shape[1] != z_arr.shape[1]:
        raise ValueError("x and z must have the same number of features")
    distances = np.sum(x_arr**2, axis=1)[:, None] + np.sum(z_arr**2, axis=1)[None, :] - 2.0 * x_arr @ z_arr.T
    return np.exp(-gamma * np.maximum(distances, 0.0))

def hinge_loss(y_true: ArrayLike, decision_scores: ArrayLike) -> float:
    y_arr = np.asarray(y_true, dtype=float).reshape(-1)
    score_arr = np.asarray(decision_scores, dtype=float).reshape(-1)
    if y_arr.shape != score_arr.shape:
        raise ValueError("y_true and decision_scores must have equal length")
    if not np.all(np.isin(y_arr, (-1.0, 1.0))):
        raise ValueError("y_true must contain only -1 and +1")
    return float(np.mean(np.maximum(0.0, 1.0 - y_arr * score_arr)))

def svm_primal_objective(weights: ArrayLike, y_true: ArrayLike, decision_scores: ArrayLike, *, c: float = 1.0) -> float:
    if c <= 0:
        raise ValueError("c must be positive")
    w = np.asarray(weights, dtype=float).reshape(-1)
    y = np.asarray(y_true, dtype=float).reshape(-1)
    s = np.asarray(decision_scores, dtype=float).reshape(-1)
    if y.shape != s.shape:
        raise ValueError("y_true and decision_scores must have equal length")
    if not np.all(np.isin(y, (-1.0, 1.0))):
        raise ValueError("y_true must contain only -1 and +1")
    return float(0.5 * np.dot(w, w) + c * np.sum(np.maximum(0.0, 1.0 - y * s)))

def margin_width(weights: ArrayLike) -> float:
    norm = float(np.linalg.norm(np.asarray(weights, dtype=float)))
    if norm == 0.0:
        raise ValueError("weights must not be all zeros")
    return 2.0 / norm
