import asyncio

from concurrency.functions import (
    io_bound_async,
    cpu_bound_async,
    time_async,
)


@time_async
async def main():
    """A good implementation of the main function,
    where the async tasks don't wait for each other."""

    tasks = [
        asyncio.create_task(io_bound_async()),
        asyncio.create_task(cpu_bound_async()),
        asyncio.create_task(io_bound_async()),
    ]

    await asyncio.gather(*tasks)
    print("Main finished ", end="")


if __name__ == "__main__":
    asyncio.run(main())
