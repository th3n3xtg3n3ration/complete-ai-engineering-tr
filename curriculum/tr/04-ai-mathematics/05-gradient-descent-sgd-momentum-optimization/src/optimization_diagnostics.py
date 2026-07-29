"""Utilities for diagnosing optimization runs from scalar training metrics."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class DiagnosticReport:
    status: str
    messages: tuple[str, ...]


@dataclass
class EarlyStopping:
    """Track a validation metric and stop after a configurable patience window."""

    patience: int = 5
    minimum_delta: float = 0.0
    best_value: float = math.inf
    bad_epochs: int = 0
    best_epoch: int | None = None

    def __post_init__(self) -> None:
        if self.patience <= 0:
            raise ValueError("patience must be positive")
        if self.minimum_delta < 0.0 or not math.isfinite(self.minimum_delta):
            raise ValueError("minimum_delta must be non-negative and finite")

    def update(self, value: float, epoch: int) -> bool:
        """Return ``True`` when training should stop."""

        if not math.isfinite(value):
            return True
        if epoch <= 0:
            raise ValueError("epoch must be positive")

        if value < self.best_value - self.minimum_delta:
            self.best_value = value
            self.best_epoch = epoch
            self.bad_epochs = 0
        else:
            self.bad_epochs += 1
        return self.bad_epochs >= self.patience


def relative_improvement(previous: float, current: float, eps: float = 1e-12) -> float:
    if not math.isfinite(previous) or not math.isfinite(current):
        raise ValueError("loss values must be finite")
    return (previous - current) / max(abs(previous), eps)


def diagnose_training(
    losses: Iterable[float],
    *,
    gradient_norms: Iterable[float] | None = None,
    update_norms: Iterable[float] | None = None,
    plateau_window: int = 5,
    plateau_tolerance: float = 1e-4,
) -> DiagnosticReport:
    """Apply simple, explainable heuristics to a training history."""

    loss_values = [float(value) for value in losses]
    if len(loss_values) < 2:
        raise ValueError("at least two loss values are required")
    if plateau_window < 2 or plateau_window > len(loss_values):
        raise ValueError("plateau_window must be between 2 and the history length")

    messages: list[str] = []
    if not all(math.isfinite(value) for value in loss_values):
        return DiagnosticReport(
            status="diverged",
            messages=("Loss history contains NaN or infinity.",),
        )

    if loss_values[-1] > loss_values[0] * 10.0:
        messages.append("Loss increased by more than 10x; learning rate may be too large.")

    increases = sum(
        current > previous
        for previous, current in zip(loss_values, loss_values[1:], strict=True)
    )
    if increases >= max(2, len(loss_values) // 3):
        messages.append("Loss frequently increases; the run may be oscillating.")

    recent = loss_values[-plateau_window:]
    recent_range = max(recent) - min(recent)
    scale = max(abs(recent[0]), 1e-12)
    if recent_range / scale < plateau_tolerance:
        messages.append("Recent loss changes are very small; training may be on a plateau.")

    if gradient_norms is not None:
        gradients = [float(value) for value in gradient_norms]
        if len(gradients) != len(loss_values):
            raise ValueError("gradient_norms must match the loss history length")
        if not all(math.isfinite(value) and value >= 0.0 for value in gradients):
            messages.append("Gradient norms contain invalid values.")
        elif gradients[-1] > max(100.0, gradients[0] * 20.0):
            messages.append("Gradient norm exploded relative to the start of training.")
        elif gradients[-1] < 1e-10 and recent_range / scale >= plateau_tolerance:
            messages.append("Gradients vanished before the loss stabilized.")

    if update_norms is not None:
        updates = [float(value) for value in update_norms]
        if len(updates) != len(loss_values):
            raise ValueError("update_norms must match the loss history length")
        if not all(math.isfinite(value) and value >= 0.0 for value in updates):
            messages.append("Update norms contain invalid values.")
        elif updates[-1] > max(10.0, updates[0] * 20.0):
            messages.append("Parameter updates exploded relative to the start of training.")
        elif updates[-1] < 1e-12 and recent_range / scale >= plateau_tolerance:
            messages.append("Updates became negligible while loss still changes.")

    if any("exploded" in message or "10x" in message for message in messages):
        status = "unstable"
    elif messages:
        status = "warning"
    else:
        status = "healthy"
        messages.append("No common optimization failure pattern was detected.")

    return DiagnosticReport(status=status, messages=tuple(messages))


if __name__ == "__main__":
    report = diagnose_training(
        [10.0, 5.2, 2.8, 1.5, 1.1, 1.01, 1.005, 1.004],
        gradient_norms=[8.0, 4.0, 2.2, 1.1, 0.5, 0.1, 0.02, 0.01],
        update_norms=[0.8, 0.4, 0.22, 0.11, 0.05, 0.01, 0.002, 0.001],
        plateau_window=3,
        plateau_tolerance=0.01,
    )
    print(report.status)
    for message in report.messages:
        print(f"- {message}")
