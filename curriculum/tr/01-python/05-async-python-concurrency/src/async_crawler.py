from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from typing import Awaitable, Callable, Iterable

Fetcher = Callable[[str], Awaitable[str]]


@dataclass(frozen=True, slots=True)
class CrawlResult:
    url: str
    content: str | None
    attempts: int
    elapsed_seconds: float
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


async def crawl_one(
    url: str,
    fetcher: Fetcher,
    semaphore: asyncio.Semaphore,
    *,
    timeout_seconds: float = 2.0,
    max_retries: int = 2,
    retry_delay_seconds: float = 0.01,
) -> CrawlResult:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if max_retries < 0:
        raise ValueError("max_retries cannot be negative")

    started = perf_counter()
    attempts = 0

    for attempt in range(max_retries + 1):
        attempts = attempt + 1
        try:
            async with semaphore:
                async with asyncio.timeout(timeout_seconds):
                    content = await fetcher(url)
            return CrawlResult(
                url=url,
                content=content,
                attempts=attempts,
                elapsed_seconds=perf_counter() - started,
            )
        except asyncio.CancelledError:
            raise
        except (TimeoutError, ConnectionError) as exc:
            if attempt == max_retries:
                return CrawlResult(
                    url=url,
                    content=None,
                    attempts=attempts,
                    elapsed_seconds=perf_counter() - started,
                    error=f"{type(exc).__name__}: {exc}",
                )
            await asyncio.sleep(retry_delay_seconds * (2**attempt))

    raise RuntimeError("unreachable")


async def crawl_many(
    urls: Iterable[str],
    fetcher: Fetcher,
    *,
    concurrency: int = 5,
    timeout_seconds: float = 2.0,
    max_retries: int = 2,
) -> list[CrawlResult]:
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")

    semaphore = asyncio.Semaphore(concurrency)
    tasks = [
        asyncio.create_task(
            crawl_one(
                url,
                fetcher,
                semaphore,
                timeout_seconds=timeout_seconds,
                max_retries=max_retries,
            )
        )
        for url in urls
    ]
    return list(await asyncio.gather(*tasks))


async def demo_fetcher(url: str) -> str:
    await asyncio.sleep(0.02)
    return f"content:{url}"


async def main() -> None:
    results = await crawl_many(
        ["https://example.com/a", "https://example.com/b"],
        demo_fetcher,
        concurrency=2,
    )
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
