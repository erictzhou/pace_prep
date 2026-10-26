import asyncio

async def job(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    print(f"{name} completed")
    return name

async def main():
    a = asyncio.create_task(job("A", 0.3))
    b = asyncio.create_task(job("B", 0.1))
    c = asyncio.create_task(job("C", 0.2))

    await a
    await b
    await c
    print([a, b, c])
    

asyncio.run(main())