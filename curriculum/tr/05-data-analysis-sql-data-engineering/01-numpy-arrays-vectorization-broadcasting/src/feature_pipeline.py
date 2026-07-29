"""Leakage-safe numeric feature preprocessing implemented with NumPy."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class PipelineState:
    feature_count: int
    imputation_values: FloatArray
    clip_lower: FloatArray
    clip_upper: FloatArray
    means: FloatArray
    scales: FloatArray
    constant_features: tuple[int, ...]


class NumericFeaturePipeline:
    """Median imputation, optional quantile clipping, and standardization."""

    def __init__(
        self,
        *,
        clip_quantiles: tuple[float, float] | None = (0.01, 0.99),
        variance_epsilon: float = 1e-12,
    ) -> None:
        if clip_quantiles is not None:
            lower, upper = clip_quantiles
            if not 0.0 <= lower < upper <= 1.0:
                raise ValueError("clip_quantiles must satisfy 0 <= lower < upper <= 1")
        if variance_epsilon <= 0.0 or not np.isfinite(variance_epsilon):
            raise ValueError("variance_epsilon must be positive and finite")

        self.clip_quantiles = clip_quantiles
        self.variance_epsilon = float(variance_epsilon)
        self._state: PipelineState | None = None

    @property
    def is_fitted(self) -> bool:
        return self._state is not None

    @property
    def state(self) -> PipelineState:
        if self._state is None:
            raise RuntimeError("pipeline has not been fitted")
        return self._state

    @staticmethod
    def _validate_input(values: ArrayLike) -> FloatArray:
        array = np.asarray(values, dtype=np.float64)
        if array.ndim != 2:
            raise ValueError("expected a 2-D feature matrix")
        if array.shape[0] == 0 or array.shape[1] == 0:
            raise ValueError("feature matrix must not be empty")
        if np.isinf(array).any():
            raise ValueError("infinite values are not supported")
        return array

    def fit(self, values: ArrayLike) -> "NumericFeaturePipeline":
        """Learn preprocessing state from training data only."""

        array = self._validate_input(values)
        all_missing = np.isnan(array).all(axis=0)
        if np.any(all_missing):
            indices = np.flatnonzero(all_missing).tolist()
            raise ValueError(f"all values are missing in features {indices}")

        imputation_values = np.nanmedian(array, axis=0)
        imputed = np.where(np.isnan(array), imputation_values, array)

        if self.clip_quantiles is None:
            clip_lower = np.full(array.shape[1], -np.inf, dtype=np.float64)
            clip_upper = np.full(array.shape[1], np.inf, dtype=np.float64)
        else:
            lower_q, upper_q = self.clip_quantiles
            clip_lower = np.quantile(imputed, lower_q, axis=0)
            clip_upper = np.quantile(imputed, upper_q, axis=0)

        clipped = np.clip(imputed, clip_lower, clip_upper)
        means = np.mean(clipped, axis=0)
        scales = np.std(clipped, axis=0)
        constant_mask = scales <= self.variance_epsilon
        safe_scales = np.where(constant_mask, 1.0, scales)

        self._state = PipelineState(
            feature_count=array.shape[1],
            imputation_values=imputation_values.copy(),
            clip_lower=clip_lower.copy(),
            clip_upper=clip_upper.copy(),
            means=means.copy(),
            scales=safe_scales.copy(),
            constant_features=tuple(np.flatnonzero(constant_mask).tolist()),
        )
        return self

    def transform(self, values: ArrayLike) -> FloatArray:
        """Apply previously learned training statistics."""

        array = self._validate_input(values)
        state = self.state
        if array.shape[1] != state.feature_count:
            raise ValueError(
                f"expected {state.feature_count} features, got {array.shape[1]}"
            )

        imputed = np.where(np.isnan(array), state.imputation_values, array)
        clipped = np.clip(imputed, state.clip_lower, state.clip_upper)
        transformed = (clipped - state.means) / state.scales
        return transformed.astype(np.float64, copy=False)

    def fit_transform(self, values: ArrayLike) -> FloatArray:
        """Fit on training data and transform the same matrix."""

        return self.fit(values).transform(values)

    def inverse_transform(self, values: ArrayLike) -> FloatArray:
        """Undo standardization; clipping and imputation are not reversible."""

        array = self._validate_input(values)
        state = self.state
        if array.shape[1] != state.feature_count:
            raise ValueError(
                f"expected {state.feature_count} features, got {array.shape[1]}"
            )
        return array * state.scales + state.means


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    training = rng.normal(size=(100, 4))
    training[0, 1] = np.nan
    pipeline = NumericFeaturePipeline()
    prepared = pipeline.fit_transform(training)
    print(pipeline.state)
    print(np.mean(prepared, axis=0))
