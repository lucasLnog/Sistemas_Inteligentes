import csv
import json
from pathlib import Path


def save_raw_results(
    results,
    experiment_config,
    output_file
):
    output_file = Path(output_file)
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        *experiment_config.keys(),
        "run",
        "ga_seed",
        "initial_best_cost",
        "best_cost",
        "improvement_percentage",
        "execution_time",
        "number_of_evaluations",
        "best_route",
        "cost_history"
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            row = {
                **experiment_config,
                "run": result["run"],
                "ga_seed": result["ga_seed"],
                "initial_best_cost": (
                    result["initial_best_cost"]
                ),
                "best_cost": result["best_cost"],
                "improvement_percentage": (
                    result["improvement_percentage"]
                ),
                "execution_time": (
                    result["execution_time"]
                ),
                "number_of_evaluations": (
                    result["number_of_evaluations"]
                ),
                "best_route": json.dumps(
                    result["best_route"]
                ),
                "cost_history": json.dumps(
                    result["cost_history"]
                )
            }

            writer.writerow(row)

    return output_file


def save_summary_results(
    summary,
    experiment_config,
    output_file
):
    output_file = Path(output_file)
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        *experiment_config.keys(),
        "best_run",
        "best_ga_seed",
        "best_cost",
        "worst_cost",
        "mean_cost",
        "median_cost",
        "cost_standard_deviation",
        "mean_execution_time",
        "mean_improvement_percentage",
        "number_of_evaluations",
        "best_route"
    ]

    best_run = summary["best_run"]

    row = {
        **experiment_config,
        "best_run": best_run["run"],
        "best_ga_seed": best_run["ga_seed"],
        "best_cost": summary["best_cost"],
        "worst_cost": summary["worst_cost"],
        "mean_cost": summary["mean_cost"],
        "median_cost": summary["median_cost"],
        "cost_standard_deviation": (
            summary["cost_standard_deviation"]
        ),
        "mean_execution_time": (
            summary["mean_execution_time"]
        ),
        "mean_improvement_percentage": (
            summary["mean_improvement_percentage"]
        ),
        "number_of_evaluations": (
            best_run["number_of_evaluations"]
        ),
        "best_route": json.dumps(
            best_run["best_route"]
        )
    }

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerow(row)

    return output_file