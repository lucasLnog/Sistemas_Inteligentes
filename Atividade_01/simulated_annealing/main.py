from pathlib import Path

from simulated_annealing import utils
from simulated_annealing.results import (
    save_raw_results,
    save_summary_results
)
from simulated_annealing.experiments import (
    run_experiment,
    summarize_results
)
from tsp import instance

def main():
    # TSP instance configuration
    number_of_cities = 25
    instance_name = "tsp_sample.csv"

    experiment_config = {
        "initial_temperature": 1000.0,
        "minimum_temperature": 1e-3,
        "cooling_rate": 0.995,
        "max_iterations": 10000
    }

    # Locate and load the TSP instance
    project_directory = Path(__file__).resolve().parent.parent
    instance_file = project_directory / "data" / instance_name

    cities = instance.load_tsp(instance_file)

    if len(cities) != number_of_cities:
        raise ValueError(
            f"Expected {number_of_cities} cities, "
            f"but the instance contains {len(cities)}."
        )

    neighbor_functions = [
        utils.create_swap_neighbor,
        utils.create_insertion_neighbor,
        utils.create_two_opt_neighbor
    ]

    results = []

    for neighbor_function in neighbor_functions:
        print(f"\nRunning experiments with {neighbor_function.__name__}...")
        experiment_results = run_experiment(
            cities=cities,
            neighbor_function=neighbor_function,
            number_of_runs=30,
            experiment_config=experiment_config
        )
        results.append((neighbor_function.__name__, experiment_results))

    summary = summarize_results(results)

    for summary_entry in summary:
        best_run = summary_entry["best_run"]
        print(f"\nSummary for {summary_entry['operator']}:")
        print(f"Best Run: {best_run['run']}")
        print(f"Best Route Seed: {best_run['route_seed']}")
        print(f"Best SA Seed: {best_run['sa_seed']}")
        print(f"Best Cost: {summary_entry['best_cost']:.2f}")
        print(f"Worst Cost: {summary_entry['worst_cost']:.2f}")
        print(f"Mean Cost: {summary_entry['mean_cost']:.2f}")
        print(f"Median Cost: {summary_entry['median_cost']:.2f}")
        print(
            f"Cost Standard Deviation: "
            f"{summary_entry['cost_standard_deviation']:.2f}"
        )
        print(f"Mean Execution Time: {summary_entry['mean_execution_time']:.6f} seconds")
        print(f"Mean Improvement Percentage: {summary_entry['mean_improvement_percentage']:.2f}%")

    results_directory = project_directory / "results"

    experiment_config = {
        "instance": instance_name,
        "number_of_cities": number_of_cities,
        "number_of_runs": 30,
        **experiment_config
    }

    raw_results_file = save_raw_results(
        grouped_results=results,
        experiment_config=experiment_config,
        output_file=results_directory / "sa_raw_results.csv"
    )

    summary_results_file = save_summary_results(
        summary=summary,
        experiment_config=experiment_config,
        output_file=results_directory / "sa_summary.csv"
    )

    print(f"\nRaw results saved to: {raw_results_file}")
    print(f"Summary saved to: {summary_results_file}")

    
if __name__ == "__main__":
    main()