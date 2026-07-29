"""Data-quality utilities for tabular preprocessing workflows."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FrameQualityProfile:
    """Compact quality summary for a pandas DataFrame."""

    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    memory_bytes: int


def require_columns(frame: pd.DataFrame, required: Iterable[str]) -> None:
    """Raise a clear error when required columns are absent."""

    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def profile_frame(frame: pd.DataFrame) -> FrameQualityProfile:
    """Return row, missing-value, duplicate, and memory diagnostics."""

    return FrameQualityProfile(
        rows=len(frame),
        columns=len(frame.columns),
        missing_cells=int(frame.isna().sum().sum()),
        duplicate_rows=int(frame.duplicated().sum()),
        memory_bytes=int(frame.memory_usage(index=True, deep=True).sum()),
    )


def missingness_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a deterministic column-level missingness report."""

    rows = max(len(frame), 1)
    report = pd.DataFrame(
        {
            "column": frame.columns,
            "missing_count": [int(frame[column].isna().sum()) for column in frame.columns],
        }
    )
    report["missing_rate"] = report["missing_count"] / rows
    return report.sort_values(
        ["missing_rate", "column"],
        ascending=[False, True],
        kind="mergesort",
    ).reset_index(drop=True)


def duplicate_key_report(frame: pd.DataFrame, key_columns: Sequence[str]) -> pd.DataFrame:
    """Return duplicated business keys with their occurrence counts."""

    if not key_columns:
        raise ValueError("key_columns must not be empty")
    require_columns(frame, key_columns)
    counts = (
        frame.groupby(list(key_columns), dropna=False, sort=True)
        .size()
        .rename("row_count")
        .reset_index()
    )
    return counts.loc[counts["row_count"] > 1].reset_index(drop=True)


def iqr_bounds(series: pd.Series, *, multiplier: float = 1.5) -> tuple[float, float]:
    """Calculate finite IQR bounds for a numeric series."""

    if multiplier <= 0 or not np.isfinite(multiplier):
        raise ValueError("multiplier must be positive and finite")
    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if numeric.empty:
        raise ValueError("series must contain at least one finite numeric value")
    q1 = float(numeric.quantile(0.25))
    q3 = float(numeric.quantile(0.75))
    spread = q3 - q1
    return q1 - multiplier * spread, q3 + multiplier * spread


def cap_outliers_iqr(
    frame: pd.DataFrame,
    columns: Sequence[str],
    *,
    multiplier: float = 1.5,
) -> tuple[pd.DataFrame, dict[str, tuple[float, float]]]:
    """Return a clipped copy and the learned IQR bounds."""

    require_columns(frame, columns)
    result = frame.copy(deep=True)
    bounds: dict[str, tuple[float, float]] = {}
    for column in columns:
        lower, upper = iqr_bounds(result[column], multiplier=multiplier)
        result[column] = pd.to_numeric(result[column], errors="coerce").clip(lower, upper)
        bounds[column] = (lower, upper)
    return result, bounds


def robust_z_scores(series: pd.Series) -> pd.Series:
    """Return median absolute deviation based robust z-scores."""

    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    median = float(numeric.median())
    deviations = (numeric - median).abs()
    mad = float(deviations.median())
    if not np.isfinite(mad) or mad == 0.0:
        return pd.Series(np.zeros(len(series), dtype=float), index=series.index)
    return 0.6744897501960817 * (numeric - median) / mad


def coerce_numeric_columns(
    frame: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Return a copy with selected columns coerced to nullable floats."""

    require_columns(frame, columns)
    result = frame.copy(deep=True)
    for column in columns:
        result[column] = pd.to_numeric(result[column], errors="coerce").astype("Float64")
    return result


def validate_numeric_range(
    frame: pd.DataFrame,
    column: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
    allow_missing: bool = True,
) -> None:
    """Validate numeric values against explicit business constraints."""

    require_columns(frame, [column])
    numeric = pd.to_numeric(frame[column], errors="coerce")
    if not allow_missing and numeric.isna().any():
        raise ValueError(f"{column} contains missing or non-numeric values")
    valid = numeric.dropna()
    if minimum is not None and (valid < minimum).any():
        raise ValueError(f"{column} contains values below {minimum}")
    if maximum is not None and (valid > maximum).any():
        raise ValueError(f"{column} contains values above {maximum}")
