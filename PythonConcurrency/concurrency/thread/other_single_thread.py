from concurrency.functions import other_example_task, time_sync


@time_sync
def main():
    other_example_task("other example")
    other_example_task("other example")
    other_example_task("other example")

    print("Main finished ", end="")


if __name__ == "__main__":
    main()
