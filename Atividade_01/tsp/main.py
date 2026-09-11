from pathlib import Path
import instance

def main():
    number_of_cities = 25
    instance_seed = "TSP"

    project_directory = Path(__file__).resolve().parent.parent
    data_directory = project_directory / "data"
    output_file = data_directory / "tsp_sample.csv"

    data_directory.mkdir(parents=True, exist_ok=True)

    print("Generating the TSP instance...")

    cities = instance.generate_tsp(
        n=number_of_cities,
        seed=instance_seed
    )

    instance.save_tsp(
        cities=cities,
        filename=output_file
    )

    print(f"Instance generated with {len(cities)} cities.")
    print(f"Instance saved to: {output_file}")


if __name__ == "__main__":
    main()