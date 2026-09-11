from tsp import tsp

def create_initial_population(
    population_size,
    number_of_cities,
    rng
):
    if population_size <= 0:
        raise ValueError("The population size must be greater than zero.")

    if number_of_cities < 3:
        raise ValueError("The number of cities must be at least three.")

    population = []

    for _ in range(population_size):
        route = tsp.create_random_route(number_of_cities, rng)
        population.append(route)

    return population


def evaluate_population(population, distance_matrix):
    evaluated_population = []

    for individual in population:
        evaluated_population.append((
            individual, 
            tsp.route_cost(individual, distance_matrix)
        ))

    return sorted(evaluated_population, key=lambda x: x[1])


def tournament_selection(
    evaluated_population,
    tournament_size,
    rng
):
    if tournament_size <= 0:
        raise ValueError("The tournament size must be greater than zero.")

    if tournament_size > len(evaluated_population):
        raise ValueError("The tournament size cannot be larger than the population size.")

    tournament = rng.sample(evaluated_population, tournament_size)
    winner = min(tournament, key=lambda x: x[1])

    return winner[0].copy()


def ordered_crossover(parent_a, parent_b, rng):
    if len(parent_a) != len(parent_b):
        raise ValueError(
            "Parents must have the same length."
        )

    if len(parent_a) < 4:
        raise ValueError(
            "Parents must have at least four cities."
        )

    if parent_a[0] != 0 or parent_b[0] != 0:
        raise ValueError(
            "Both parents must start at city zero."
        )

    size = len(parent_a)

    parent_a_cities = set(parent_a)
    parent_b_cities = set(parent_b)

    if len(parent_a_cities) != size:
        raise ValueError(
            "Parent A contains repeated cities."
        )

    if len(parent_b_cities) != size:
        raise ValueError(
            "Parent B contains repeated cities."
        )

    if parent_a_cities != parent_b_cities:
        raise ValueError(
            "Parents must contain the same cities."
        )

    start, end = sorted(
        rng.sample(range(1, size), 2)
    )

    child = [None] * size
    child[0] = 0

    segment = parent_a[start:end + 1]
    child[start:end + 1] = segment

    used_cities = set(segment)
    used_cities.add(0)

    parent_b_circular = (
        parent_b[end + 1:]
        + parent_b[1:end + 1]
    )

    remaining_cities = [
        city
        for city in parent_b_circular
        if city not in used_cities
    ]

    empty_positions = (
        list(range(end + 1, size))
        + list(range(1, start))
    )

    if len(remaining_cities) != len(empty_positions):
        raise RuntimeError(
            "Ordered crossover produced inconsistent data."
        )

    for position, city in zip(
        empty_positions,
        remaining_cities
    ):
        child[position] = city

    return child


def swap_mutation(individual, mutation_rate, rng):
    if not (0 <= mutation_rate <=1):
        raise ValueError("Mutation rate must be between 0 and 1.")

    if len(individual) < 3:
        raise ValueError(
            "The individual must contain at least three cities."
        )
    
    mutated_individual = individual.copy()

    if rng.random() < mutation_rate:
        position_a, position_b = rng.sample(range(1, len(mutated_individual)), 2)
        mutated_individual[position_a], mutated_individual[position_b] = mutated_individual[position_b], mutated_individual[position_a]

    return mutated_individual


def create_next_generation(
    evaluated_population,
    population_size,
    tournament_size,
    crossover_rate,
    mutation_rate,
    elite_size,
    rng
):
    if population_size <= 0:
        raise ValueError(
            "Population size must be greater than zero."
        )

    if len(evaluated_population) != population_size:
        raise ValueError(
            "Evaluated population size must match population size."
        )
    
    if elite_size < 0:
        raise ValueError("Elite size must be non-negative.")

    if elite_size > population_size:
        raise ValueError("Elite size cannot be larger than the population size.")

    if not 0.0 <= crossover_rate <= 1.0:
        raise ValueError(
            "Crossover rate must be between 0 and 1."
        )

    next_generation = [
        individual.copy()
        for individual, _
        in evaluated_population[:elite_size]
    ]

    while len(next_generation) < population_size:
        parent_a = tournament_selection(evaluated_population, tournament_size, rng)
        parent_b = tournament_selection(evaluated_population, tournament_size, rng)

        if rng.random() < crossover_rate:
            child_a = ordered_crossover(parent_a, parent_b, rng)
            child_b = ordered_crossover(parent_b, parent_a, rng)
        else:
            child_a = parent_a.copy()
            child_b = parent_b.copy()

        mutated_child_a = swap_mutation(child_a, mutation_rate, rng)
        mutated_child_b = swap_mutation(child_b, mutation_rate, rng)

        next_generation.append(mutated_child_a)
        if len(next_generation) < population_size:
            next_generation.append(mutated_child_b)

    return next_generation