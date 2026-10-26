import asyncio

async def job(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return name

async def run_with_timeout(
    jobs: list[tuple[str, float]],
    timeout_s: float
) -> list[dict]:

    async def helper(name: str, delay: float, timeout_s: float):
        try: 
            return await asyncio.wait_for(job(name, delay), timeout_s)
        except TimeoutError:
            return [name, False]
        
    runs = []
    for name, delay in jobs:
        runs.append(helper(name, delay, timeout_s))

    results = await asyncio.gather(*runs)
    ret = []
    for r in results:
        if isinstance(r, list):
            ret.append({
                "name" : r[0],
                "status" : "timeout"
            })
        else:
            ret.append({
                "name" : r,
                "status" : "ok"
            })
    return ret


async def main():
    results = await run_with_timeout(
        [
            ("A", 0.1),
            ("B", 0.5),
            ("C", 0.2),
        ],
        timeout_s=0.3
    )

    print(results)

asyncio.run(main())

asyncio.run(main())