import asyncio

async def job(name: str, delay: float) -> str:
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished")
    return name

async def run_bounded(
    jobs: list[tuple[str, float]],
    limit: int
) -> list[str]:

    if limit <= 0:
        raise ValueError("Semaphore value nonpositive")
    sem = asyncio.Semaphore(limit)

    async def limited(name: str, delay: float):
        async with sem:
            return await job(name, delay)

    coro = []
    for j in jobs:
        coro.append(limited(j[0], j[1]))

    result = await asyncio.gather(*coro)
    print(result)

async def main():
    results = await run_bounded(
        [
            ("A", 0.3),
            ("B", 0.1),
            ("C", 0.1),
            ("D", 0.1),
        ],
        limit=2
    )
    print(results)

asyncio.run(main())