"""Bayesian inference helpers and a pure-Python Gaussian Naive Bayes model."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
import math


Number = int | float


def _validate_probability(value: Number, *, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return result


def binary_bayes_update(
    prior: Number,
    likelihood_if_true: Number,
    likelihood_if_false: Number,
) -> float:
    """Return P(H|D) from a binary prior and two likelihoods."""

    prior_probability = _validate_probability(prior, name="prior")
    true_likelihood = _validate_probability(likelihood_if_true, name="likelihood_if_true")
    false_likelihood = _validate_probability(likelihood_if_false, name="likelihood_if_false")
    evidence = true_likelihood * prior_probability + false_likelihood * (1.0 - prior_probability)
    if evidence == 0.0:
        raise ValueError("evidence is zero; posterior is undefined")
    return true_likelihood * prior_probability / evidence


def logsumexp(values: Iterable[Number]) -> float:
    data = [float(value) for value in values]
    if not data:
        raise ValueError("values must not be empty")
    if any(math.isnan(value) for value in data):
        raise ValueError("values must not contain NaN")
    maximum = max(data)
    if maximum == -math.inf:
        return -math.inf
    if maximum == math.inf:
        return math.inf
    return maximum + math.log(math.fsum(math.exp(value - maximum) for value in data))


def _validate_matrix(features: Sequence[Sequence[Number]]) -> list[list[float]]:
    rows = [[float(value) for value in row] for row in features]
    if not rows:
        raise ValueError("features must contain at least one row")
    width = len(rows[0])
    if width == 0:
        raise ValueError("feature rows must not be empty")
    if any(len(row) != width for row in rows):
        raise ValueError("all feature rows must have equal length")
    if not all(math.isfinite(value) for row in rows for value in row):
        raise ValueError("features must contain only finite values")
    return rows


class GaussianNaiveBayes:
    """Gaussian Naive Bayes classifier with log-space posterior calculations.

    The class stores one mean and variance per class and feature. Variance
    smoothing is scaled by the largest global feature variance, following the
    spirit of common production implementations while keeping the code small.
    """

    def __init__(self, *, var_smoothing: float = 1e-9, class_priors: dict[object, float] | None = None) -> None:
        smoothing = float(var_smoothing)
        if not math.isfinite(smoothing) or smoothing <= 0.0:
            raise ValueError("var_smoothing must be positive and finite")
        self.var_smoothing = smoothing
        self.class_priors = dict(class_priors) if class_priors is not None else None
        self.classes_: tuple[object, ...] = ()
        self.class_prior_: dict[object, float] = {}
        self.means_: dict[object, tuple[float, ...]] = {}
        self.variances_: dict[object, tuple[float, ...]] = {}
        self.n_features_: int | None = None
        self._is_fitted = False

    def fit(self, features: Sequence[Sequence[Number]], labels: Sequence[object]) -> "GaussianNaiveBayes":
        rows = _validate_matrix(features)
        y = list(labels)
        if len(rows) != len(y):
            raise ValueError("features and labels must have equal length")
        if any(label is None for label in y):
            raise ValueError("labels must not contain None")

        classes = tuple(sorted(set(y), key=repr))
        if len(classes) < 2:
            raise ValueError("at least two classes are required")

        width = len(rows[0])
        global_variances = []
        for column in range(width):
            values = [row[column] for row in rows]
            center = math.fsum(values) / len(values)
            global_variances.append(math.fsum((value - center) ** 2 for value in values) / len(values))
        epsilon = self.var_smoothing * max(max(global_variances), 1.0)

        counts = Counter(y)
        priors = self._resolve_priors(classes, counts, len(y))
        means: dict[object, tuple[float, ...]] = {}
        variances: dict[object, tuple[float, ...]] = {}

        for label in classes:
            class_rows = [row for row, target in zip(rows, y, strict=True) if target == label]
            class_means: list[float] = []
            class_variances: list[float] = []
            for column in range(width):
                values = [row[column] for row in class_rows]
                center = math.fsum(values) / len(values)
                variance = math.fsum((value - center) ** 2 for value in values) / len(values)
                class_means.append(center)
                class_variances.append(variance + epsilon)
            means[label] = tuple(class_means)
            variances[label] = tuple(class_variances)

        self.classes_ = classes
        self.class_prior_ = priors
        self.means_ = means
        self.variances_ = variances
        self.n_features_ = width
        self._is_fitted = True
        return self

    def _resolve_priors(
        self,
        classes: tuple[object, ...],
        counts: Counter[object],
        total: int,
    ) -> dict[object, float]:
        if self.class_priors is None:
            return {label: counts[label] / total for label in classes}
        if set(self.class_priors) != set(classes):
            raise ValueError("class_priors keys must match observed classes")
        priors = {
            label: _validate_probability(self.class_priors[label], name=f"prior[{label!r}]")
            for label in classes
        }
        if any(value == 0.0 for value in priors.values()):
            raise ValueError("class priors must be strictly positive")
        if not math.isclose(math.fsum(priors.values()), 1.0, rel_tol=1e-9, abs_tol=1e-12):
            raise ValueError("class priors must sum to one")
        return priors

    def _joint_log_likelihood(self, row: Sequence[Number]) -> list[float]:
        self._require_fitted()
        values = [float(value) for value in row]
        if len(values) != self.n_features_:
            raise ValueError(f"expected {self.n_features_} features, received {len(values)}")
        if not all(math.isfinite(value) for value in values):
            raise ValueError("features must contain only finite values")

        scores: list[float] = []
        for label in self.classes_:
            score = math.log(self.class_prior_[label])
            for value, mean, variance in zip(
                values,
                self.means_[label],
                self.variances_[label],
                strict=True,
            ):
                score += -0.5 * (math.log(2.0 * math.pi * variance) + ((value - mean) ** 2) / variance)
            scores.append(score)
        return scores

    def predict_log_proba(self, features: Sequence[Sequence[Number]]) -> list[list[float]]:
        rows = _validate_matrix(features)
        results: list[list[float]] = []
        for row in rows:
            scores = self._joint_log_likelihood(row)
            normalizer = logsumexp(scores)
            results.append([score - normalizer for score in scores])
        return results

    def predict_proba(self, features: Sequence[Sequence[Number]]) -> list[list[float]]:
        return [[math.exp(value) for value in row] for row in self.predict_log_proba(features)]

    def predict(self, features: Sequence[Sequence[Number]]) -> list[object]:
        log_probabilities = self.predict_log_proba(features)
        return [
            self.classes_[max(range(len(row)), key=row.__getitem__)]
            for row in log_probabilities
        ]

    def score(self, features: Sequence[Sequence[Number]], labels: Sequence[object]) -> float:
        expected = list(labels)
        predicted = self.predict(features)
        if len(predicted) != len(expected):
            raise ValueError("features and labels must have equal length")
        if not expected:
            raise ValueError("labels must not be empty")
        return sum(a == b for a, b in zip(predicted, expected, strict=True)) / len(expected)

    def _require_fitted(self) -> None:
        if not self._is_fitted:
            raise RuntimeError("fit must be called before prediction")


if __name__ == "__main__":
    posterior = binary_bayes_update(prior=0.01, likelihood_if_true=0.95, likelihood_if_false=0.05)
    print(f"posterior_after_positive_test={posterior:.4f}")

    model = GaussianNaiveBayes().fit(
        [[1.0, 1.2], [0.8, 0.9], [3.0, 3.1], [3.2, 2.9]],
        [0, 0, 1, 1],
    )
    print(model.predict([[1.1, 1.0], [3.1, 3.0]]))
    print(model.predict_proba([[2.0, 2.0]]))
