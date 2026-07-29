"""Compare embedding rankings with cosine similarity and Euclidean distance."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from linear_algebra import cosine_similarity, euclidean_distance, normalize

Metric = Literal["cosine", "euclidean"]


@dataclass(frozen=True)
class DocumentEmbedding:
    document_id: str
    title: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class SearchResult:
    rank: int
    document_id: str
    title: str
    metric: Metric
    normalized: bool
    score: float


DOCUMENTS = (
    DocumentEmbedding("doc-001", "Python testing guide", (0.82, 0.12, 0.31, 0.08)),
    DocumentEmbedding("doc-002", "Neural network optimization", (0.21, 0.91, 0.24, 0.36)),
    DocumentEmbedding("doc-003", "Vector search systems", (0.76, 0.20, 0.48, 0.15)),
    DocumentEmbedding("doc-004", "Linux process management", (0.67, 0.08, 0.17, 0.05)),
    DocumentEmbedding("doc-005", "Transformer attention", (0.35, 0.72, 0.61, 0.44)),
)

QUERY = (0.78, 0.16, 0.43, 0.11)


def rank_embeddings(
    query: tuple[float, ...],
    documents: tuple[DocumentEmbedding, ...],
    *,
    metric: Metric,
    normalized: bool,
) -> list[SearchResult]:
    """Rank document embeddings from best to worst."""
    if not documents:
        return []

    query_vector = normalize(query) if normalized else list(query)
    scored: list[tuple[DocumentEmbedding, float]] = []

    for document in documents:
        candidate = normalize(document.vector) if normalized else list(document.vector)
        if metric == "cosine":
            score = cosine_similarity(query_vector, candidate)
        elif metric == "euclidean":
            score = euclidean_distance(query_vector, candidate)
        else:
            raise ValueError(f"unsupported metric: {metric}")
        scored.append((document, score))

    reverse = metric == "cosine"
    scored.sort(key=lambda item: item[1], reverse=reverse)

    return [
        SearchResult(
            rank=index,
            document_id=document.document_id,
            title=document.title,
            metric=metric,
            normalized=normalized,
            score=score,
        )
        for index, (document, score) in enumerate(scored, start=1)
    ]


def run_experiment() -> list[SearchResult]:
    results: list[SearchResult] = []
    for normalized in (False, True):
        for metric in ("cosine", "euclidean"):
            results.extend(
                rank_embeddings(
                    QUERY,
                    DOCUMENTS,
                    metric=metric,
                    normalized=normalized,
                )
            )
    return results


def write_results(results: list[SearchResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["rank", "document_id", "title", "metric", "normalized", "score"],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "rank": result.rank,
                    "document_id": result.document_id,
                    "title": result.title,
                    "metric": result.metric,
                    "normalized": result.normalized,
                    "score": f"{result.score:.8f}",
                }
            )


def print_summary(results: list[SearchResult]) -> None:
    groups: dict[tuple[Metric, bool], list[SearchResult]] = {}
    for result in results:
        groups.setdefault((result.metric, result.normalized), []).append(result)

    for (metric, normalized), group in groups.items():
        top = min(group, key=lambda result: result.rank)
        print(
            f"metric={metric:<9} normalized={str(normalized):<5} "
            f"top={top.document_id} score={top.score:.6f} title={top.title}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("embedding_results.csv"),
        help="CSV output path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_experiment()
    write_results(results, args.output)
    print_summary(results)
    print(f"wrote {len(results)} rows to {args.output}")


if __name__ == "__main__":
    main()
