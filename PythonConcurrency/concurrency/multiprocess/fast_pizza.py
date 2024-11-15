import multiprocessing as mp

from concurrency.functions import time_sync
from concurrency.multiprocess.pizza import (
    form_dough_balls,
    stretch_dough,
    place_toppings,
    bake_pizza,
    PIZZA_REQUIRED
)


def pizza_worker(work_to_do: callable, inp_cn: mp.Queue, outp_cn: mp.Queue) -> None:
    """
    A worker process, that executes a specific pizza job.

    It takes the next input from its input data channel, carries out its task
    and places its result into its output channel.
    """
    while inp := inp_cn.get():
        result = work_to_do(inp)
        outp_cn.put(result)
    outp_cn.put(None)
    print("Worker finished.")


def process_results(result_cn: mp.Queue) -> None:
    """Simple process that lets you know if you can start eating your pizza."""
    while res := result_cn.get():
        print(f"Pizza {res} is ready.")
    print("Every pizza is ready now, enjoy! :)")


@time_sync
def main() -> None:
    """The main entrypoint of the fast pizza process.

    This implementation imitates a pizza baking process where every well defined step
    is done by a different person. To do that, it implements a datachannel approach,
    where consecutive worker processes are connected via their data channels.
    Workers n (sender) and (n+1) (receiver) are connected by channel n, where worker n
    writes and worker (n+1) reads it. When the 1th worker is done, None is placed into
    the 1th channel, which will propagate through the channels and signal every worker
    process to finish.
    """
    # Create the data channels, Queues specifically in this case
    stretch_cn, top_cn, bake_cn, ready_cn = (
        mp.Queue(),
        mp.Queue(),
        mp.Queue(),
        mp.Queue(),
    )

    # Every process will be placed into this processes list
    processes: list[mp.Process] = []
    processes.append(
        mp.Process(target=pizza_worker, args=(stretch_dough, stretch_cn, top_cn))
    )
    processes.append(
        mp.Process(target=pizza_worker, args=(place_toppings, top_cn, bake_cn))
    )
    processes.append(
        mp.Process(target=pizza_worker, args=(bake_pizza, bake_cn, ready_cn))
    )

    processes.append(mp.Process(target=process_results, args=(ready_cn,)))

    # Start the workers
    for p in processes:
        p.start()

    # Start making the dough balls and pass them to the next worker (pizza dough stretcher).
    # Every consecutive channel / worker will be automatically handled by the worker processes.
    for d in form_dough_balls(PIZZA_REQUIRED):
        stretch_cn.put(d)

    # When every dough ball is ready, signal it to the workers
    stretch_cn.put(None)

    # Wait for every worker / process to finish
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
