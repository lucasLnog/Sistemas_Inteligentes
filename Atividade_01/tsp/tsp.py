import csv

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

def euclidean_distance(city_a, city_b):
    return ((city_a["x"] - city_b["x"]) ** 2 + (city_a["y"] - city_b["y"]) ** 2) ** 0.5


def create_distance_matrix(cities):
    n = len(cities)
    distance_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            distance = euclidean_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    return distance_matrix


def route_cost(route, distance_matrix):
    total_cost = 0.0

    for i in range(len(route)):
        city_a = route[i]
        city_b = route[(i + 1) % len(route)]

        total_cost += distance_matrix[city_a][city_b]

    return total_cost


def is_valid_route(route, number_of_cities):
    if len(route) != number_of_cities:
        return False

    expected_cities = set(range(number_of_cities))
    route_cities = set(route)

    return route_cities == expected_cities


def create_random_route(number_of_cities, rng):
    if number_of_cities <= 0:
        raise ValueError("The number of cities must be greater than zero.")

    cities = list(range(1, number_of_cities))
    rng.shuffle(cities)

    route = [0] + cities
    
    return route