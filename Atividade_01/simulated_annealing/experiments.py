import random
import statistics
import time

from simulated_annealing.simulated_annealing import simulated_annealing
from tsp import tsp



def run_experiment(
    cities,
    neighbor_function,
    number_of_runs,
    experiment_config
):
    results = []

    distance_matrix = tsp.create_distance_matrix(cities)

    for run in range(number_of_runs):
        route_seed = f"ROUTE-{(run + 1):02d}"

        initial_route = tsp.create_random_route(len(cities), random.Random(route_seed))
        initial_cost = tsp.route_cost(initial_route, distance_matrix)

        sa_seed = f"SA-{(run + 1):02d}"

        start_time = time.perf_counter()
        
        best_route, best_cost = simulated_annealing(
            initial_route=initial_route,
            distance_matrix=distance_matrix,
            initial_temperature=experiment_config["initial_temperature"],
            minimum_temperature=experiment_config["minimum_temperature"],
            cooling_rate=experiment_config["cooling_rate"],
            neighbor_function=neighbor_function,
            rng=random.Random(sa_seed),
            max_iterations=experiment_config["max_iterations"]
        )

        end_time = time.perf_counter()

        execution_time = end_time - start_time

        improvement_percentage = (
            (initial_cost - best_cost) / initial_cost * 100
        )

        results.append(
            {
                "run": run + 1,
                "operator": neighbor_function.__name__,
                "route_seed": route_seed,
                "sa_seed": sa_seed,
                "initial_cost": initial_cost,
                "best_cost": best_cost,
                "improvement_percentage": improvement_percentage,
                "execution_time": execution_time,
                "best_route": best_route
            }
        )

    return results


def summarize_results(experiment_results):
    summary = []

    for operator_name, result in experiment_results:
        best_costs = [run_result["best_cost"] for run_result in result]
        execution_times = [run_result["execution_time"] for run_result in result]
        improvement_percentages = [run_result["improvement_percentage"] for run_result in result]

        summary.append(
            {
                "operator": operator_name,
                "best_run": min(result, key=lambda x: x["best_cost"]),
                "best_cost": min(best_costs),
                "worst_cost": max(best_costs),
                "mean_cost": statistics.mean(best_costs),
                "median_cost": statistics.median(best_costs),
                "cost_standard_deviation": statistics.stdev(best_costs) if len(best_costs) > 1 else 0.0,
                "mean_execution_time": statistics.mean(execution_times),
                "mean_improvement_percentage": statistics.mean(improvement_percentages)
            }
        )

    return summary