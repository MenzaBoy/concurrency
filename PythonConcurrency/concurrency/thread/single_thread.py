from concurrency.functions import example_task, time_sync


@time_sync
def main():
    example_task("example")
    example_task("example")
    example_task("example")

    print("Main finished ", end="")


if __name__ == "__main__":
    main()
