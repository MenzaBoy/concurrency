import asyncio

from concurrency.functions import (
    io_bound_async,
    cpu_bound_async,
    time_async,
)


@time_async
async def main():
    """A basic implementation of the main function,
    where the async tasks might wait for each other."""

    # bg_task = asyncio.create_task(cpu_bound_async())
    bg_task = asyncio.create_task(io_bound_async())

    await io_bound_async()
    await cpu_bound_async()

    # await cpu_bound_async()
    # await io_bound_async()

    print("Blocking tasks finished.")
    await bg_task
    print("Main finished ", end="")


if __name__ == "__main__":
    asyncio.run(main())
