"""Maximum-likelihood and simple MAP estimators implemented with pure Python."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class GaussianEstimate:
    mean: float
    variance_mle: float
    standard_deviation_mle: float


def _binary_values(values: Iterable[int | bool]) -> list[int]:
    result: list[int] = []
    for value in values:
        integer = int(value)
        if integer not in (0, 1) or value != integer:
            raise ValueError("Bernoulli observations must be 0 or 1")
        result.append(integer)
    if not result:
        raise ValueError("at least one observation is required")
    return result


def _finite_values(values: Iterable[float]) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError("at least one observation is required")
    if not all(math.isfinite(value) for value in result):
        raise ValueError("all observations must be finite")
    return result


def bernoulli_log_likelihood(
    observations: Iterable[int | bool],
    probability: float,
) -> float:
    """Return the Bernoulli log-likelihood for a candidate probability."""

    data = _binary_values(observations)
    probability = float(probability)
    if not 0.0 <= probability <= 1.0 or not math.isfinite(probability):
        raise ValueError("probability must be finite and between 0 and 1")

    successes = sum(data)
    failures = len(data) - successes
    if probability == 0.0:
        return 0.0 if successes == 0 else -math.inf
    if probability == 1.0:
        return 0.0 if failures == 0 else -math.inf
    return successes * math.log(probability) + failures * math.log1p(-probability)


def bernoulli_mle(observations: Iterable[int | bool]) -> float:
    """Return the closed-form MLE of a Bernoulli probability."""

    data = _binary_values(observations)
    return sum(data) / len(data)


def bernoulli_grid_search_mle(
    observations: Iterable[int | bool],
    candidates: Iterable[float],
) -> tuple[float, float]:
    """Return ``(best_probability, best_log_likelihood)`` over a finite grid."""

    data = _binary_values(observations)
    candidate_values = [float(value) for value in candidates]
    if not candidate_values:
        raise ValueError("at least one candidate is required")

    best_probability: float | None = None
    best_score = -math.inf
    for probability in candidate_values:
        score = bernoulli_log_likelihood(data, probability)
        if score > best_score:
            best_probability = probability
            best_score = score
    if best_probability is None:
        raise ValueError("candidate grid contains no valid maximizer")
    return best_probability, best_score


def beta_bernoulli_posterior(
    successes: int,
    failures: int,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> tuple[float, float]:
    """Return posterior Beta parameters after Bernoulli observations."""

    if successes < 0 or failures < 0:
        raise ValueError("successes and failures must be non-negative")
    if alpha <= 0.0 or beta <= 0.0:
        raise ValueError("alpha and beta must be positive")
    if not math.isfinite(alpha) or not math.isfinite(beta):
        raise ValueError("alpha and beta must be finite")
    return alpha + successes, beta + failures


def beta_bernoulli_posterior_mean(
    successes: int,
    failures: int,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> float:
    posterior_alpha, posterior_beta = beta_bernoulli_posterior(
        successes,
        failures,
        alpha=alpha,
        beta=beta,
    )
    return posterior_alpha / (posterior_alpha + posterior_beta)


def beta_bernoulli_map(
    successes: int,
    failures: int,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> float:
    """Return a Beta-Bernoulli MAP estimate.

    A unique interior mode requires both posterior shape parameters to exceed
    one. Boundary modes are returned when exactly one side is at or below one.
    A U-shaped posterior has two boundary modes and therefore no unique MAP;
    this function raises ``ValueError`` in that case.
    """

    posterior_alpha, posterior_beta = beta_bernoulli_posterior(
        successes,
        failures,
        alpha=alpha,
        beta=beta,
    )
    if posterior_alpha > 1.0 and posterior_beta > 1.0:
        return (posterior_alpha - 1.0) / (posterior_alpha + posterior_beta - 2.0)
    if posterior_alpha <= 1.0 < posterior_beta:
        return 0.0
    if posterior_beta <= 1.0 < posterior_alpha:
        return 1.0
    raise ValueError("posterior has no unique MAP mode")


def gaussian_log_likelihood(
    observations: Iterable[float],
    *,
    mean: float,
    variance: float,
) -> float:
    """Return the iid Gaussian log-likelihood."""

    data = _finite_values(observations)
    mean = float(mean)
    variance = float(variance)
    if not math.isfinite(mean):
        raise ValueError("mean must be finite")
    if variance <= 0.0 or not math.isfinite(variance):
        raise ValueError("variance must be positive and finite")

    squared_error = math.fsum((value - mean) ** 2 for value in data)
    return -0.5 * (
        len(data) * math.log(2.0 * math.pi * variance)
        + squared_error / variance
    )


def gaussian_mle(observations: Iterable[float]) -> GaussianEstimate:
    """Return closed-form Gaussian MLE estimates for mean and variance."""

    data = _finite_values(observations)
    estimated_mean = math.fsum(data) / len(data)
    variance = math.fsum(
        (value - estimated_mean) ** 2 for value in data
    ) / len(data)
    return GaussianEstimate(
        mean=estimated_mean,
        variance_mle=variance,
        standard_deviation_mle=math.sqrt(variance),
    )


if __name__ == "__main__":
    conversions = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
    candidates = [index / 100 for index in range(5, 96)]
    print(f"closed_form_mle={bernoulli_mle(conversions):.3f}")
    print(f"grid_search={bernoulli_grid_search_mle(conversions, candidates)}")
    print(
        "map=",
        beta_bernoulli_map(sum(conversions), len(conversions) - sum(conversions), alpha=2, beta=2),
    )
    print(f"gaussian_mle={gaussian_mle([2.0, 3.0, 4.0, 5.0])}")
