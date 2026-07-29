"""Pure-Python multiclass softmax regression capstone.

The module combines linear algebra, differentiation, optimization, probability,
and information theory without requiring NumPy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from collections.abc import Sequence


FeatureVector = Sequence[float]
Dataset = Sequence[FeatureVector]
Labels = Sequence[int]


def _stable_softmax(logits: Sequence[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in logits)
    if not values or any(not math.isfinite(value) for value in values):
        raise ValueError("logits must be a non-empty sequence of finite values")
    maximum = max(values)
    exponentials = tuple(math.exp(value - maximum) for value in values)
    denominator = sum(exponentials)
    return tuple(value / denominator for value in exponentials)


def _validate_dataset(features: Dataset, labels: Labels) -> tuple[list[list[float]], list[int]]:
    rows = [[float(value) for value in row] for row in features]
    targets = [int(label) for label in labels]
    if not rows:
        raise ValueError("features must not be empty")
    if len(rows) != len(targets):
        raise ValueError("features and labels must have equal length")
    width = len(rows[0])
    if width == 0 or any(len(row) != width for row in rows):
        raise ValueError("feature rows must be non-empty and rectangular")
    if any(not math.isfinite(value) for row in rows for value in row):
        raise ValueError("features must be finite")
    if any(label < 0 for label in targets):
        raise ValueError("labels must be non-negative integers")
    return rows, targets


@dataclass
class TrainingHistory:
    losses: list[float] = field(default_factory=list)
    accuracies: list[float] = field(default_factory=list)


@dataclass
class SoftmaxRegression:
    """Multiclass linear classifier trained with full-batch gradient descent."""

    learning_rate: float = 0.1
    epochs: int = 300
    l2: float = 0.0
    label_smoothing: float = 0.0
    seed: int = 42
    weights: list[list[float]] = field(default_factory=list, init=False)
    biases: list[float] = field(default_factory=list, init=False)
    class_count: int = field(default=0, init=False)
    feature_count: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if not math.isfinite(self.learning_rate) or self.learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive and finite")
        if self.epochs <= 0:
            raise ValueError("epochs must be positive")
        if not math.isfinite(self.l2) or self.l2 < 0.0:
            raise ValueError("l2 must be non-negative and finite")
        if not math.isfinite(self.label_smoothing) or not 0.0 <= self.label_smoothing < 1.0:
            raise ValueError("label_smoothing must be within [0, 1)")

    def _initialize(self, feature_count: int, class_count: int) -> None:
        generator = random.Random(self.seed)
        scale = 1.0 / math.sqrt(feature_count)
        self.weights = [
            [generator.uniform(-scale, scale) for _ in range(feature_count)]
            for _ in range(class_count)
        ]
        self.biases = [0.0 for _ in range(class_count)]
        self.feature_count = feature_count
        self.class_count = class_count

    def _logits(self, row: Sequence[float]) -> tuple[float, ...]:
        if not self.weights:
            raise RuntimeError("model is not fitted")
        if len(row) != self.feature_count:
            raise ValueError("feature width does not match the fitted model")
        return tuple(
            sum(weight * value for weight, value in zip(class_weights, row, strict=True))
            + self.biases[class_index]
            for class_index, class_weights in enumerate(self.weights)
        )

    def predict_proba_one(self, row: FeatureVector) -> tuple[float, ...]:
        values = tuple(float(value) for value in row)
        if any(not math.isfinite(value) for value in values):
            raise ValueError("features must be finite")
        return _stable_softmax(self._logits(values))

    def predict_proba(self, features: Dataset) -> list[tuple[float, ...]]:
        return [self.predict_proba_one(row) for row in features]

    def predict(self, features: Dataset) -> list[int]:
        return [max(range(len(probabilities)), key=probabilities.__getitem__) for probabilities in self.predict_proba(features)]

    def _target_distribution(self, target: int) -> tuple[float, ...]:
        off_value = self.label_smoothing / self.class_count
        on_value = 1.0 - self.label_smoothing + off_value
        return tuple(on_value if index == target else off_value for index in range(self.class_count))

    def loss(self, features: Dataset, labels: Labels) -> float:
        rows, targets = _validate_dataset(features, labels)
        if not self.weights:
            raise RuntimeError("model is not fitted")
        if any(target >= self.class_count for target in targets):
            raise ValueError("label exceeds the fitted class range")

        data_loss = 0.0
        for row, target in zip(rows, targets, strict=True):
            probabilities = self.predict_proba_one(row)
            target_distribution = self._target_distribution(target)
            data_loss -= sum(
                expected * math.log(max(probability, 1e-300))
                for expected, probability in zip(target_distribution, probabilities, strict=True)
            )
        data_loss /= len(rows)
        penalty = 0.5 * self.l2 * sum(weight * weight for class_weights in self.weights for weight in class_weights)
        return data_loss + penalty

    def fit(self, features: Dataset, labels: Labels) -> TrainingHistory:
        rows, targets = _validate_dataset(features, labels)
        class_count = max(targets) + 1
        if class_count < 2:
            raise ValueError("at least two classes are required")
        self._initialize(len(rows[0]), class_count)
        history = TrainingHistory()

        for _ in range(self.epochs):
            weight_gradients = [
                [0.0 for _ in range(self.feature_count)]
                for _ in range(self.class_count)
            ]
            bias_gradients = [0.0 for _ in range(self.class_count)]

            for row, target in zip(rows, targets, strict=True):
                probabilities = self.predict_proba_one(row)
                target_distribution = self._target_distribution(target)
                for class_index in range(self.class_count):
                    error = probabilities[class_index] - target_distribution[class_index]
                    bias_gradients[class_index] += error
                    for feature_index, value in enumerate(row):
                        weight_gradients[class_index][feature_index] += error * value

            sample_count = len(rows)
            for class_index in range(self.class_count):
                self.biases[class_index] -= self.learning_rate * (
                    bias_gradients[class_index] / sample_count
                )
                for feature_index in range(self.feature_count):
                    gradient = weight_gradients[class_index][feature_index] / sample_count
                    gradient += self.l2 * self.weights[class_index][feature_index]
                    self.weights[class_index][feature_index] -= self.learning_rate * gradient

            history.losses.append(self.loss(rows, targets))
            history.accuracies.append(accuracy(targets, self.predict(rows)))

        return history


def accuracy(labels: Labels, predictions: Labels) -> float:
    targets = tuple(int(label) for label in labels)
    predicted = tuple(int(label) for label in predictions)
    if not targets or len(targets) != len(predicted):
        raise ValueError("labels and predictions must be non-empty and equal length")
    return sum(target == guess for target, guess in zip(targets, predicted, strict=True)) / len(targets)


def confusion_matrix(labels: Labels, predictions: Labels, *, class_count: int | None = None) -> list[list[int]]:
    targets = tuple(int(label) for label in labels)
    predicted = tuple(int(label) for label in predictions)
    if not targets or len(targets) != len(predicted):
        raise ValueError("labels and predictions must be non-empty and equal length")
    inferred = max(max(targets), max(predicted)) + 1
    size = inferred if class_count is None else class_count
    if size < inferred:
        raise ValueError("class_count is smaller than observed labels")
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for target, guess in zip(targets, predicted, strict=True):
        matrix[target][guess] += 1
    return matrix


def expected_calibration_error(
    labels: Labels,
    probabilities: Sequence[Sequence[float]],
    *,
    bins: int = 10,
) -> float:
    """Compute top-label expected calibration error."""

    targets = tuple(int(label) for label in labels)
    rows = tuple(tuple(float(value) for value in row) for row in probabilities)
    if not targets or len(targets) != len(rows):
        raise ValueError("labels and probabilities must be non-empty and equal length")
    if bins <= 0:
        raise ValueError("bins must be positive")

    bucket_confidence = [0.0 for _ in range(bins)]
    bucket_correct = [0 for _ in range(bins)]
    bucket_count = [0 for _ in range(bins)]

    for target, row in zip(targets, rows, strict=True):
        if not row or any(not math.isfinite(value) or value < 0.0 for value in row):
            raise ValueError("probability rows must contain finite non-negative values")
        if not math.isclose(sum(row), 1.0, abs_tol=1e-9, rel_tol=0.0):
            raise ValueError("each probability row must sum to 1")
        prediction = max(range(len(row)), key=row.__getitem__)
        confidence = row[prediction]
        bucket = min(int(confidence * bins), bins - 1)
        bucket_confidence[bucket] += confidence
        bucket_correct[bucket] += int(prediction == target)
        bucket_count[bucket] += 1

    total = len(targets)
    error = 0.0
    for confidence_sum, correct_sum, count in zip(
        bucket_confidence,
        bucket_correct,
        bucket_count,
        strict=True,
    ):
        if count == 0:
            continue
        average_confidence = confidence_sum / count
        average_accuracy = correct_sum / count
        error += (count / total) * abs(average_accuracy - average_confidence)
    return error


def make_three_class_dataset(*, samples_per_class: int = 40, seed: int = 7) -> tuple[list[list[float]], list[int]]:
    """Create a reproducible, linearly separable two-dimensional dataset."""

    if samples_per_class <= 0:
        raise ValueError("samples_per_class must be positive")
    generator = random.Random(seed)
    centers = ((-2.5, -2.0), (2.5, -2.0), (0.0, 2.5))
    features: list[list[float]] = []
    labels: list[int] = []
    for class_index, (center_x, center_y) in enumerate(centers):
        for _ in range(samples_per_class):
            features.append(
                [
                    generator.gauss(center_x, 0.55),
                    generator.gauss(center_y, 0.55),
                ]
            )
            labels.append(class_index)
    return features, labels


if __name__ == "__main__":
    x_values, y_values = make_three_class_dataset()
    classifier = SoftmaxRegression(
        learning_rate=0.15,
        epochs=250,
        l2=0.001,
        label_smoothing=0.05,
        seed=11,
    )
    training = classifier.fit(x_values, y_values)
    predicted_labels = classifier.predict(x_values)
    predicted_probabilities = classifier.predict_proba(x_values)
    print("initial loss:", round(training.losses[0], 6))
    print("final loss:", round(training.losses[-1], 6))
    print("accuracy:", round(accuracy(y_values, predicted_labels), 4))
    print("ECE:", round(expected_calibration_error(y_values, predicted_probabilities), 4))
    print("confusion matrix:", confusion_matrix(y_values, predicted_labels))
