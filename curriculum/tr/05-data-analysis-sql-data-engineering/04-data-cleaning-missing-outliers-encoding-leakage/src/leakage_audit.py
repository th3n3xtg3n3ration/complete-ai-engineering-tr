"""Audits for common target, temporal, and entity leakage patterns."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd

from data_quality import require_columns


@dataclass(frozen=True)
class LeakageFinding:
    """Explainable leakage warning."""

    column: str
    severity: str
    reason: str


_SUSPICIOUS_TOKENS = (
    "target",
    "label",
    "outcome",
    "future",
    "after_",
    "post_",
    "prediction",
    "predicted",
)


def audit_feature_target_leakage(
    frame: pd.DataFrame,
    *,
    target_column: str,
    feature_columns: Sequence[str] | None = None,
    correlation_threshold: float = 0.999,
) -> list[LeakageFinding]:
    """Detect obvious target proxies and suspicious post-outcome features."""

    require_columns(frame, [target_column])
    if not 0.0 < correlation_threshold <= 1.0:
        raise ValueError("correlation_threshold must be in (0, 1]")
    features = list(feature_columns or [c for c in frame.columns if c != target_column])
    require_columns(frame, features)

    target = frame[target_column]
    findings: list[LeakageFinding] = []
    for column in features:
        lowered = column.lower()
        if any(token in lowered for token in _SUSPICIOUS_TOKENS):
            findings.append(
                LeakageFinding(
                    column=column,
                    severity="warning",
                    reason="column name suggests target or post-outcome information",
                )
            )

        feature = frame[column]
        comparable = pd.DataFrame({"feature": feature, "target": target}).dropna()
        if comparable.empty:
            continue
        if comparable["feature"].astype("string").equals(
            comparable["target"].astype("string")
        ):
            findings.append(
                LeakageFinding(
                    column=column,
                    severity="critical",
                    reason="feature is identical to the target on comparable rows",
                )
            )
            continue

        numeric_feature = pd.to_numeric(comparable["feature"], errors="coerce")
        numeric_target = pd.to_numeric(comparable["target"], errors="coerce")
        numeric = pd.DataFrame(
            {"feature": numeric_feature, "target": numeric_target}
        ).dropna()
        if (
            len(numeric) >= 3
            and numeric["feature"].nunique() > 1
            and numeric["target"].nunique() > 1
        ):
            correlation = float(numeric["feature"].corr(numeric["target"]))
            if np.isfinite(correlation) and abs(correlation) >= correlation_threshold:
                findings.append(
                    LeakageFinding(
                        column=column,
                        severity="critical",
                        reason=f"absolute target correlation is {abs(correlation):.6f}",
                    )
                )
    return findings


def temporal_split(
    frame: pd.DataFrame,
    *,
    time_column: str,
    cutoff: str | pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data so training rows strictly precede the cutoff."""

    require_columns(frame, [time_column])
    timestamps = pd.to_datetime(
        frame[time_column], errors="coerce", utc=True, format="mixed"
    )
    if timestamps.isna().any():
        raise ValueError(f"{time_column} contains invalid timestamps")
    boundary = pd.Timestamp(cutoff)
    if boundary.tzinfo is None:
        boundary = boundary.tz_localize("UTC")
    else:
        boundary = boundary.tz_convert("UTC")
    train = frame.loc[timestamps < boundary].copy()
    evaluation = frame.loc[timestamps >= boundary].copy()
    if train.empty or evaluation.empty:
        raise ValueError("temporal split must create non-empty train and evaluation sets")
    return train, evaluation


def overlapping_keys(
    train: pd.DataFrame,
    evaluation: pd.DataFrame,
    *,
    key_columns: Sequence[str],
) -> pd.DataFrame:
    """Return entity keys appearing in both train and evaluation sets."""

    if not key_columns:
        raise ValueError("key_columns must not be empty")
    require_columns(train, key_columns)
    require_columns(evaluation, key_columns)
    left = train.loc[:, key_columns].drop_duplicates()
    right = evaluation.loc[:, key_columns].drop_duplicates()
    return (
        left.merge(right, on=list(key_columns), how="inner", validate="one_to_one")
        .sort_values(list(key_columns), kind="mergesort")
        .reset_index(drop=True)
    )


def assert_no_row_overlap(
    train: pd.DataFrame,
    evaluation: pd.DataFrame,
    *,
    row_id_column: str,
) -> None:
    """Raise when an exact row identifier appears in both splits."""

    overlap = overlapping_keys(
        train,
        evaluation,
        key_columns=[row_id_column],
    )
    if not overlap.empty:
        raise ValueError(
            f"train and evaluation overlap on {row_id_column}: "
            f"{overlap[row_id_column].tolist()}"
        )
