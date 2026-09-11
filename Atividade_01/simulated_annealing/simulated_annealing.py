from tsp import tsp
from simulated_annealing import utils


def simulated_annealing(
    initial_route,
    distance_matrix,
    initial_temperature,
    minimum_temperature,
    cooling_rate,
    neighbor_function,
    rng,
    max_iterations=None
):
    if initial_temperature <= 0:
        raise ValueError(
            "The initial temperature must be greater than zero."
        )

    if minimum_temperature <= 0:
        raise ValueError(
            "The minimum temperature must be greater than zero."
        )

    if minimum_temperature >= initial_temperature:
        raise ValueError(
            "The minimum temperature must be lower than "
            "the initial temperature."
        )

    if not 0 < cooling_rate < 1:
        raise ValueError(
            "The cooling rate must be between zero and one."
        )

    if (
        max_iterations is not None
        and max_iterations <= 0
    ):
        raise ValueError(
            "The maximum number of iterations must be "
            "greater than zero."
        )

    number_of_cities = len(distance_matrix)

    if not tsp.is_valid_route(
        initial_route,
        number_of_cities
    ):
        raise ValueError(
            "The initial route is invalid."
        )

    current_route = initial_route.copy()
    current_cost = tsp.route_cost(
        current_route,
        distance_matrix
    )

    best_route = current_route.copy()
    best_cost = current_cost

    temperature = initial_temperature
    number_of_iterations = 0

    while (
        temperature > minimum_temperature
        and (
            max_iterations is None
            or number_of_iterations < max_iterations
        )
    ):
        candidate_route = neighbor_function(
            current_route,
            rng
        )

        candidate_cost = tsp.route_cost(
            candidate_route,
            distance_matrix
        )

        if utils.should_accept(
            current_cost,
            candidate_cost,
            temperature,
            rng
        ):
            current_route = candidate_route
            current_cost = candidate_cost

            if current_cost < best_cost:
                best_route = current_route.copy()
                best_cost = current_cost

        temperature = cooling_rate * temperature
        number_of_iterations += 1

    return best_route, best_cost