"""SVM model helpers."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import average_precision_score, balanced_accuracy_score, brier_score_loss, f1_score, log_loss, roc_auc_score
from sklearn.svm import LinearSVC, SVC

@dataclass(frozen=True)
class ClassificationReport:
    roc_auc: float
    average_precision: float
    f1: float
    balanced_accuracy: float
    brier: float | None = None
    log_loss_value: float | None = None

def build_linear_svm(*, c: float = 1.0, class_weight=None, random_state: int = 42) -> LinearSVC:
    if c <= 0:
        raise ValueError("c must be positive")
    return LinearSVC(C=c, class_weight=class_weight, dual="auto", random_state=random_state)

def build_kernel_svm(*, c: float = 1.0, kernel: str = "rbf", gamma: str | float = "scale", degree: int = 3, coef0: float = 0.0, class_weight=None, probability: bool = False, random_state: int = 42) -> SVC:
    if c <= 0:
        raise ValueError("c must be positive")
    if kernel not in {"linear", "poly", "rbf", "sigmoid", "precomputed"}:
        raise ValueError("unsupported kernel")
    if isinstance(gamma, (int, float)) and gamma <= 0:
        raise ValueError("numeric gamma must be positive")
    if degree < 1:
        raise ValueError("degree must be at least 1")
    return SVC(C=c, kernel=kernel, gamma=gamma, degree=degree, coef0=coef0, class_weight=class_weight, probability=probability, random_state=random_state)

def support_vector_fraction(model: SVC, n_samples: int) -> float:
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    if not hasattr(model, "support_"):
        raise ValueError("model must be fitted")
    return float(len(model.support_) / n_samples)

def calibrate_svm(estimator: BaseEstimator, *, method: str = "sigmoid", cv: int = 3) -> CalibratedClassifierCV:
    if method not in {"sigmoid", "isotonic"}:
        raise ValueError("method must be 'sigmoid' or 'isotonic'")
    if cv < 2:
        raise ValueError("cv must be at least 2")
    return CalibratedClassifierCV(estimator=estimator, method=method, cv=cv)

def evaluate_classifier(y_true: ArrayLike, *, scores: ArrayLike, predictions: ArrayLike, probabilities: ArrayLike | None = None) -> ClassificationReport:
    y = np.asarray(y_true).reshape(-1)
    s = np.asarray(scores, dtype=float).reshape(-1)
    p = np.asarray(predictions).reshape(-1)
    if not (len(y) == len(s) == len(p)):
        raise ValueError("all arrays must have equal length")
    brier = log_value = None
    if probabilities is not None:
        probs = np.asarray(probabilities, dtype=float).reshape(-1)
        if len(probs) != len(y):
            raise ValueError("probabilities must have equal length")
        if np.any((probs < 0.0) | (probs > 1.0)):
            raise ValueError("probabilities must lie in [0, 1]")
        brier = float(brier_score_loss(y, probs))
        log_value = float(log_loss(y, np.column_stack([1.0 - probs, probs])))
    return ClassificationReport(float(roc_auc_score(y, s)), float(average_precision_score(y, s)), float(f1_score(y, p, zero_division=0)), float(balanced_accuracy_score(y, p)), brier, log_value)

def predict_with_threshold(probabilities: ArrayLike, threshold: float = 0.5) -> NDArray[np.int64]:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must lie in [0, 1]")
    probs = np.asarray(probabilities, dtype=float).reshape(-1)
    if np.any((probs < 0.0) | (probs > 1.0)):
        raise ValueError("probabilities must lie in [0, 1]")
    return (probs >= threshold).astype(np.int64)
