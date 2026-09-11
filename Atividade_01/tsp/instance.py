import csv
import random

def generate_tsp(n, seed, coordinate_min=0, coordinate_max=1000):
    if n <= 0:
        raise ValueError("A quantidade de cidades deve ser maior que zero.")

    available_positions = (coordinate_max - coordinate_min + 1) ** 2

    if n > available_positions:
        raise ValueError(
            "A quantidade de cidades é maior que o número de coordenadas disponíveis."
        )

    rng = random.Random(seed)

    cities = []
    used_coordinates = set()

    for city_id in range(n):
        while True:
            x = rng.randint(coordinate_min, coordinate_max)
            y = rng.randint(coordinate_min, coordinate_max)

            coordinate = (x, y)

            if coordinate not in used_coordinates:
                used_coordinates.add(coordinate)

                city = {
                    "id": city_id,
                    "x": x,
                    "y": y
                }

                cities.append(city)
                break

    return cities


def save_tsp(cities, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "x", "y"]
        )

        writer.writeheader()
        writer.writerows(cities)

        
def load_tsp(filename):
    cities = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            city = {
                "id": int(row["id"]),
                "x": int(row["x"]),
                "y": int(row["y"])
            }

            cities.append(city)

    return cities