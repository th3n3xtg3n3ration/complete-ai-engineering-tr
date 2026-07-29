"""Reproducible simulations for probability, sampling, and Bayesian classification."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Sequence

from bayes import GaussianNaiveBayes


@dataclass(frozen=True)
class ClassificationMetrics:
    accuracy: float
    log_loss: float
    confusion_matrix: tuple[tuple[int, int], tuple[int, int]]


def make_gaussian_classification_data(
    *,
    samples: int = 600,
    positive_rate: float = 0.35,
    seed: int = 42,
) -> tuple[list[list[float]], list[int]]:
    if samples < 20:
        raise ValueError("samples must be at least 20")
    if not 0.0 < positive_rate < 1.0:
        raise ValueError("positive_rate must be between zero and one")

    rng = random.Random(seed)
    features: list[list[float]] = []
    labels: list[int] = []
    for _ in range(samples):
        label = 1 if rng.random() < positive_rate else 0
        if label == 0:
            row = [rng.gauss(-1.0, 1.0), rng.gauss(0.0, 0.8), rng.gauss(0.5, 1.2)]
        else:
            row = [rng.gauss(1.2, 0.9), rng.gauss(1.0, 1.1), rng.gauss(-0.4, 0.9)]
        features.append(row)
        labels.append(label)
    return features, labels


def train_test_split(
    features: Sequence[Sequence[float]],
    labels: Sequence[int],
    *,
    test_ratio: float = 0.25,
    seed: int = 42,
) -> tuple[list[list[float]], list[list[float]], list[int], list[int]]:
    if len(features) != len(labels) or len(features) < 4:
        raise ValueError("features and labels must have equal length of at least four")
    if not 0.0 < test_ratio < 1.0:
        raise ValueError("test_ratio must be between zero and one")

    indices = list(range(len(features)))
    random.Random(seed).shuffle(indices)
    test_size = max(1, min(len(indices) - 1, round(len(indices) * test_ratio)))
    test_indices = set(indices[:test_size])

    x_train: list[list[float]] = []
    x_test: list[list[float]] = []
    y_train: list[int] = []
    y_test: list[int] = []
    for index, (row, label) in enumerate(zip(features, labels, strict=True)):
        if index in test_indices:
            x_test.append([float(value) for value in row])
            y_test.append(int(label))
        else:
            x_train.append([float(value) for value in row])
            y_train.append(int(label))
    return x_train, x_test, y_train, y_test


def binary_log_loss(labels: Sequence[int], positive_probabilities: Sequence[float], *, eps: float = 1e-15) -> float:
    if len(labels) != len(positive_probabilities) or not labels:
        raise ValueError("labels and probabilities must be non-empty and equal length")
    losses: list[float] = []
    for label, probability in zip(labels, positive_probabilities, strict=True):
        if label not in (0, 1):
            raise ValueError("labels must be binary")
        value = min(max(float(probability), eps), 1.0 - eps)
        losses.append(-(label * math.log(value) + (1 - label) * math.log(1.0 - value)))
    return math.fsum(losses) / len(losses)


def evaluate_binary_classifier(
    labels: Sequence[int],
    positive_probabilities: Sequence[float],
    *,
    threshold: float = 0.5,
) -> ClassificationMetrics:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between zero and one")
    if len(labels) != len(positive_probabilities) or not labels:
        raise ValueError("labels and probabilities must be non-empty and equal length")

    true_negative = false_positive = false_negative = true_positive = 0
    for label, probability in zip(labels, positive_probabilities, strict=True):
        prediction = int(float(probability) >= threshold)
        if label == 0 and prediction == 0:
            true_negative += 1
        elif label == 0 and prediction == 1:
            false_positive += 1
        elif label == 1 and prediction == 0:
            false_negative += 1
        elif label == 1 and prediction == 1:
            true_positive += 1
        else:
            raise ValueError("labels must be binary")

    accuracy = (true_negative + true_positive) / len(labels)
    return ClassificationMetrics(
        accuracy=accuracy,
        log_loss=binary_log_loss(labels, positive_probabilities),
        confusion_matrix=((true_negative, false_positive), (false_negative, true_positive)),
    )


def calibration_bins(
    labels: Sequence[int],
    probabilities: Sequence[float],
    *,
    bins: int = 10,
) -> list[dict[str, float | int]]:
    if bins <= 0:
        raise ValueError("bins must be positive")
    if len(labels) != len(probabilities) or not labels:
        raise ValueError("labels and probabilities must be non-empty and equal length")

    grouped: list[list[tuple[int, float]]] = [[] for _ in range(bins)]
    for label, probability in zip(labels, probabilities, strict=True):
        if label not in (0, 1):
            raise ValueError("labels must be binary")
        value = float(probability)
        if not 0.0 <= value <= 1.0:
            raise ValueError("probabilities must be between zero and one")
        index = min(int(value * bins), bins - 1)
        grouped[index].append((label, value))

    result: list[dict[str, float | int]] = []
    for index, observations in enumerate(grouped):
        if not observations:
            continue
        result.append(
            {
                "bin": index,
                "count": len(observations),
                "mean_probability": math.fsum(value for _, value in observations) / len(observations),
                "positive_rate": math.fsum(label for label, _ in observations) / len(observations),
            }
        )
    return result


def simulate_sample_means(
    *,
    sample_size: int,
    repetitions: int,
    seed: int = 42,
) -> list[float]:
    """Return means of exponential samples to illustrate the CLT."""

    if sample_size <= 0 or repetitions <= 0:
        raise ValueError("sample_size and repetitions must be positive")
    rng = random.Random(seed)
    return [
        math.fsum(rng.expovariate(1.0) for _ in range(sample_size)) / sample_size
        for _ in range(repetitions)
    ]


def run_experiment(seed: int = 42) -> ClassificationMetrics:
    features, labels = make_gaussian_classification_data(seed=seed)
    x_train, x_test, y_train, y_test = train_test_split(features, labels, seed=seed)
    model = GaussianNaiveBayes(var_smoothing=1e-9).fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)
    positive_index = model.classes_.index(1)
    positive_probabilities = [row[positive_index] for row in probabilities]
    return evaluate_binary_classifier(y_test, positive_probabilities)


if __name__ == "__main__":
    metrics = run_experiment()
    print(f"accuracy={metrics.accuracy:.4f}")
    print(f"log_loss={metrics.log_loss:.4f}")
    print(f"confusion_matrix={metrics.confusion_matrix}")

    means = simulate_sample_means(sample_size=30, repetitions=5_000)
    empirical_mean = math.fsum(means) / len(means)
    empirical_variance = math.fsum((value - empirical_mean) ** 2 for value in means) / len(means)
    print(f"sample_means_mean={empirical_mean:.4f}")
    print(f"sample_means_std={math.sqrt(empirical_variance):.4f}")
