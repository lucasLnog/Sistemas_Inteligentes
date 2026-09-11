import math


def create_swap_neighbor(route, rng):
    if len(route) < 3:
        raise ValueError("The route must contain at least three cities to create a neighbor.")

    neighbor = route.copy()

    first, second = rng.sample(range(1, len(route)), 2)

    neighbor[first], neighbor[second] = neighbor[second], neighbor[first]

    return neighbor


def create_insertion_neighbor(route, rng):
    if len(route) < 3:
        raise ValueError("The route must contain at least three cities to create a neighbor.")

    neighbor = route.copy()

    source, destination = rng.sample(range(1, len(route)), 2)

    city = neighbor.pop(source)
    neighbor.insert(destination, city)

    return neighbor


def create_two_opt_neighbor(route, rng):
    if len(route) < 4:
        raise ValueError("The route must contain at least four cities to create a neighbor.")

    neighbor = route.copy()

    first = 1
    second = len(route) - 1

    while first == 1 and second == len(route) - 1:
        first, second = sorted(rng.sample(range(1, len(route)), 2))

    neighbor[first:second + 1] = reversed(neighbor[first:second + 1])

    return neighbor


def should_accept(current_cost, candidate_cost, temperature, rng):
    if not temperature > 0:
        raise ValueError("The temperature must be greater than zero.")

    if candidate_cost <= current_cost:
        return True
    
    delta = candidate_cost - current_cost

    probability = math.exp(-delta/temperature)

    random_number = rng.random()

    if random_number < probability:
        return True

    return False