from __future__ import annotations

import cProfile
import io
import logging
import pstats

from observable_service import ModelService


def run_workload(iterations: int = 5_000) -> None:
    logging.disable(logging.CRITICAL)
    service = ModelService()
    samples = (
        "I love this model",
        "A neutral sentence",
        "This is excellent",
        "The response is good",
    )
    for index in range(iterations):
        service.predict(samples[index % len(samples)], request_id=str(index))


def profile_workload(iterations: int = 5_000, limit: int = 15) -> str:
    profiler = cProfile.Profile()
    profiler.enable()
    run_workload(iterations)
    profiler.disable()

    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output)
    stats.strip_dirs().sort_stats("cumulative").print_stats(limit)
    return output.getvalue()


if __name__ == "__main__":
    print(profile_workload())
