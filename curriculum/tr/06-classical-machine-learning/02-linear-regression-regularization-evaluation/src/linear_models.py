"""From-scratch linear regression estimators for teaching purposes."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def _as_2d_float_array(values: object) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim == 1:
        array = array.reshape(-1, 1)
    if array.ndim != 2:
        raise ValueError("X must be one- or two-dimensional")
    if array.shape[0] == 0:
        raise ValueError("X must not be empty")
    if not np.isfinite(array).all():
        raise ValueError("X must contain only finite values")
    return array


def _as_1d_float_array(values: object) -> np.ndarray:
    array = np.asarray(values, dtype=float).reshape(-1)
    if array.size == 0:
        raise ValueError("y must not be empty")
    if not np.isfinite(array).all():
        raise ValueError("y must contain only finite values")
    return array


def _validate_xy(X: object, y: object) -> tuple[np.ndarray, np.ndarray]:
    x_array = _as_2d_float_array(X)
    y_array = _as_1d_float_array(y)
    if x_array.shape[0] != y_array.shape[0]:
        raise ValueError("X and y must contain the same number of rows")
    return x_array, y_array


@dataclass
class NormalEquationRegressor:
    """Ordinary least-squares estimator using a stable least-squares solve."""

    fit_intercept: bool = True
    coefficients_: np.ndarray | None = field(default=None, init=False)
    intercept_: float | None = field(default=None, init=False)
    rank_: int | None = field(default=None, init=False)
    singular_values_: np.ndarray | None = field(default=None, init=False)

    def fit(self, X: object, y: object) -> "NormalEquationRegressor":
        x_array, y_array = _validate_xy(X, y)
        design = (
            np.column_stack([np.ones(x_array.shape[0]), x_array])
            if self.fit_intercept
            else x_array
        )
        solution, _, rank, singular_values = np.linalg.lstsq(design, y_array, rcond=None)
        if self.fit_intercept:
            self.intercept_ = float(solution[0])
            self.coefficients_ = solution[1:].copy()
        else:
            self.intercept_ = 0.0
            self.coefficients_ = solution.copy()
        self.rank_ = int(rank)
        self.singular_values_ = singular_values.copy()
        return self

    def predict(self, X: object) -> np.ndarray:
        if self.coefficients_ is None or self.intercept_ is None:
            raise RuntimeError("model must be fit before prediction")
        x_array = _as_2d_float_array(X)
        if x_array.shape[1] != self.coefficients_.shape[0]:
            raise ValueError("X has a different feature count than training data")
        return x_array @ self.coefficients_ + self.intercept_


@dataclass
class GradientDescentRegressor:
    """Batch gradient-descent linear regression with optional L2 penalty."""

    learning_rate: float = 0.05
    max_iterations: int = 2_000
    tolerance: float = 1e-10
    l2_penalty: float = 0.0
    fit_intercept: bool = True
    coefficients_: np.ndarray | None = field(default=None, init=False)
    intercept_: float | None = field(default=None, init=False)
    loss_history_: list[float] = field(default_factory=list, init=False)
    n_iterations_: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        if self.tolerance < 0:
            raise ValueError("tolerance must be non-negative")
        if self.l2_penalty < 0:
            raise ValueError("l2_penalty must be non-negative")

    def fit(self, X: object, y: object) -> "GradientDescentRegressor":
        x_array, y_array = _validate_xy(X, y)
        n_rows, n_features = x_array.shape
        weights = np.zeros(n_features, dtype=float)
        intercept = 0.0
        previous_loss: float | None = None
        self.loss_history_ = []

        for iteration in range(1, self.max_iterations + 1):
            predictions = x_array @ weights + (intercept if self.fit_intercept else 0.0)
            residuals = predictions - y_array
            loss = float(
                np.mean(residuals**2) + self.l2_penalty * np.sum(weights**2)
            )
            if not np.isfinite(loss):
                raise FloatingPointError("training diverged; reduce the learning rate")
            self.loss_history_.append(loss)

            weight_gradient = (
                (2.0 / n_rows) * (x_array.T @ residuals)
                + 2.0 * self.l2_penalty * weights
            )
            intercept_gradient = (
                float(2.0 * residuals.mean()) if self.fit_intercept else 0.0
            )
            weights -= self.learning_rate * weight_gradient
            intercept -= self.learning_rate * intercept_gradient

            if previous_loss is not None and abs(previous_loss - loss) <= self.tolerance:
                self.n_iterations_ = iteration
                break
            previous_loss = loss
        else:
            self.n_iterations_ = self.max_iterations

        self.coefficients_ = weights
        self.intercept_ = float(intercept if self.fit_intercept else 0.0)
        return self

    def predict(self, X: object) -> np.ndarray:
        if self.coefficients_ is None or self.intercept_ is None:
            raise RuntimeError("model must be fit before prediction")
        x_array = _as_2d_float_array(X)
        if x_array.shape[1] != self.coefficients_.shape[0]:
            raise ValueError("X has a different feature count than training data")
        return x_array @ self.coefficients_ + self.intercept_


def make_linear_regression_data(
    row_count: int = 200,
    *,
    feature_count: int = 3,
    noise_standard_deviation: float = 0.2,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Create deterministic synthetic linear-regression data."""

    if row_count <= 0:
        raise ValueError("row_count must be positive")
    if feature_count <= 0:
        raise ValueError("feature_count must be positive")
    if noise_standard_deviation < 0:
        raise ValueError("noise_standard_deviation must be non-negative")
    rng = np.random.default_rng(random_state)
    X = rng.normal(size=(row_count, feature_count))
    true_coefficients = np.arange(1, feature_count + 1, dtype=float)
    true_intercept = 2.5
    noise = rng.normal(scale=noise_standard_deviation, size=row_count)
    y = X @ true_coefficients + true_intercept + noise
    return X, y, true_coefficients, true_intercept


if __name__ == "__main__":
    X_demo, y_demo, _, _ = make_linear_regression_data()
    model = NormalEquationRegressor().fit(X_demo, y_demo)
    print("intercept:", model.intercept_)
    print("coefficients:", model.coefficients_)
