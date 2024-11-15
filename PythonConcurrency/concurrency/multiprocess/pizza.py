import time

STEP_PROCESS_SIZE = 100_000_000 # This parameter defines how much time each function takes to complete
PIZZA_REQUIRED = 5


def form_dough_balls(dough: object):  # -> Generator[doughBall]
    for d in range(1, dough + 1):
        start = time.perf_counter()
        for _ in range(STEP_PROCESS_SIZE):
            pass
        print(f"Yielded doughBall |{d}| in {time.perf_counter()-start:.2f} seconds.")
        yield d


def stretch_dough(dough_ball: object):  # -> pizzaBase
    start = time.perf_counter()
    for _ in range(STEP_PROCESS_SIZE):
        pass
    print(
        f"Stretched pizzaBase |{dough_ball}| in {time.perf_counter()-start:.2f} seconds."
    )
    return dough_ball


def place_toppings(pizza_base: object):  # -> unbakedPizza
    start = time.perf_counter()
    for _ in range(STEP_PROCESS_SIZE):
        pass
    print(
        f"Topped unbakedPizza |{pizza_base}| in {time.perf_counter()-start:.2f} seconds"
    )
    return pizza_base


def bake_pizza(unbaked_pizza: object):  # -> bakedPizza
    start = time.perf_counter()
    for _ in range(STEP_PROCESS_SIZE):
        pass
    print(f"Baked pizza |{unbaked_pizza}| in {time.perf_counter()-start:.2f} seconds")
    return unbaked_pizza
