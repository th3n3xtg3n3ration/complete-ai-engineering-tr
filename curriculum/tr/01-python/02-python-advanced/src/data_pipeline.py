"""İleri Python kavramlarını kullanan küçük ve test edilebilir veri hattı."""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from time import perf_counter
from typing import Callable, Iterable, Iterator, TypeVar

T = TypeVar("T")


class InvalidRecordError(ValueError):
    """Bir kayıt doğrulama kurallarını karşılamadığında yükseltilir."""


@dataclass(frozen=True, slots=True)
class Record:
    name: str
    score: float


def timed(function: Callable[..., T]) -> Callable[..., T]:
    """Fonksiyonun çalışma süresini yazdıran basit decorator."""

    @wraps(function)
    def wrapper(*args: object, **kwargs: object) -> T:
        started = perf_counter()
        result = function(*args, **kwargs)
        elapsed = perf_counter() - started
        print(f"{function.__name__} {elapsed:.6f} saniyede tamamlandı.")
        return result

    return wrapper


def validate_record(raw: dict[str, object]) -> Record:
    """Ham sözlüğü doğrulayıp değişmez bir Record nesnesine dönüştürür."""
    name = raw.get("name")
    score = raw.get("score")

    if not isinstance(name, str) or not name.strip():
        raise InvalidRecordError("'name' boş olmayan bir metin olmalıdır.")
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise InvalidRecordError("'score' sayısal olmalıdır.")
    if not 0 <= float(score) <= 100:
        raise InvalidRecordError("'score' 0 ile 100 arasında olmalıdır.")

    return Record(name=name.strip(), score=float(score))


def iter_valid_records(rows: Iterable[dict[str, object]]) -> Iterator[Record]:
    """Geçerli kayıtları tembel biçimde üretir; hatalı kayıtları atlar."""
    for row in rows:
        try:
            yield validate_record(row)
        except InvalidRecordError:
            continue


def batch(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Bir iterable'ı en fazla size elemanlı listelere böler."""
    if size <= 0:
        raise ValueError("size pozitif olmalıdır.")

    current: list[T] = []
    for item in items:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current


@timed
def summarize(records: Iterable[Record]) -> dict[str, float | int]:
    """Kayıt sayısı, ortalama ve en yüksek puanı döndürür."""
    scores = [record.score for record in records]
    if not scores:
        return {"count": 0, "average": 0.0, "maximum": 0.0}
    return {
        "count": len(scores),
        "average": round(sum(scores) / len(scores), 2),
        "maximum": max(scores),
    }


def main() -> None:
    rows: list[dict[str, object]] = [
        {"name": "Ada", "score": 92},
        {"name": "Mert", "score": 78.5},
        {"name": "", "score": 60},
        {"name": "Ece", "score": 105},
    ]
    records = list(iter_valid_records(rows))
    print(records)
    print(summarize(records))
    print(list(batch(records, size=1)))


if __name__ == "__main__":
    main()
