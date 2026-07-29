"""Regression metrics, residual diagnostics, VIF, and slice analysis."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def _paired_arrays(
    y_true: object,
    y_prediction: object,
) -> tuple[np.ndarray, np.ndarray]:
    actual = np.asarray(y_true, dtype=float).reshape(-1)
    predicted = np.asarray(y_prediction, dtype=float).reshape(-1)
    if actual.size == 0:
        raise ValueError("targets must not be empty")
    if actual.shape != predicted.shape:
        raise ValueError("targets and predictions must have identical shape")
    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("targets and predictions must be finite")
    return actual, predicted


@dataclass(frozen=True)
class RegressionMetrics:
    """Common regression evaluation metrics."""

    mae: float
    mse: float
    rmse: float
    r2: float
    adjusted_r2: float | None

    def to_dict(self) -> dict[str, float | None]:
        return asdict(self)


def regression_metrics(
    y_true: object,
    y_prediction: object,
    *,
    feature_count: int | None = None,
) -> RegressionMetrics:
    actual, predicted = _paired_arrays(y_true, y_prediction)
    if feature_count is not None and feature_count < 0:
        raise ValueError("feature_count must be non-negative")
    mae = float(mean_absolute_error(actual, predicted))
    mse = float(mean_squared_error(actual, predicted))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(actual, predicted))
    adjusted: float | None = None
    if feature_count is not None:
        denominator = actual.size - feature_count - 1
        if denominator > 0:
            adjusted = float(1.0 - (1.0 - r2) * (actual.size - 1) / denominator)
    return RegressionMetrics(mae, mse, rmse, r2, adjusted)


@dataclass(frozen=True)
class ResidualSummary:
    """Compact residual distribution summary."""

    mean: float
    standard_deviation: float
    median: float
    mean_absolute_residual: float
    underprediction_rate: float
    overprediction_rate: float
    maximum_absolute_residual: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def residual_summary(y_true: object, y_prediction: object) -> ResidualSummary:
    actual, predicted = _paired_arrays(y_true, y_prediction)
    residuals = actual - predicted
    return ResidualSummary(
        mean=float(residuals.mean()),
        standard_deviation=float(residuals.std(ddof=0)),
        median=float(np.median(residuals)),
        mean_absolute_residual=float(np.abs(residuals).mean()),
        underprediction_rate=float(np.mean(residuals > 0)),
        overprediction_rate=float(np.mean(residuals < 0)),
        maximum_absolute_residual=float(np.abs(residuals).max()),
    )


def heteroskedasticity_signal(
    y_prediction: object,
    residuals: object,
) -> float:
    """Return correlation between fitted values and absolute residuals."""

    fitted, residual_array = _paired_arrays(y_prediction, residuals)
    absolute_residuals = np.abs(residual_array)
    if np.std(fitted) == 0 or np.std(absolute_residuals) == 0:
        return 0.0
    return float(np.corrcoef(fitted, absolute_residuals)[0, 1])


def variance_inflation_factors(
    frame: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Compute VIF values for finite numeric columns."""

    selected = list(columns)
    if len(selected) < 2:
        raise ValueError("at least two columns are required")
    missing = sorted(set(selected) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    data = frame[selected].apply(pd.to_numeric, errors="coerce")
    if data.isna().any().any() or not np.isfinite(data.to_numpy(dtype=float)).all():
        raise ValueError("VIF columns must contain finite numeric values")

    rows: list[dict[str, float | str]] = []
    for column in selected:
        target = data[column].to_numpy(dtype=float)
        predictors = data.drop(columns=column).to_numpy(dtype=float)
        score = LinearRegression().fit(predictors, target).score(predictors, target)
        vif = float("inf") if score >= 1.0 - 1e-12 else float(1.0 / (1.0 - score))
        rows.append({"feature": column, "vif": vif})
    return pd.DataFrame(rows).sort_values("vif", ascending=False).reset_index(drop=True)


def slice_regression_metrics(
    frame: pd.DataFrame,
    *,
    actual_column: str,
    prediction_column: str,
    slice_columns: Sequence[str],
) -> pd.DataFrame:
    """Compute MAE, RMSE, and signed bias for configured slices."""

    required = [actual_column, prediction_column, *slice_columns]
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if not slice_columns:
        raise ValueError("slice_columns must not be empty")

    rows: list[dict[str, object]] = []
    grouped = frame.groupby(list(slice_columns), dropna=False, observed=True)
    for key, subset in grouped:
        keys = key if isinstance(key, tuple) else (key,)
        actual, predicted = _paired_arrays(
            subset[actual_column],
            subset[prediction_column],
        )
        row = dict(zip(slice_columns, keys, strict=True))
        row.update(
            {
                "row_count": int(len(subset)),
                "mae": float(mean_absolute_error(actual, predicted)),
                "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
                "signed_bias": float(np.mean(predicted - actual)),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(
        ["mae", *slice_columns],
        ascending=[False, *([True] * len(slice_columns))],
    ).reset_index(drop=True)


def worst_residual_rows(
    frame: pd.DataFrame,
    *,
    actual_column: str,
    prediction_column: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return rows with the largest absolute residuals."""

    if top_n <= 0:
        raise ValueError("top_n must be positive")
    missing = sorted({actual_column, prediction_column} - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    result = frame.copy()
    result["residual"] = result[actual_column] - result[prediction_column]
    result["absolute_residual"] = result["residual"].abs()
    return result.sort_values(
        ["absolute_residual"],
        ascending=False,
        kind="stable",
    ).head(top_n).reset_index(drop=True)


if __name__ == "__main__":
    print(regression_metrics([1, 2, 3], [1.1, 1.9, 3.2], feature_count=1))
