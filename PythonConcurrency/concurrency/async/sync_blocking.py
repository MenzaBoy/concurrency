import asyncio

from concurrency.functions import (
    io_bound_async,
    cpu_bound,
    io_bound,
    time_async,
)


@time_async
async def main():
    """A poor implementation of the main function,
    where the event loop gets blocked."""

    # bg_task = asyncio.create_task(cpu_bound_async())
    bg_task = asyncio.create_task(io_bound_async())

    io_bound()
    cpu_bound()

    print("Blocking tasks finished.")

    await bg_task
    print("Main finished ", end="")


if __name__ == "__main__":
    asyncio.run(main())
