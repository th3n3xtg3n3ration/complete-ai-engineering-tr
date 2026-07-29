"""Threshold, cost, discrimination, and calibration utilities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, NDArray
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

MetricName = Literal["f1", "balanced_accuracy", "expected_cost"]


def _binary_arrays(
    y_true: ArrayLike,
    probabilities: ArrayLike,
) -> tuple[NDArray[np.int64], NDArray[np.float64]]:
    labels = np.asarray(y_true, dtype=int).reshape(-1)
    scores = np.asarray(probabilities, dtype=float).reshape(-1)
    if labels.shape != scores.shape:
        raise ValueError("y_true and probabilities must have equal shape")
    if labels.size == 0:
        raise ValueError("at least one observation is required")
    if not np.isin(labels, [0, 1]).all():
        raise ValueError("y_true must contain only 0 and 1")
    if not np.isfinite(scores).all() or np.any((scores < 0) | (scores > 1)):
        raise ValueError("probabilities must be finite values between 0 and 1")
    return labels, scores


@dataclass(frozen=True)
class ConfusionCounts:
    """Binary confusion-matrix counts."""

    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int

    @property
    def total(self) -> int:
        return self.true_negative + self.false_positive + self.false_negative + self.true_positive


def confusion_counts(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    threshold: float = 0.5,
) -> ConfusionCounts:
    """Compute binary confusion counts from probabilities."""

    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    labels, scores = _binary_arrays(y_true, probabilities)
    predictions = scores >= threshold
    return ConfusionCounts(
        true_negative=int(np.sum((labels == 0) & ~predictions)),
        false_positive=int(np.sum((labels == 0) & predictions)),
        false_negative=int(np.sum((labels == 1) & ~predictions)),
        true_positive=int(np.sum((labels == 1) & predictions)),
    )


def expected_cost(
    counts: ConfusionCounts,
    *,
    false_positive_cost: float,
    false_negative_cost: float,
    normalize: bool = True,
) -> float:
    """Return decision cost based on false-positive and false-negative costs."""

    if false_positive_cost < 0 or false_negative_cost < 0:
        raise ValueError("costs must be non-negative")
    total = (
        counts.false_positive * false_positive_cost
        + counts.false_negative * false_negative_cost
    )
    if normalize:
        if counts.total == 0:
            raise ValueError("confusion counts must contain observations")
        return float(total / counts.total)
    return float(total)


def classification_metrics(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    threshold: float = 0.5,
) -> dict[str, float]:
    """Return probability and threshold metrics for binary classification."""

    labels, scores = _binary_arrays(y_true, probabilities)
    predictions = (scores >= threshold).astype(int)
    metrics = {
        "accuracy": float(np.mean(labels == predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "f1": float(f1_score(labels, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(labels, scores)),
        "average_precision": float(average_precision_score(labels, scores)),
        "log_loss": float(log_loss(labels, scores, labels=[0, 1])),
        "brier_score": float(brier_score_loss(labels, scores)),
        "positive_rate": float(np.mean(predictions)),
        "threshold": float(threshold),
    }
    return metrics


def threshold_table(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    thresholds: ArrayLike | None = None,
    false_positive_cost: float = 1.0,
    false_negative_cost: float = 1.0,
) -> pd.DataFrame:
    """Evaluate threshold-dependent metrics across candidate thresholds."""

    labels, scores = _binary_arrays(y_true, probabilities)
    candidates = (
        np.linspace(0.0, 1.0, 101)
        if thresholds is None
        else np.asarray(thresholds, dtype=float).reshape(-1)
    )
    if candidates.size == 0 or np.any((candidates < 0) | (candidates > 1)):
        raise ValueError("thresholds must contain values between 0 and 1")
    rows: list[dict[str, float | int]] = []
    for threshold in np.unique(candidates):
        metrics = classification_metrics(labels, scores, threshold=float(threshold))
        counts = confusion_counts(labels, scores, threshold=float(threshold))
        rows.append(
            {
                "threshold": float(threshold),
                **asdict(counts),
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
                "balanced_accuracy": metrics["balanced_accuracy"],
                "expected_cost": expected_cost(
                    counts,
                    false_positive_cost=false_positive_cost,
                    false_negative_cost=false_negative_cost,
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("threshold").reset_index(drop=True)


def select_threshold(
    table: pd.DataFrame,
    *,
    metric: MetricName,
    minimum_recall: float | None = None,
    minimum_precision: float | None = None,
) -> float:
    """Select the best threshold under optional precision/recall constraints."""

    required = {"threshold", metric, "precision", "recall"}
    missing = required.difference(table.columns)
    if missing:
        raise ValueError(f"threshold table is missing columns: {sorted(missing)}")
    candidates = table.copy()
    if minimum_recall is not None:
        if not 0.0 <= minimum_recall <= 1.0:
            raise ValueError("minimum_recall must be between 0 and 1")
        candidates = candidates[candidates["recall"] >= minimum_recall]
    if minimum_precision is not None:
        if not 0.0 <= minimum_precision <= 1.0:
            raise ValueError("minimum_precision must be between 0 and 1")
        candidates = candidates[candidates["precision"] >= minimum_precision]
    if candidates.empty:
        raise ValueError("no threshold satisfies the requested constraints")
    ascending = metric == "expected_cost"
    ordered = candidates.sort_values(
        [metric, "threshold"],
        ascending=[ascending, True],
    )
    return float(ordered.iloc[0]["threshold"])


def calibration_table(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Return equal-width reliability bins, including empty-bin omission."""

    if n_bins < 2:
        raise ValueError("n_bins must be at least 2")
    labels, scores = _binary_arrays(y_true, probabilities)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_ids = np.minimum(np.digitize(scores, edges[1:-1], right=False), n_bins - 1)
    rows: list[dict[str, float | int]] = []
    for bin_id in range(n_bins):
        mask = bin_ids == bin_id
        if not np.any(mask):
            continue
        rows.append(
            {
                "bin": bin_id,
                "lower": float(edges[bin_id]),
                "upper": float(edges[bin_id + 1]),
                "count": int(mask.sum()),
                "mean_probability": float(scores[mask].mean()),
                "event_rate": float(labels[mask].mean()),
                "absolute_gap": float(abs(scores[mask].mean() - labels[mask].mean())),
            }
        )
    return pd.DataFrame(rows)


def expected_calibration_error(calibration: pd.DataFrame) -> float:
    """Compute weighted expected calibration error from reliability bins."""

    required = {"count", "absolute_gap"}
    if not required.issubset(calibration.columns):
        raise ValueError("calibration table must contain count and absolute_gap")
    total = float(calibration["count"].sum())
    if total <= 0:
        raise ValueError("calibration table must contain observations")
    return float((calibration["count"] * calibration["absolute_gap"]).sum() / total)
