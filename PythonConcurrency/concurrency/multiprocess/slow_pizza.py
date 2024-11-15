from concurrency.functions import time_sync
from concurrency.multiprocess.pizza import (
    form_dough_balls,
    stretch_dough,
    place_toppings,
    bake_pizza,
    PIZZA_REQUIRED
)


@time_sync
def main() -> None:
    """A really simple approach for making pizza.

    Every step is run after its previous step is ready. It basically imitates the process
    of 1 person baking pizzas going through the steps one-by-one.
    """
    for dough_ball in form_dough_balls(PIZZA_REQUIRED):
        pizza_base = stretch_dough(dough_ball)
        unbaked_pizza = place_toppings(pizza_base)
        bake_pizza(unbaked_pizza)


if __name__ == "__main__":
    main()
