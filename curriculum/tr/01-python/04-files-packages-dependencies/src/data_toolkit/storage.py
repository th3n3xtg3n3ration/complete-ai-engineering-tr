from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable

from data_toolkit.models import Record


def save_records(path: Path, records: Iterable[Record]) -> None:
    """Kayıtları UTF-8 JSON dosyasına atomik biçimde yazar."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [record.to_dict() for record in records]

    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        delete=False,
        suffix=".tmp",
    ) as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        temporary_path = Path(stream.name)

    temporary_path.replace(destination)


def load_records(path: Path) -> list[Record]:
    """JSON dosyasını okur ve her kaydı doğrular."""
    source = Path(path)
    with source.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)

    if not isinstance(payload, list):
        raise TypeError("JSON kökü bir liste olmalıdır")

    records: list[Record] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise TypeError(f"{index}. kayıt nesne olmalıdır")
        records.append(Record.from_dict(item))
    return records


def summarize(records: Iterable[Record]) -> dict[str, float]:
    """Kategori bazında değer toplamı üretir."""
    totals: dict[str, float] = {}
    for record in records:
        totals[record.category] = totals.get(record.category, 0.0) + record.value
    return totals