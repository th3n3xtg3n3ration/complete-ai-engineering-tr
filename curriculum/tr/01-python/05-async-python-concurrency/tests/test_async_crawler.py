import asyncio
import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "src" / "async_crawler.py"
spec = importlib.util.spec_from_file_location("async_crawler", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

crawl_many = module.crawl_many
crawl_one = module.crawl_one


def test_crawl_many_preserves_order():
    async def scenario():
        async def fetcher(url: str) -> str:
            await asyncio.sleep(0)
            return url.upper()

        results = await crawl_many(["a", "b", "c"], fetcher, concurrency=2)
        assert [result.content for result in results] == ["A", "B", "C"]

    asyncio.run(scenario())


def test_retry_succeeds_after_transient_failure():
    async def scenario():
        attempts = 0

        async def fetcher(url: str) -> str:
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise ConnectionError("temporary")
            return "ok"

        result = await crawl_one("x", fetcher, asyncio.Semaphore(1), max_retries=1)
        assert result.succeeded
        assert result.attempts == 2
        assert result.content == "ok"

    asyncio.run(scenario())


def test_timeout_becomes_failed_result():
    async def scenario():
        async def fetcher(url: str) -> str:
            await asyncio.sleep(0.05)
            return "late"

        result = await crawl_one(
            "x", fetcher, asyncio.Semaphore(1), timeout_seconds=0.001, max_retries=0
        )
        assert not result.succeeded
        assert result.content is None
        assert "TimeoutError" in result.error

    asyncio.run(scenario())


def test_concurrency_limit_is_respected():
    async def scenario():
        active = 0
        maximum = 0
        lock = asyncio.Lock()

        async def fetcher(url: str) -> str:
            nonlocal active, maximum
            async with lock:
                active += 1
                maximum = max(maximum, active)
            await asyncio.sleep(0.01)
            async with lock:
                active -= 1
            return url

        await crawl_many([str(i) for i in range(8)], fetcher, concurrency=3)
        assert maximum <= 3

    asyncio.run(scenario())


def test_invalid_concurrency_is_rejected():
    async def fetcher(url: str) -> str:
        return url

    with pytest.raises(ValueError):
        asyncio.run(crawl_many(["x"], fetcher, concurrency=0))
