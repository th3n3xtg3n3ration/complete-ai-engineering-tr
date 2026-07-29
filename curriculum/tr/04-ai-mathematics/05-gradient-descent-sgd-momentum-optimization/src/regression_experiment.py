"""Train one-dimensional linear regression with several pure Python optimizers."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable

from optimizers import Adam, Optimizer, RMSProp, SGD, l2_norm

Example = tuple[float, float]


@dataclass(frozen=True)
class EpochMetrics:
    epoch: int
    loss: float
    gradient_norm: float
    update_norm: float
    parameters: tuple[float, float]


@dataclass(frozen=True)
class TrainingResult:
    optimizer_name: str
    parameters: tuple[float, float]
    history: tuple[EpochMetrics, ...]


def make_regression_data(
    count: int = 200,
    *,
    slope: float = 3.5,
    intercept: float = -1.25,
    noise_std: float = 0.35,
    seed: int = 42,
) -> list[Example]:
    if count <= 0:
        raise ValueError("count must be positive")
    if noise_std < 0.0 or not math.isfinite(noise_std):
        raise ValueError("noise_std must be non-negative and finite")

    generator = random.Random(seed)
    examples: list[Example] = []
    for _ in range(count):
        feature = generator.uniform(-3.0, 3.0)
        noise = generator.gauss(0.0, noise_std)
        target = slope * feature + intercept + noise
        examples.append((feature, target))
    return examples


def predict(parameters: Iterable[float], feature: float) -> float:
    values = [float(value) for value in parameters]
    if len(values) != 2:
        raise ValueError("linear regression expects [slope, intercept]")
    return values[0] * feature + values[1]


def mean_squared_error(parameters: Iterable[float], examples: Iterable[Example]) -> float:
    values = list(examples)
    if not values:
        raise ValueError("examples must not be empty")
    squared_errors = [
        (predict(parameters, feature) - target) ** 2 for feature, target in values
    ]
    return sum(squared_errors) / len(squared_errors)


def mse_gradient(parameters: Iterable[float], examples: Iterable[Example]) -> list[float]:
    params = [float(value) for value in parameters]
    values = list(examples)
    if len(params) != 2:
        raise ValueError("linear regression expects [slope, intercept]")
    if not values:
        raise ValueError("examples must not be empty")

    slope_gradient = 0.0
    intercept_gradient = 0.0
    for feature, target in values:
        error = predict(params, feature) - target
        slope_gradient += 2.0 * feature * error
        intercept_gradient += 2.0 * error
    scale = 1.0 / len(values)
    return [slope_gradient * scale, intercept_gradient * scale]


def iter_minibatches(
    examples: list[Example],
    batch_size: int,
    *,
    generator: random.Random,
) -> Iterable[list[Example]]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    indices = list(range(len(examples)))
    generator.shuffle(indices)
    for start in range(0, len(indices), batch_size):
        yield [examples[index] for index in indices[start : start + batch_size]]


def train(
    examples: list[Example],
    optimizer: Optimizer,
    *,
    epochs: int = 100,
    batch_size: int = 16,
    seed: int = 7,
    initial_parameters: Iterable[float] = (0.0, 0.0),
) -> TrainingResult:
    if not examples:
        raise ValueError("examples must not be empty")
    if epochs <= 0:
        raise ValueError("epochs must be positive")

    parameters = [float(value) for value in initial_parameters]
    if len(parameters) != 2:
        raise ValueError("initial_parameters must contain slope and intercept")

    generator = random.Random(seed)
    history: list[EpochMetrics] = []

    for epoch in range(1, epochs + 1):
        gradient_norms: list[float] = []
        update_norms: list[float] = []

        for batch in iter_minibatches(examples, batch_size, generator=generator):
            gradient_parameters = parameters
            if isinstance(optimizer, SGD) and optimizer.nesterov:
                gradient_parameters = optimizer.lookahead(parameters)
            gradients = mse_gradient(gradient_parameters, batch)
            previous = parameters
            parameters = optimizer.step(parameters, gradients)
            gradient_norms.append(l2_norm(gradients))
            update_norms.append(
                l2_norm(
                    current - old
                    for current, old in zip(parameters, previous, strict=True)
                )
            )

        loss = mean_squared_error(parameters, examples)
        if not math.isfinite(loss):
            raise FloatingPointError("training diverged to a non-finite loss")
        history.append(
            EpochMetrics(
                epoch=epoch,
                loss=loss,
                gradient_norm=sum(gradient_norms) / len(gradient_norms),
                update_norm=sum(update_norms) / len(update_norms),
                parameters=(parameters[0], parameters[1]),
            )
        )

    return TrainingResult(
        optimizer_name=type(optimizer).__name__,
        parameters=(parameters[0], parameters[1]),
        history=tuple(history),
    )


def run_comparison() -> list[TrainingResult]:
    data = make_regression_data()
    experiments: list[Optimizer] = [
        SGD(learning_rate=0.03),
        SGD(learning_rate=0.02, momentum=0.9),
        RMSProp(learning_rate=0.03),
        Adam(learning_rate=0.05),
    ]

    results: list[TrainingResult] = []
    for optimizer in experiments:
        result = train(data, optimizer, epochs=80, batch_size=20)
        results.append(result)
        final = result.history[-1]
        print(
            f"{result.optimizer_name:<8} "
            f"loss={final.loss:.6f} "
            f"slope={result.parameters[0]:.4f} "
            f"intercept={result.parameters[1]:.4f} "
            f"grad_norm={final.gradient_norm:.6f}"
        )
    return results


if __name__ == "__main__":
    run_comparison()
