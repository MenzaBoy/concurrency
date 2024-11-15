import threading

from concurrency.functions import example_task, time_sync


@time_sync
def main():
    # Creating threads for the example tasks
    threads = [
        threading.Thread(target=example_task, args=["example"]),
        threading.Thread(target=example_task, args=["example"]),
        threading.Thread(target=example_task, args=["example"]),
    ]

    # Generates 5_000 OS threads, costly
    # for _ in range(5_000):
    #     threads.append(threading.Thread(target=example_task, args=["example"]))

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for both threads to complete
    for thread in threads:
        thread.join()

    print("Main finished ", end="")


if __name__ == "__main__":
    main()
