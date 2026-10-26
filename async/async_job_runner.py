import asyncio

async def job(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} finished"

async def main():
    a = job("A", 0.3)
    b = job("B", 0.1)
    c = job("C", 0.2)

    results = await asyncio.gather(a, b, c)
    print(results)

asyncio.run(main())