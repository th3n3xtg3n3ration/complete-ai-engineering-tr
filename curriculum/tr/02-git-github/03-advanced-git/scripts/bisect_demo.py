"""Small deterministic check for use with `git bisect run`.

Exit code 0 means the current commit is good.
Exit code 1 means the current commit contains the regression.
"""

from __future__ import annotations


def model_score(predictions: list[int], labels: list[int]) -> float:
    if len(predictions) != len(labels):
        raise ValueError("predictions and labels must have equal length")
    if not labels:
        raise ValueError("labels cannot be empty")
    correct = sum(prediction == label for prediction, label in zip(predictions, labels))
    return correct / len(labels)


def main() -> int:
    score = model_score([1, 0, 1, 1], [1, 0, 1, 0])
    return 0 if score >= 0.75 else 1


if __name__ == "__main__":
    raise SystemExit(main())
