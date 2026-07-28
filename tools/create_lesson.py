"""Yeni ders klasörünü standart şablondan oluşturan komut satırı aracı."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_LEVELS = {f"L{number}" for number in range(7)}


def create_lesson(module: Path, lesson: str, title: str, level: str) -> Path:
    if not SLUG_PATTERN.fullmatch(lesson):
        raise ValueError("Ders adı '01-variables-and-data-types' biçiminde olmalıdır.")
    if level not in VALID_LEVELS:
        raise ValueError("Seviye L0 ile L6 arasında olmalıdır.")

    root = Path(__file__).resolve().parents[1]
    template = root / "templates" / "lesson-template"
    destination = module / lesson

    if destination.exists():
        raise FileExistsError(f"Hedef zaten var: {destination}")

    module.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, destination)

    replacements = {
        "module-topic-number": lesson,
        "Ders Başlığı": title,
        "level: L0": f"level: {level}",
        "**Seviye:** L0": f"**Seviye:** {level}",
        "last_reviewed: 2026-07-28": f"last_reviewed: {date.today().isoformat()}",
    }

    for path in destination.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".yml", ".json", ".py"}:
            continue
        content = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            content = content.replace(old, new)
        path.write_text(content, encoding="utf-8")

    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, type=Path)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--level", default="L0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    created = create_lesson(args.module, args.lesson, args.title, args.level)
    print(f"Ders oluşturuldu: {created}")


if __name__ == "__main__":
    main()
