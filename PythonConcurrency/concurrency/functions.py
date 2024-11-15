import time
import asyncio
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

N_TH_FIBO = 36


def time_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        print(f"in {time.perf_counter()-start:.2f} seconds.")

    return wrapper


def time_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        await func(*args, **kwargs)
        print(f"in {time.perf_counter()-start:.2f} seconds.")

    return wrapper


@time_sync
def io_bound(task_description: str = None):
    """Simulates a blocking I/O operation."""
    print(
        f"Starting {task_description if task_description else 'I/O bound'} operation."
    )
    time.sleep(5)
    print(
        f"{task_description if task_description else 'I/O bound'} operation finished ",
        end="",
    )


@time_sync
def cpu_bound(task_description: str = None, fibo_value: int = None):
    """Simulates a blocking CPU operation."""
    print(
        f"Starting {task_description if task_description else 'CPU bound'} operation."
    )

    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    fibonacci(fibo_value if fibo_value else N_TH_FIBO)
    print(
        f"{task_description if task_description else 'CPU bound'} operation finished ",
        end="",
    )


def example_task(desc: str = None):
    io_bound(desc)


def other_example_task(desc: str = None):
    cpu_bound(desc)


@time_async
async def io_bound_async():
    """A random async task that should be running in the background."""
    print("Starting I/O bound async task.")
    for i in range(5):
        print(f"I/O bound async task iteration {i}.")
        await asyncio.sleep(1)
    print(f"I/O bound async task finished ", end="")


@time_async
async def cpu_bound_async():
    """A random async task that runs on the CPU, it doesn't make much sense.
    Leaving it here for 'completeness'."""

    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    print("Starting CPU bound async task.")
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, fibonacci, N_TH_FIBO)
    print(f"CPU bound async task finished ", end="")
