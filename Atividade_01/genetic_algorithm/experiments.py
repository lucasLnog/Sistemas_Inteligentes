import random
import statistics
import time

from genetic_algorithm.genetic_algorithm import (
    genetic_algorithm as run_genetic_algorithm
)


def run_experiment(distance_matrix, experiment_config):
    number_of_runs = experiment_config["number_of_runs"]

    results = []

    for run in range(1, number_of_runs + 1):
        ga_seed = f"GA-{run:02d}"
        rng = random.Random(ga_seed)

        start_time = time.perf_counter()

        ga_result = run_genetic_algorithm(
            distance_matrix=distance_matrix,
            population_size=experiment_config["population_size"],
            number_of_generations=experiment_config["number_of_generations"],
            tournament_size=experiment_config["tournament_size"],
            crossover_rate=experiment_config["crossover_rate"],
            mutation_rate=experiment_config["mutation_rate"],
            elite_size=experiment_config["elite_size"],
            rng=rng
        )

        execution_time = time.perf_counter() - start_time

        initial_best_cost = ga_result["cost_history"][0]
        best_cost = ga_result["best_cost"]

        improvement_percentage = (
            (initial_best_cost - best_cost)
            / initial_best_cost
            * 100
        )

        number_of_evaluations = (
            experiment_config["population_size"]
            * experiment_config["number_of_generations"]
        )

        results.append(
            {
                "run": run,
                "ga_seed": ga_seed,
                "initial_best_cost": initial_best_cost,
                "best_cost": best_cost,
                "improvement_percentage": improvement_percentage,
                "execution_time": execution_time,
                "number_of_evaluations": number_of_evaluations,
                "best_route": ga_result["best_route"],
                "cost_history": ga_result["cost_history"]
            }
        )

    return results


def summarize_results(results):
    if not results:
        raise ValueError(
            "At least one experiment result is required."
        )

    best_costs = [
        result["best_cost"]
        for result in results
    ]

    execution_times = [
        result["execution_time"]
        for result in results
    ]

    improvement_percentages = [
        result["improvement_percentage"]
        for result in results
    ]

    best_run = min(
        results,
        key=lambda result: result["best_cost"]
    )

    return {
        "best_run": best_run,
        "best_cost": min(best_costs),
        "worst_cost": max(best_costs),
        "mean_cost": statistics.mean(best_costs),
        "median_cost": statistics.median(best_costs),
        "cost_standard_deviation": (
            statistics.stdev(best_costs)
            if len(best_costs) > 1
            else 0.0
        ),
        "mean_execution_time": statistics.mean(
            execution_times
        ),
        "mean_improvement_percentage": statistics.mean(
            improvement_percentages
        )
    }