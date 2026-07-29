"""Model construction, calibration, evaluation, and threshold tools for SVM."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
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
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC, SVC


@dataclass(frozen=True)
class ClassificationReport:
    roc_auc: float
    average_precision: float
    f1: float
    precision: float
    recall: float
    balanced_accuracy: float
    brier: float | None = None
    log_loss_value: float | None = None


@dataclass(frozen=True)
class ThresholdResult:
    threshold: float
    cost: float
    false_positives: int
    false_negatives: int


def build_linear_svm(
    *,
    c: float = 1.0,
    class_weight: str | dict[int, float] | None = None,
    random_state: int = 42,
    max_iter: int = 10_000,
) -> LinearSVC:
    """Build a validated linear SVM classifier."""
    if c <= 0:
        raise ValueError("c must be positive")
    if max_iter < 1:
        raise ValueError("max_iter must be positive")
    return LinearSVC(
        C=c,
        class_weight=class_weight,
        dual="auto",
        random_state=random_state,
        max_iter=max_iter,
    )


def build_kernel_svm(
    *,
    c: float = 1.0,
    kernel: str = "rbf",
    gamma: str | float = "scale",
    degree: int = 3,
    coef0: float = 0.0,
    class_weight: str | dict[int, float] | None = None,
    probability: bool = False,
    decision_function_shape: str = "ovr",
    random_state: int = 42,
    cache_size: float = 512.0,
) -> SVC:
    """Build a validated kernel SVM classifier."""
    if c <= 0:
        raise ValueError("c must be positive")
    if kernel not in {"linear", "poly", "rbf", "sigmoid", "precomputed"}:
        raise ValueError("unsupported kernel")
    if isinstance(gamma, (int, float)) and gamma <= 0:
        raise ValueError("numeric gamma must be positive")
    if degree < 1:
        raise ValueError("degree must be at least 1")
    if decision_function_shape not in {"ovo", "ovr"}:
        raise ValueError("decision_function_shape must be 'ovo' or 'ovr'")
    if cache_size <= 0:
        raise ValueError("cache_size must be positive")
    return SVC(
        C=c,
        kernel=kernel,
        gamma=gamma,
        degree=degree,
        coef0=coef0,
        class_weight=class_weight,
        probability=probability,
        decision_function_shape=decision_function_shape,
        random_state=random_state,
        cache_size=cache_size,
    )


def build_ovr_linear_svm(
    *,
    c: float = 1.0,
    class_weight: str | dict[int, float] | None = None,
    random_state: int = 42,
) -> OneVsRestClassifier:
    """Build an explicit one-vs-rest multiclass linear SVM."""
    estimator = build_linear_svm(
        c=c,
        class_weight=class_weight,
        random_state=random_state,
    )
    return OneVsRestClassifier(estimator)


def support_vector_fraction(model: SVC, n_samples: int) -> float:
    """Return the fraction of fitted training rows selected as support vectors."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    if not hasattr(model, "support_"):
        raise ValueError("model must be fitted")
    return float(len(model.support_) / n_samples)


def support_vector_summary(model: SVC) -> dict[str, object]:
    """Return support-vector counts and dual coefficient metadata."""
    if not hasattr(model, "support_"):
        raise ValueError("model must be fitted")
    return {
        "total": int(len(model.support_)),
        "per_class": np.asarray(model.n_support_, dtype=int).tolist(),
        "dual_coefficient_shape": tuple(model.dual_coef_.shape),
        "support_indices": np.asarray(model.support_, dtype=int).copy(),
    }


def calibrate_svm(
    estimator: BaseEstimator,
    *,
    method: str = "sigmoid",
    cv: int = 5,
    n_jobs: int | None = None,
) -> CalibratedClassifierCV:
    """Wrap an estimator in cross-validated probability calibration."""
    if method not in {"sigmoid", "isotonic"}:
        raise ValueError("method must be 'sigmoid' or 'isotonic'")
    if cv < 2:
        raise ValueError("cv must be at least 2")
    return CalibratedClassifierCV(
        estimator=estimator,
        method=method,
        cv=cv,
        n_jobs=n_jobs,
    )


def evaluate_classifier(
    y_true: ArrayLike,
    *,
    scores: ArrayLike,
    predictions: ArrayLike,
    probabilities: ArrayLike | None = None,
) -> ClassificationReport:
    """Evaluate ranking, threshold, and optional probability quality."""
    labels = np.asarray(y_true).reshape(-1)
    score_arr = np.asarray(scores, dtype=float).reshape(-1)
    prediction_arr = np.asarray(predictions).reshape(-1)
    if not (len(labels) == len(score_arr) == len(prediction_arr)):
        raise ValueError("all arrays must have equal length")
    if np.unique(labels).size != 2:
        raise ValueError("evaluate_classifier expects a binary target")

    brier = None
    log_value = None
    if probabilities is not None:
        probability_arr = np.asarray(probabilities, dtype=float).reshape(-1)
        if len(probability_arr) != len(labels):
            raise ValueError("probabilities must have equal length")
        if np.any((probability_arr < 0.0) | (probability_arr > 1.0)):
            raise ValueError("probabilities must lie in [0, 1]")
        brier = float(brier_score_loss(labels, probability_arr))
        log_value = float(
            log_loss(labels, np.column_stack([1.0 - probability_arr, probability_arr]))
        )

    return ClassificationReport(
        roc_auc=float(roc_auc_score(labels, score_arr)),
        average_precision=float(average_precision_score(labels, score_arr)),
        f1=float(f1_score(labels, prediction_arr, zero_division=0)),
        precision=float(precision_score(labels, prediction_arr, zero_division=0)),
        recall=float(recall_score(labels, prediction_arr, zero_division=0)),
        balanced_accuracy=float(balanced_accuracy_score(labels, prediction_arr)),
        brier=brier,
        log_loss_value=log_value,
    )


def predict_with_threshold(
    probabilities: ArrayLike,
    threshold: float = 0.5,
) -> NDArray[np.int64]:
    """Convert positive-class probabilities to binary predictions."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must lie in [0, 1]")
    probability_arr = np.asarray(probabilities, dtype=float).reshape(-1)
    if np.any((probability_arr < 0.0) | (probability_arr > 1.0)):
        raise ValueError("probabilities must lie in [0, 1]")
    return (probability_arr >= threshold).astype(np.int64)


def classification_cost(
    y_true: ArrayLike,
    predictions: ArrayLike,
    *,
    false_positive_cost: float,
    false_negative_cost: float,
) -> tuple[float, int, int]:
    """Return total binary decision cost and error counts."""
    if false_positive_cost < 0 or false_negative_cost < 0:
        raise ValueError("costs must be non-negative")
    labels = np.asarray(y_true).reshape(-1)
    prediction_arr = np.asarray(predictions).reshape(-1)
    if labels.shape != prediction_arr.shape:
        raise ValueError("y_true and predictions must have equal length")
    if not np.all(np.isin(labels, (0, 1))) or not np.all(
        np.isin(prediction_arr, (0, 1))
    ):
        raise ValueError("y_true and predictions must contain only 0 and 1")
    false_positives = int(np.sum((labels == 0) & (prediction_arr == 1)))
    false_negatives = int(np.sum((labels == 1) & (prediction_arr == 0)))
    cost = (
        false_positive_cost * false_positives
        + false_negative_cost * false_negatives
    )
    return float(cost), false_positives, false_negatives


def select_cost_sensitive_threshold(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    thresholds: Iterable[float] | None = None,
    false_positive_cost: float = 25.0,
    false_negative_cost: float = 400.0,
) -> ThresholdResult:
    """Select the minimum-cost threshold on validation probabilities."""
    labels = np.asarray(y_true).reshape(-1)
    probability_arr = np.asarray(probabilities, dtype=float).reshape(-1)
    if labels.shape != probability_arr.shape:
        raise ValueError("y_true and probabilities must have equal length")
    candidate_thresholds = (
        np.linspace(0.0, 1.0, 101)
        if thresholds is None
        else np.asarray(list(thresholds), dtype=float)
    )
    if candidate_thresholds.size == 0:
        raise ValueError("thresholds must not be empty")
    if np.any((candidate_thresholds < 0.0) | (candidate_thresholds > 1.0)):
        raise ValueError("thresholds must lie in [0, 1]")

    best: ThresholdResult | None = None
    for threshold in candidate_thresholds:
        predictions = predict_with_threshold(probability_arr, float(threshold))
        cost, false_positives, false_negatives = classification_cost(
            labels,
            predictions,
            false_positive_cost=false_positive_cost,
            false_negative_cost=false_negative_cost,
        )
        candidate = ThresholdResult(
            threshold=float(threshold),
            cost=cost,
            false_positives=false_positives,
            false_negatives=false_negatives,
        )
        if best is None or (candidate.cost, candidate.threshold) < (
            best.cost,
            best.threshold,
        ):
            best = candidate
    if best is None:
        raise RuntimeError("threshold selection failed")
    return best
