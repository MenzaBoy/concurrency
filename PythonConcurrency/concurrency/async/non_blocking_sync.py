import asyncio
from concurrent.futures import ThreadPoolExecutor

from concurrency.functions import (
    io_bound_async,
    cpu_bound,
    io_bound,
    time_async,
)


@time_async
async def main():
    """A proper implementation of the main function,
    where the blocking synchronous tasks are run in an executor."""

    bg_task = asyncio.create_task(io_bound_async())
    sync_tasks = []

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=10) as pool:
        sync_tasks.append(loop.run_in_executor(pool, cpu_bound))
        for _ in range(3):
            sync_tasks.append(loop.run_in_executor(pool, io_bound))

        await asyncio.gather(*sync_tasks)

    print("Executor tasks finished.")
    await bg_task
    print("Main finished ", end="")


if __name__ == "__main__":
    asyncio.run(main())
