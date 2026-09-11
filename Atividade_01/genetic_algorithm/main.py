from pathlib import Path

from tsp import instance
from tsp import tsp

from genetic_algorithm.experiments import (
    run_experiment,
    summarize_results
)
from genetic_algorithm.results import (
    save_raw_results,
    save_summary_results
)



def main():
    # TSP instance configuration
    number_of_cities = 25
    instance_name = "tsp_sample.csv"

    # Genetic Algorithm configuration
    experiment_config = {
        "instance": instance_name,
        "number_of_cities": number_of_cities,
        "number_of_runs": 30,
        "population_size": 100,
        "number_of_generations": 500,
        "tournament_size": 3,
        "crossover_rate": 0.9,
        "mutation_rate": 0.05,
        "elite_size": 1
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

    distance_matrix = tsp.create_distance_matrix(cities)

    print(
        f"Running {experiment_config['number_of_runs']} "
        f"genetic algorithm experiments..."
    )

    results = run_experiment(
        distance_matrix=distance_matrix,
        experiment_config=experiment_config
    )

    # Validate individual results
    for result in results:
        assert result["best_route"][0] == 0
        assert tsp.is_valid_route(
            result["best_route"],
            number_of_cities
        )
        assert len(result["cost_history"]) == (
            experiment_config["number_of_generations"]
        )
        assert result["best_cost"] == min(
            result["cost_history"]
        )

        calculated_cost = tsp.route_cost(
            result["best_route"],
            distance_matrix
        )

        assert calculated_cost == result["best_cost"]

    summary = summarize_results(results)
    best_run = summary["best_run"]

    results_directory = project_directory / "results"

    raw_results_file = save_raw_results(
        results=results,
        experiment_config=experiment_config,
        output_file=results_directory / "ga_raw_results.csv"
    )

    summary_results_file = save_summary_results(
        summary=summary,
        experiment_config=experiment_config,
        output_file=results_directory / "ga_summary.csv"
    )

    print("\nGenetic Algorithm Summary:")
    print(f"Best Run: {best_run['run']}")
    print(f"GA Seed: {best_run['ga_seed']}")
    print(f"Best Route: {best_run['best_route']}")
    print(f"Best Cost: {summary['best_cost']:.2f}")
    print(f"Worst Cost: {summary['worst_cost']:.2f}")
    print(f"Mean Cost: {summary['mean_cost']:.2f}")
    print(f"Median Cost: {summary['median_cost']:.2f}")
    print(
        f"Cost Standard Deviation: "
        f"{summary['cost_standard_deviation']:.2f}"
    )
    print(
        f"Mean Execution Time: "
        f"{summary['mean_execution_time']:.6f} seconds"
    )
    print(
        f"Mean Improvement Percentage: "
        f"{summary['mean_improvement_percentage']:.2f}%"
    )
    print(
        f"Evaluations per Run: "
        f"{best_run['number_of_evaluations']}"
    )

    print(
        f"\nRaw results saved to: "
        f"{raw_results_file}"
    )
    print(
        f"Summary saved to: "
        f"{summary_results_file}"
    )


if __name__ == "__main__":
    main()