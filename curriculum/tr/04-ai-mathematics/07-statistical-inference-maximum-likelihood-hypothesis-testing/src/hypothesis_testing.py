"""Pure-Python hypothesis tests, effect sizes, and multiple-testing helpers."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class TestResult:
    statistic: float
    p_value: float
    estimate: float
    standard_error: float
    confidence_interval: tuple[float, float]
    reject_null: bool


@dataclass(frozen=True)
class ConversionTestResult:
    control_rate: float
    treatment_rate: float
    absolute_lift: float
    relative_lift: float
    statistic: float
    p_value: float
    confidence_interval: tuple[float, float]
    reject_null: bool


def _finite_values(values: Iterable[float], *, minimum_size: int = 1) -> list[float]:
    result = [float(value) for value in values]
    if len(result) < minimum_size:
        raise ValueError(f"at least {minimum_size} observations are required")
    if not all(math.isfinite(value) for value in result):
        raise ValueError("all observations must be finite")
    return result


def _validate_alpha(alpha: float) -> float:
    alpha = float(alpha)
    if not 0.0 < alpha < 1.0 or not math.isfinite(alpha):
        raise ValueError("alpha must be finite and between 0 and 1")
    return alpha


def _mean(values: list[float]) -> float:
    return math.fsum(values) / len(values)


def _sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two observations are required")
    center = _mean(values)
    return math.fsum((value - center) ** 2 for value in values) / (len(values) - 1)


def normal_cdf(value: float) -> float:
    """Return the standard normal cumulative distribution function."""

    value = float(value)
    if not math.isfinite(value):
        if value == math.inf:
            return 1.0
        if value == -math.inf:
            return 0.0
        raise ValueError("value must not be NaN")
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def two_sided_normal_p_value(statistic: float) -> float:
    statistic = float(statistic)
    if math.isnan(statistic):
        raise ValueError("statistic must not be NaN")
    return min(1.0, 2.0 * (1.0 - normal_cdf(abs(statistic))))


def one_sample_mean_test(
    values: Iterable[float],
    *,
    null_mean: float,
    alpha: float = 0.05,
    critical_value: float = 1.959963984540054,
) -> TestResult:
    """Run a two-sided normal-approximation test for one sample mean."""

    data = _finite_values(values, minimum_size=2)
    alpha = _validate_alpha(alpha)
    null_mean = float(null_mean)
    if not math.isfinite(null_mean):
        raise ValueError("null_mean must be finite")
    if critical_value <= 0.0 or not math.isfinite(critical_value):
        raise ValueError("critical_value must be positive and finite")

    estimate = _mean(data)
    standard_error = math.sqrt(_sample_variance(data) / len(data))
    if standard_error == 0.0:
        statistic = 0.0 if estimate == null_mean else math.copysign(math.inf, estimate - null_mean)
    else:
        statistic = (estimate - null_mean) / standard_error
    p_value = two_sided_normal_p_value(statistic)
    margin = critical_value * standard_error
    return TestResult(
        statistic=statistic,
        p_value=p_value,
        estimate=estimate - null_mean,
        standard_error=standard_error,
        confidence_interval=(estimate - margin, estimate + margin),
        reject_null=p_value < alpha,
    )


def two_sample_mean_test(
    control: Iterable[float],
    treatment: Iterable[float],
    *,
    alpha: float = 0.05,
    critical_value: float = 1.959963984540054,
) -> TestResult:
    """Compare independent means with unequal-variance standard errors.

    The standard error matches Welch's test. The p-value uses a normal
    approximation because the standard library does not provide a Student-t
    CDF. Production analyses with small samples should use a validated t CDF.
    """

    control_values = _finite_values(control, minimum_size=2)
    treatment_values = _finite_values(treatment, minimum_size=2)
    alpha = _validate_alpha(alpha)
    if critical_value <= 0.0 or not math.isfinite(critical_value):
        raise ValueError("critical_value must be positive and finite")

    control_mean = _mean(control_values)
    treatment_mean = _mean(treatment_values)
    difference = treatment_mean - control_mean
    variance_term = (
        _sample_variance(control_values) / len(control_values)
        + _sample_variance(treatment_values) / len(treatment_values)
    )
    standard_error = math.sqrt(variance_term)
    if standard_error == 0.0:
        statistic = 0.0 if difference == 0.0 else math.copysign(math.inf, difference)
    else:
        statistic = difference / standard_error
    p_value = two_sided_normal_p_value(statistic)
    margin = critical_value * standard_error
    return TestResult(
        statistic=statistic,
        p_value=p_value,
        estimate=difference,
        standard_error=standard_error,
        confidence_interval=(difference - margin, difference + margin),
        reject_null=p_value < alpha,
    )


def cohens_d(control: Iterable[float], treatment: Iterable[float]) -> float:
    """Return Cohen's d using pooled sample variance."""

    control_values = _finite_values(control, minimum_size=2)
    treatment_values = _finite_values(treatment, minimum_size=2)
    degrees_of_freedom = len(control_values) + len(treatment_values) - 2
    pooled_variance = (
        (len(control_values) - 1) * _sample_variance(control_values)
        + (len(treatment_values) - 1) * _sample_variance(treatment_values)
    ) / degrees_of_freedom
    difference = _mean(treatment_values) - _mean(control_values)
    if pooled_variance == 0.0:
        return 0.0 if difference == 0.0 else math.copysign(math.inf, difference)
    return difference / math.sqrt(pooled_variance)


def conversion_rate_test(
    *,
    control_successes: int,
    control_total: int,
    treatment_successes: int,
    treatment_total: int,
    alpha: float = 0.05,
    critical_value: float = 1.959963984540054,
) -> ConversionTestResult:
    """Run a pooled two-proportion z test and an unpooled confidence interval."""

    alpha = _validate_alpha(alpha)
    if control_total <= 0 or treatment_total <= 0:
        raise ValueError("group totals must be positive")
    if not 0 <= control_successes <= control_total:
        raise ValueError("control successes must be between zero and total")
    if not 0 <= treatment_successes <= treatment_total:
        raise ValueError("treatment successes must be between zero and total")
    if critical_value <= 0.0 or not math.isfinite(critical_value):
        raise ValueError("critical_value must be positive and finite")

    control_rate = control_successes / control_total
    treatment_rate = treatment_successes / treatment_total
    absolute_lift = treatment_rate - control_rate
    relative_lift = (
        absolute_lift / control_rate
        if control_rate > 0.0
        else (0.0 if treatment_rate == 0.0 else math.inf)
    )

    pooled_rate = (
        control_successes + treatment_successes
    ) / (control_total + treatment_total)
    pooled_se = math.sqrt(
        pooled_rate
        * (1.0 - pooled_rate)
        * (1.0 / control_total + 1.0 / treatment_total)
    )
    if pooled_se == 0.0:
        statistic = 0.0 if absolute_lift == 0.0 else math.copysign(math.inf, absolute_lift)
    else:
        statistic = absolute_lift / pooled_se
    p_value = two_sided_normal_p_value(statistic)

    interval_se = math.sqrt(
        control_rate * (1.0 - control_rate) / control_total
        + treatment_rate * (1.0 - treatment_rate) / treatment_total
    )
    margin = critical_value * interval_se
    return ConversionTestResult(
        control_rate=control_rate,
        treatment_rate=treatment_rate,
        absolute_lift=absolute_lift,
        relative_lift=relative_lift,
        statistic=statistic,
        p_value=p_value,
        confidence_interval=(absolute_lift - margin, absolute_lift + margin),
        reject_null=p_value < alpha,
    )


def permutation_test_mean_difference(
    control: Iterable[float],
    treatment: Iterable[float],
    *,
    permutations: int = 10_000,
    seed: int | None = None,
) -> tuple[float, float]:
    """Return observed treatment-minus-control difference and two-sided p-value."""

    control_values = _finite_values(control)
    treatment_values = _finite_values(treatment)
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    observed = _mean(treatment_values) - _mean(control_values)
    combined = control_values + treatment_values
    control_size = len(control_values)
    rng = random.Random(seed)
    extreme = 0

    for _ in range(permutations):
        shuffled = combined.copy()
        rng.shuffle(shuffled)
        permuted_control = shuffled[:control_size]
        permuted_treatment = shuffled[control_size:]
        difference = _mean(permuted_treatment) - _mean(permuted_control)
        if abs(difference) >= abs(observed) - 1e-15:
            extreme += 1

    p_value = (extreme + 1) / (permutations + 1)
    return observed, p_value


def bonferroni_adjust(p_values: Iterable[float]) -> list[float]:
    values = _validated_p_values(p_values)
    count = len(values)
    return [min(1.0, value * count) for value in values]


def benjamini_hochberg_adjust(p_values: Iterable[float]) -> list[float]:
    """Return monotone Benjamini-Hochberg adjusted p-values."""

    values = _validated_p_values(p_values)
    count = len(values)
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    adjusted_sorted = [0.0] * count
    running_minimum = 1.0

    for reverse_index in range(count - 1, -1, -1):
        original_index, p_value = indexed[reverse_index]
        rank = reverse_index + 1
        candidate = p_value * count / rank
        running_minimum = min(running_minimum, candidate)
        adjusted_sorted[reverse_index] = min(1.0, running_minimum)

    adjusted = [0.0] * count
    for sorted_index, (original_index, _) in enumerate(indexed):
        adjusted[original_index] = adjusted_sorted[sorted_index]
    return adjusted


def _validated_p_values(p_values: Iterable[float]) -> list[float]:
    values = [float(value) for value in p_values]
    if not values:
        raise ValueError("at least one p-value is required")
    if not all(math.isfinite(value) and 0.0 <= value <= 1.0 for value in values):
        raise ValueError("p-values must be finite and between 0 and 1")
    return values


if __name__ == "__main__":
    result = conversion_rate_test(
        control_successes=1_080,
        control_total=12_000,
        treatment_successes=1_150,
        treatment_total=12_100,
    )
    print(result)
    print(
        "bonferroni=",
        bonferroni_adjust([0.001, 0.009, 0.013, 0.031, 0.049, 0.08]),
    )
    print(
        "benjamini_hochberg=",
        benjamini_hochberg_adjust([0.001, 0.009, 0.013, 0.031, 0.049, 0.08]),
    )
