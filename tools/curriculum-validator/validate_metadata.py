"""Müfredattaki metadata.yml dosyalarını doğrular."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
from typing import Any

import yaml

REQUIRED_KEYS = {
    "id",
    "title",
    "language",
    "level",
    "status",
    "prerequisites",
    "artifacts",
}
VALID_LEVELS = {f"L{number}" for number in range(7)}
VALID_STATUSES = {
    "planned",
    "draft",
    "review",
    "stable",
    "completed",
    "needs-update",
    "deprecated",
}


def _first_present(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return None


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        return [f"{path}: YAML kökü mapping olmalıdır."]

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"{path}: eksik alanlar: {', '.join(sorted(missing))}")

    if data.get("level") not in VALID_LEVELS:
        errors.append(f"{path}: geçersiz level: {data.get('level')}")

    if data.get("status") not in VALID_STATUSES:
        errors.append(f"{path}: geçersiz status: {data.get('status')}")

    duration = _first_present(data, "duration_hours", "estimated_hours")
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append(
            f"{path}: duration_hours veya estimated_hours pozitif sayı olmalıdır."
        )

    prerequisites = data.get("prerequisites")
    if prerequisites is not None and not isinstance(prerequisites, list):
        errors.append(f"{path}: prerequisites liste olmalıdır.")

    outcomes = _first_present(data, "outcomes", "learning_outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        errors.append(f"{path}: outcomes veya learning_outcomes dolu liste olmalıdır.")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, (list, dict)):
        errors.append(f"{path}: artifacts liste veya mapping olmalıdır.")

    maintainers = data.get("maintainers")
    if maintainers is not None and not isinstance(maintainers, list):
        errors.append(f"{path}: maintainers liste olmalıdır.")

    review_date = data.get("last_reviewed")
    if review_date is not None:
        if isinstance(review_date, date):
            review_date = review_date.isoformat()
        try:
            date.fromisoformat(str(review_date))
        except ValueError:
            errors.append(f"{path}: last_reviewed YYYY-MM-DD biçiminde olmalıdır.")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    metadata_files = sorted((root / "curriculum").rglob("metadata.yml"))

    if not metadata_files:
        print("Metadata dosyası bulunamadı.")
        return 1

    errors = [error for path in metadata_files for error in validate_file(path)]
    if errors:
        print("Metadata doğrulaması başarısız:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Başarılı: {len(metadata_files)} metadata dosyası doğrulandı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
