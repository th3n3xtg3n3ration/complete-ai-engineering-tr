"""Müfredattaki metadata.yml dosyalarını doğrular."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

import yaml

REQUIRED_KEYS = {
    "id",
    "title",
    "language",
    "level",
    "duration_hours",
    "status",
    "last_reviewed",
    "prerequisites",
    "outcomes",
    "artifacts",
    "maintainers",
}
VALID_LEVELS = {f"L{number}" for number in range(7)}
VALID_STATUSES = {"planned", "draft", "review", "stable", "needs-update", "deprecated"}


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

    duration = data.get("duration_hours")
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append(f"{path}: duration_hours pozitif sayı olmalıdır.")

    for key in ("prerequisites", "outcomes", "artifacts", "maintainers"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{path}: {key} liste olmalıdır.")

    review_date = data.get("last_reviewed")
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
