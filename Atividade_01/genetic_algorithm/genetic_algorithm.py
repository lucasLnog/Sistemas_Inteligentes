from genetic_algorithm import utils

def genetic_algorithm(
    distance_matrix,
    population_size,
    number_of_generations,
    tournament_size,
    crossover_rate,
    mutation_rate,
    elite_size,
    rng
):
    if number_of_generations <= 0:
        raise ValueError(
            "Number of generations must be greater than zero."
        )

    number_of_cities = len(distance_matrix)

    population = utils.create_initial_population(
        population_size=population_size,
        number_of_cities=number_of_cities,
        rng=rng
    )

    best_route = None
    best_cost = float("inf")
    cost_history = []

    for generation in range(number_of_generations):
        evaluated_population = utils.evaluate_population(
            population,
            distance_matrix
        )

        current_best_route, current_best_cost = (
            evaluated_population[0]
        )

        cost_history.append(current_best_cost)

        if current_best_cost < best_cost:
            best_route = current_best_route.copy()
            best_cost = current_best_cost

        if generation < number_of_generations - 1:
            population = utils.create_next_generation(
                evaluated_population=evaluated_population,
                population_size=population_size,
                tournament_size=tournament_size,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                elite_size=elite_size,
                rng=rng
            )

    return {
        "best_route": best_route,
        "best_cost": best_cost,
        "cost_history": cost_history
    }