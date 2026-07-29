"""Generate reproducible activation-curve data with the Python standard library."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from math_functions import numerical_derivative, relu, sigmoid, softplus, tanh


def build_rows(start: float, stop: float, step: float) -> list[dict[str, float]]:
    """Create activation and local-slope measurements for an inclusive interval."""
    if step <= 0.0:
        raise ValueError("step must be greater than zero")
    if stop < start:
        raise ValueError("stop must be greater than or equal to start")

    row_count = int(round((stop - start) / step))
    rows: list[dict[str, float]] = []
    for index in range(row_count + 1):
        x_value = start + index * step
        rows.append(
            {
                "x": x_value,
                "sigmoid": sigmoid(x_value),
                "sigmoid_slope": numerical_derivative(sigmoid, x_value),
                "tanh": tanh(x_value),
                "tanh_slope": numerical_derivative(tanh, x_value),
                "relu": relu(x_value),
                "relu_slope": numerical_derivative(relu, x_value),
                "softplus": softplus(x_value),
                "softplus_slope": numerical_derivative(softplus, x_value),
            }
        )
    return rows


def write_csv(rows: list[dict[str, float]], output_path: Path) -> None:
    """Write experiment rows to CSV, creating parent directories when needed."""
    if not rows:
        raise ValueError("rows must not be empty")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, float]]) -> dict[str, object]:
    """Return a JSON-serializable summary of the generated experiment."""
    if not rows:
        raise ValueError("rows must not be empty")

    return {
        "sample_count": len(rows),
        "x_range": [rows[0]["x"], rows[-1]["x"]],
        "observations": {
            "sigmoid_output_range": [rows[0]["sigmoid"], rows[-1]["sigmoid"]],
            "tanh_output_range": [rows[0]["tanh"], rows[-1]["tanh"]],
            "relu_at_zero": next(row["relu"] for row in rows if abs(row["x"]) < 1e-12),
            "softplus_at_zero": next(row["softplus"] for row in rows if abs(row["x"]) < 1e-12),
        },
    }


def parse_args() -> argparse.Namespace:
    lesson_directory = Path(__file__).resolve().parents[1]
    default_output = lesson_directory / "generated" / "activation_curves.csv"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=float, default=-8.0)
    parser.add_argument("--stop", type=float, default=8.0)
    parser.add_argument("--step", type=float, default=0.25)
    parser.add_argument("--output", type=Path, default=default_output)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_rows(args.start, args.stop, args.step)
    write_csv(rows, args.output)
    report = summarize(rows)
    report["output"] = str(args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
