import csv
import json
from pathlib import Path


def save_raw_results(
    grouped_results,
    experiment_config,
    output_file
):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        *experiment_config.keys(),
        "run",
        "operator",
        "route_seed",
        "sa_seed",
        "initial_cost",
        "best_cost",
        "improvement_percentage",
        "execution_time",
        "best_route"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for operator_name, operator_results in grouped_results:
            for run_result in operator_results:
                row = {
                    **experiment_config,
                    **run_result,
                    "operator": operator_name,
                    "best_route": json.dumps(
                        run_result["best_route"]
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
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        *experiment_config.keys(),
        "operator",
        "best_run",
        "best_route_seed",
        "best_sa_seed",
        "best_cost",
        "worst_cost",
        "mean_cost",
        "median_cost",
        "cost_standard_deviation",
        "mean_execution_time",
        "mean_improvement_percentage",
        "best_route"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for summary_entry in summary:
            best_run = summary_entry["best_run"]

            row = {
                **experiment_config,
                "operator": summary_entry["operator"],
                "best_run": best_run["run"],
                "best_route_seed": best_run["route_seed"],
                "best_sa_seed": best_run["sa_seed"],
                "best_cost": summary_entry["best_cost"],
                "worst_cost": summary_entry["worst_cost"],
                "mean_cost": summary_entry["mean_cost"],
                "median_cost": summary_entry["median_cost"],
                "cost_standard_deviation": (
                    summary_entry["cost_standard_deviation"]
                ),
                "mean_execution_time": (
                    summary_entry["mean_execution_time"]
                ),
                "mean_improvement_percentage": (
                    summary_entry["mean_improvement_percentage"]
                ),
                "best_route": json.dumps(
                    best_run["best_route"]
                )
            }

            writer.writerow(row)

    return output_file