import asyncio

async def worker(log: list[str]) -> None:
    # Implement worker
    log.append("started")
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Task was cancelled")
        log.append("cancelled")
        raise
    finally:
        log.append("cleanup")


async def main():
    log = []
    task = asyncio.create_task(worker(log))
    await asyncio.sleep(0.85)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Task was cancelled")

    #await task
    log.append("observed")
    print(log)
    # Implement main

asyncio.run(main())