"""Logistic regression primitives implemented with NumPy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

ClassWeight = Literal["balanced"] | dict[int, float] | None


def sigmoid(values: ArrayLike) -> NDArray[np.float64]:
    """Return a numerically stable sigmoid transformation."""

    array = np.asarray(values, dtype=float)
    output = np.empty_like(array, dtype=float)
    positive = array >= 0
    output[positive] = 1.0 / (1.0 + np.exp(-array[positive]))
    negative_exp = np.exp(array[~positive])
    output[~positive] = negative_exp / (1.0 + negative_exp)
    return output


def binary_log_loss(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    sample_weight: ArrayLike | None = None,
    epsilon: float = 1e-15,
) -> float:
    """Compute binary cross-entropy with optional sample weights."""

    targets = np.asarray(y_true, dtype=float).reshape(-1)
    scores = np.asarray(probabilities, dtype=float).reshape(-1)
    if targets.shape != scores.shape:
        raise ValueError("y_true and probabilities must have equal shape")
    if targets.size == 0:
        raise ValueError("at least one observation is required")
    if not np.isin(targets, [0.0, 1.0]).all():
        raise ValueError("y_true must contain only 0 and 1")
    clipped = np.clip(scores, epsilon, 1.0 - epsilon)
    losses = -(targets * np.log(clipped) + (1.0 - targets) * np.log(1.0 - clipped))
    if sample_weight is None:
        return float(np.mean(losses))
    weights = np.asarray(sample_weight, dtype=float).reshape(-1)
    if weights.shape != targets.shape:
        raise ValueError("sample_weight must match y_true")
    if np.any(weights < 0) or float(weights.sum()) <= 0:
        raise ValueError("sample_weight must be non-negative with positive sum")
    return float(np.average(losses, weights=weights))


def _validate_binary_data(
    features: ArrayLike,
    target: ArrayLike,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    matrix = np.asarray(features, dtype=float)
    labels = np.asarray(target, dtype=float).reshape(-1)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if matrix.ndim != 2:
        raise ValueError("features must be a two-dimensional matrix")
    if matrix.shape[0] != labels.shape[0]:
        raise ValueError("features and target must have equal row counts")
    if matrix.shape[0] == 0:
        raise ValueError("at least one observation is required")
    if not np.isfinite(matrix).all() or not np.isfinite(labels).all():
        raise ValueError("features and target must be finite")
    if not np.isin(labels, [0.0, 1.0]).all():
        raise ValueError("target must contain only 0 and 1")
    if np.unique(labels).size != 2:
        raise ValueError("target must contain both binary classes")
    return matrix, labels


def _sample_weights(target: NDArray[np.float64], class_weight: ClassWeight) -> NDArray[np.float64]:
    if class_weight is None:
        return np.ones_like(target, dtype=float)
    if class_weight == "balanced":
        counts = np.bincount(target.astype(int), minlength=2).astype(float)
        class_values = target.size / (2.0 * counts)
        return class_values[target.astype(int)]
    weights = np.array([float(class_weight.get(int(value), 1.0)) for value in target])
    if np.any(weights <= 0):
        raise ValueError("class weights must be positive")
    return weights


@dataclass
class LogisticRegressionGD:
    """Binary logistic regression trained with batch gradient descent."""

    learning_rate: float = 0.1
    max_iter: int = 2_000
    l2_strength: float = 0.0
    fit_intercept: bool = True
    tolerance: float = 1e-8
    class_weight: ClassWeight = None

    def __post_init__(self) -> None:
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.max_iter <= 0:
            raise ValueError("max_iter must be positive")
        if self.l2_strength < 0:
            raise ValueError("l2_strength must be non-negative")
        if self.tolerance < 0:
            raise ValueError("tolerance must be non-negative")
        self.coef_: NDArray[np.float64] | None = None
        self.intercept_: float = 0.0
        self.loss_history_: list[float] = []
        self.n_iter_: int = 0

    def fit(self, features: ArrayLike, target: ArrayLike) -> "LogisticRegressionGD":
        """Fit the model and store coefficients and optimization history."""

        matrix, labels = _validate_binary_data(features, target)
        weights = _sample_weights(labels, self.class_weight)
        coefficients = np.zeros(matrix.shape[1], dtype=float)
        intercept = 0.0
        previous_loss = np.inf
        self.loss_history_ = []

        for iteration in range(1, self.max_iter + 1):
            logits = matrix @ coefficients + intercept
            probabilities = sigmoid(logits)
            residual = probabilities - labels
            weighted_residual = residual * weights
            weight_total = float(weights.sum())
            gradient = matrix.T @ weighted_residual / weight_total
            gradient += self.l2_strength * coefficients
            intercept_gradient = float(weighted_residual.sum() / weight_total)

            coefficients -= self.learning_rate * gradient
            if self.fit_intercept:
                intercept -= self.learning_rate * intercept_gradient

            probabilities = sigmoid(matrix @ coefficients + intercept)
            loss = binary_log_loss(labels, probabilities, sample_weight=weights)
            loss += 0.5 * self.l2_strength * float(coefficients @ coefficients)
            self.loss_history_.append(loss)
            self.n_iter_ = iteration
            if abs(previous_loss - loss) <= self.tolerance:
                break
            previous_loss = loss

        self.coef_ = coefficients
        self.intercept_ = intercept if self.fit_intercept else 0.0
        return self

    def _check_fitted(self) -> NDArray[np.float64]:
        if self.coef_ is None:
            raise RuntimeError("fit must be called before prediction")
        return self.coef_

    def decision_function(self, features: ArrayLike) -> NDArray[np.float64]:
        """Return log-odds scores."""

        coefficients = self._check_fitted()
        matrix = np.asarray(features, dtype=float)
        if matrix.ndim == 1:
            matrix = matrix.reshape(-1, coefficients.size)
        if matrix.ndim != 2 or matrix.shape[1] != coefficients.size:
            raise ValueError("feature shape does not match fitted coefficients")
        return matrix @ coefficients + self.intercept_

    def predict_proba(self, features: ArrayLike) -> NDArray[np.float64]:
        """Return two-column class probabilities."""

        positive = sigmoid(self.decision_function(features))
        return np.column_stack((1.0 - positive, positive))

    def predict(self, features: ArrayLike, *, threshold: float = 0.5) -> NDArray[np.int64]:
        """Return binary predictions at a configurable threshold."""

        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")
        return (self.predict_proba(features)[:, 1] >= threshold).astype(int)
