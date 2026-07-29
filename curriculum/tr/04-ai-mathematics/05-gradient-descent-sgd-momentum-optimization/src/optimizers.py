"""Small, dependency-free optimizers for educational experiments.

The implementations operate on flat ``list[float]`` parameter vectors. They are
intentionally explicit so that optimizer state and update equations are easy to
inspect. Production tensor libraries provide faster and more general versions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Iterable, Protocol

Vector = list[float]


def _to_finite_vector(values: Iterable[float], *, name: str) -> Vector:
    vector = [float(value) for value in values]
    if not vector:
        raise ValueError(f"{name} must not be empty")
    if not all(math.isfinite(value) for value in vector):
        raise ValueError(f"{name} must contain only finite values")
    return vector


def _validate_pair(parameters: Iterable[float], gradients: Iterable[float]) -> tuple[Vector, Vector]:
    params = _to_finite_vector(parameters, name="parameters")
    grads = _to_finite_vector(gradients, name="gradients")
    if len(params) != len(grads):
        raise ValueError("parameters and gradients must have the same length")
    return params, grads


def l2_norm(values: Iterable[float]) -> float:
    vector = [float(value) for value in values]
    return math.sqrt(sum(value * value for value in vector))


def clip_by_global_norm(gradients: Iterable[float], max_norm: float, eps: float = 1e-12) -> Vector:
    """Scale a gradient vector so that its L2 norm does not exceed ``max_norm``."""

    grads = _to_finite_vector(gradients, name="gradients")
    if not math.isfinite(max_norm) or max_norm <= 0.0:
        raise ValueError("max_norm must be a positive finite number")
    norm = l2_norm(grads)
    if norm <= max_norm:
        return grads
    scale = max_norm / (norm + eps)
    return [gradient * scale for gradient in grads]


class Optimizer(Protocol):
    learning_rate: float

    def step(self, parameters: Iterable[float], gradients: Iterable[float]) -> Vector:
        """Return updated parameters."""


@dataclass
class SGD:
    """Gradient descent with optional momentum, Nesterov mode and weight decay."""

    learning_rate: float = 0.01
    momentum: float = 0.0
    nesterov: bool = False
    weight_decay: float = 0.0
    max_grad_norm: float | None = None
    velocity: Vector = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not math.isfinite(self.learning_rate) or self.learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive and finite")
        if not 0.0 <= self.momentum < 1.0:
            raise ValueError("momentum must be in [0, 1)")
        if self.nesterov and self.momentum == 0.0:
            raise ValueError("nesterov requires non-zero momentum")
        if not math.isfinite(self.weight_decay) or self.weight_decay < 0.0:
            raise ValueError("weight_decay must be non-negative and finite")
        if self.max_grad_norm is not None and self.max_grad_norm <= 0.0:
            raise ValueError("max_grad_norm must be positive")

    def lookahead(self, parameters: Iterable[float]) -> Vector:
        """Return the Nesterov lookahead point used to evaluate a gradient."""

        params = _to_finite_vector(parameters, name="parameters")
        if not self.velocity:
            self.velocity = [0.0] * len(params)
        if len(self.velocity) != len(params):
            raise ValueError("parameter vector size changed after optimizer initialization")
        return [
            parameter - self.learning_rate * self.momentum * velocity
            for parameter, velocity in zip(params, self.velocity, strict=True)
        ]

    def step(self, parameters: Iterable[float], gradients: Iterable[float]) -> Vector:
        params, grads = _validate_pair(parameters, gradients)
        if self.max_grad_norm is not None:
            grads = clip_by_global_norm(grads, self.max_grad_norm)
        if not self.velocity:
            self.velocity = [0.0] * len(params)
        if len(self.velocity) != len(params):
            raise ValueError("parameter vector size changed after optimizer initialization")

        updated: Vector = []
        new_velocity: Vector = []
        for parameter, gradient, velocity in zip(params, grads, self.velocity, strict=True):
            regularized_gradient = gradient + self.weight_decay * parameter
            current_velocity = self.momentum * velocity + regularized_gradient
            if self.nesterov:
                direction = self.momentum * current_velocity + regularized_gradient
            else:
                direction = current_velocity
            updated.append(parameter - self.learning_rate * direction)
            new_velocity.append(current_velocity)

        self.velocity = new_velocity
        return updated


@dataclass
class AdaGrad:
    learning_rate: float = 0.1
    eps: float = 1e-8
    accumulator: Vector = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.learning_rate <= 0.0 or not math.isfinite(self.learning_rate):
            raise ValueError("learning_rate must be positive and finite")
        if self.eps <= 0.0:
            raise ValueError("eps must be positive")

    def step(self, parameters: Iterable[float], gradients: Iterable[float]) -> Vector:
        params, grads = _validate_pair(parameters, gradients)
        if not self.accumulator:
            self.accumulator = [0.0] * len(params)
        if len(self.accumulator) != len(params):
            raise ValueError("parameter vector size changed after optimizer initialization")

        updated: Vector = []
        next_accumulator: Vector = []
        for parameter, gradient, total in zip(params, grads, self.accumulator, strict=True):
            total += gradient * gradient
            updated.append(parameter - self.learning_rate * gradient / (math.sqrt(total) + self.eps))
            next_accumulator.append(total)
        self.accumulator = next_accumulator
        return updated


@dataclass
class RMSProp:
    learning_rate: float = 0.01
    decay: float = 0.9
    eps: float = 1e-8
    square_average: Vector = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.learning_rate <= 0.0 or not math.isfinite(self.learning_rate):
            raise ValueError("learning_rate must be positive and finite")
        if not 0.0 <= self.decay < 1.0:
            raise ValueError("decay must be in [0, 1)")
        if self.eps <= 0.0:
            raise ValueError("eps must be positive")

    def step(self, parameters: Iterable[float], gradients: Iterable[float]) -> Vector:
        params, grads = _validate_pair(parameters, gradients)
        if not self.square_average:
            self.square_average = [0.0] * len(params)
        if len(self.square_average) != len(params):
            raise ValueError("parameter vector size changed after optimizer initialization")

        updated: Vector = []
        next_average: Vector = []
        for parameter, gradient, average in zip(params, grads, self.square_average, strict=True):
            average = self.decay * average + (1.0 - self.decay) * gradient * gradient
            updated.append(parameter - self.learning_rate * gradient / (math.sqrt(average) + self.eps))
            next_average.append(average)
        self.square_average = next_average
        return updated


@dataclass
class Adam:
    learning_rate: float = 0.001
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8
    weight_decay: float = 0.0
    first_moment: Vector = field(default_factory=list, init=False)
    second_moment: Vector = field(default_factory=list, init=False)
    timestep: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.learning_rate <= 0.0 or not math.isfinite(self.learning_rate):
            raise ValueError("learning_rate must be positive and finite")
        if not 0.0 <= self.beta1 < 1.0 or not 0.0 <= self.beta2 < 1.0:
            raise ValueError("beta1 and beta2 must be in [0, 1)")
        if self.eps <= 0.0:
            raise ValueError("eps must be positive")
        if self.weight_decay < 0.0 or not math.isfinite(self.weight_decay):
            raise ValueError("weight_decay must be non-negative and finite")

    def step(self, parameters: Iterable[float], gradients: Iterable[float]) -> Vector:
        params, grads = _validate_pair(parameters, gradients)
        if not self.first_moment:
            self.first_moment = [0.0] * len(params)
            self.second_moment = [0.0] * len(params)
        if len(self.first_moment) != len(params):
            raise ValueError("parameter vector size changed after optimizer initialization")

        self.timestep += 1
        updated: Vector = []
        next_first: Vector = []
        next_second: Vector = []

        for parameter, gradient, first, second in zip(
            params, grads, self.first_moment, self.second_moment, strict=True
        ):
            first = self.beta1 * first + (1.0 - self.beta1) * gradient
            second = self.beta2 * second + (1.0 - self.beta2) * gradient * gradient
            corrected_first = first / (1.0 - self.beta1**self.timestep)
            corrected_second = second / (1.0 - self.beta2**self.timestep)
            adaptive_update = corrected_first / (math.sqrt(corrected_second) + self.eps)
            # Decoupled weight decay: AdamW-style parameter shrinkage.
            updated.append(
                parameter
                - self.learning_rate * adaptive_update
                - self.learning_rate * self.weight_decay * parameter
            )
            next_first.append(first)
            next_second.append(second)

        self.first_moment = next_first
        self.second_moment = next_second
        return updated


def step_decay(initial_rate: float, step: int, *, drop: float = 0.5, every: int = 100) -> float:
    if initial_rate <= 0.0 or drop <= 0.0 or every <= 0 or step < 0:
        raise ValueError("invalid step-decay arguments")
    return initial_rate * drop ** (step // every)


def exponential_decay(initial_rate: float, step: int, *, decay: float = 0.99) -> float:
    if initial_rate <= 0.0 or not 0.0 < decay <= 1.0 or step < 0:
        raise ValueError("invalid exponential-decay arguments")
    return initial_rate * decay**step


def cosine_decay(initial_rate: float, step: int, total_steps: int, *, minimum_rate: float = 0.0) -> float:
    if initial_rate <= 0.0 or minimum_rate < 0.0 or minimum_rate > initial_rate:
        raise ValueError("invalid learning-rate bounds")
    if total_steps <= 0 or step < 0:
        raise ValueError("total_steps must be positive and step must be non-negative")
    progress = min(step, total_steps) / total_steps
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return minimum_rate + (initial_rate - minimum_rate) * cosine


if __name__ == "__main__":
    parameters = [8.0, -6.0]
    optimizer = Adam(learning_rate=0.2)
    for iteration in range(1, 101):
        gradients = [2.0 * parameters[0], 8.0 * parameters[1]]
        parameters = optimizer.step(parameters, gradients)
        if iteration % 20 == 0:
            loss = parameters[0] ** 2 + 4.0 * parameters[1] ** 2
            print(f"step={iteration:03d} loss={loss:.6f} parameters={parameters}")
