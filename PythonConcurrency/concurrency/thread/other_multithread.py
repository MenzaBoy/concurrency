import threading

from concurrency.functions import other_example_task, time_sync


@time_sync
def main():
    # Creating threads for the example tasks
    threads = [
        threading.Thread(target=other_example_task, args=["other example"]),
        threading.Thread(target=other_example_task, args=["other example"]),
        threading.Thread(target=other_example_task, args=["other example"]),
    ]

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for both threads to complete
    for thread in threads:
        thread.join()

    print("Main finished ", end="")


if __name__ == "__main__":
    main()
