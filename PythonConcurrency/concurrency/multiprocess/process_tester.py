import time
import random
import multiprocessing as mp
import matplotlib.pyplot as plt

from concurrency.functions import time_sync

@time_sync
def bubble_sort(lst):
    """Bubble Sort algorithm.
    
    A really simple implementation of the bubble sort algorithm to utilize the CPU.
    It repeatedly compares adjacent elements and swaps them if they are out of order.
    """
    n = len(lst)
    for i in range(n):
        swapped = False
        for j in range(
            0, n - i - 1
        ):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True
        if not swapped:
            break
    print(f"Sorted array ", end="")


class ProcessTester:
    """
    A class to test the multiprocessing module.

    This class runs and evaluates the execution of parallel CPU-bound tasks using multiple
    CPU cores. The end product is a scatter plot which shows how a certain number of parallel 
    tasks run, using various number of CPU cores.
    """

    def __init__(self, num_of_cores: int, max_num_of_processes: int) -> None:
        """
        Initialize the ProcessTester with a specific number of cores and max processes.

        Args:
            num_of_cores (int): Number of worker processes.
        """
        self.num_of_cores = num_of_cores
        self.max_num_of_processes = max_num_of_processes
        self.task_queue = mp.Queue()
        self.results = []
    
    @staticmethod
    def worker(task_queue: mp.Queue) -> None:
        """
        Worker process to execute a task from the queue.
        """

        while task := task_queue.get():
            func, args = task
            print(
                f"Worker process {mp.current_process().name} is executing a task."
            )
            func(*args)

    def add_task(self, func: callable, args: tuple = (None,)) -> None:
        """
        Add a task to the task queue.

        Args:
            func (Callable): The function to execute.
            args (tuple): The arguments to pass to the function.
        """
        self.task_queue.put((func, args))

    def run(self) -> None:
        """
        Run the ProcessTester.

        Go through max_num_of_processes iterations. The n-th iteration will
        create n processes and run num_of_cores tasks on them. The higher the
        process number, the less time the execution should take. This performance increase
        should start diminishing after process num reaches num_of_cores/2 and completely stop
        after num_of_cores.
        """
        for iteration in range(1,self.max_num_of_processes+1):
            self.workers = [
            mp.Process(target=self.worker, args=(self.task_queue,))
            for _ in range(iteration)
        ]

            for worker in self.workers:
                worker.start()

            start = time.perf_counter()
            for _ in range(self.num_of_cores):
                self.add_task(bubble_sort, ([random.randint(1,1_000_000) for _ in range(8_000)],))

            for _ in range(iteration):
                self.task_queue.put(None)

            for worker in self.workers:
                worker.join()

            self.results.append(round(time.perf_counter() - start, 2))
            print(f"Completed run with {iteration} processes in {self.results[-1]:2f} seconds.")
        self.create_and_save_plot()


    def create_and_save_plot(self) -> None:
        x_values = list(
        range(1, len(self.results) + 1)
        )

        # Create a scatter plot
        plt.scatter(x_values, self.results)
        plt.xticks(x_values)

        # Add labels to the plot
        plt.xlabel("Number of cores")
        plt.ylabel("Execution time (s)")
        plt.title("Task Execution Times per CPU")

        # Save it
        plt.savefig("concurrency/results/scatter_plot.png", dpi=300)


@time_sync
def main() -> None:
    """
    The main entry point of the application.

    It creates and runs a ProcessTester instance to measure the performance of the
    multiprocessing module.
    """
    cpu_cores = mp.cpu_count()
    pt = ProcessTester(num_of_cores=cpu_cores, max_num_of_processes=cpu_cores+5)
    pt.run()

    print("Main finished ", end='')


if __name__ == "__main__":
    main()
