from math import ceil
import random
from .batch_gerrymander import batch_gerrymander

def score_solution(original: list[list[int]], solution: list[list[tuple[int,int]]]) -> int:
    """Returns the score of the current solution. The score function is a penalty that must be minimized."""
    return votes_score(original, solution) + size_score(solution) + distance_score(solution)


def votes_score(original: list[list[int]], solution: list[list[tuple[int,int]]]) -> int:
    """Calculates the part of the score associated to lost districts. 
    It is 5 times the square of the number of lost districts."""
    lost_districts = 0
    for district in solution:
        sum = 0
        for city in district:
            sum += original[city[0]][city[1]]
        if sum <= 500*len(district):
            lost_districts += 1
    return 5 * lost_districts**2


def size_score(solution: list[list[tuple[int,int]]]) -> int:
    """Calculates the part of the score associated to districts having the wrong size.
    It is the square of the difference between the wanted number of cities and the 
    current number of cities in a given district."""
    n = len(solution)
    size_penality = 0
    for district in solution:
        size_penality += (len(district)-n)**2
    return size_penality


def distance_score(solution: list[list[tuple[int,int]]]) -> int:
    """Calculates the part of the score associated to the distance between cities in a district.
    It is the mean square distance between each city and every other city in its district."""
    distance_score = 0
    n = len(solution)
    for district in solution:
        for i,city in enumerate(district):
            for j in range(i+1, len(district)):
                distance_score += (max(0, distance_manhattan(city, district[j])-ceil(n/2)))**2
    return distance_score/len(solution)


def distance_manhattan(city_a: tuple[int,int], city_b: tuple[int,int]) -> int:
    return abs(city_a[0] - city_b[0]) + abs(city_a[1] - city_b[1])

def random_disctricts(state: list[list[int]]) -> list[list[tuple[int,int]]]:
    """This function generates uniformly randomly n non-empty districts."""
    
    n = len(state)
    cities = [(i,j) for i in range(n) for j in range(n)]
    random.shuffle(cities)
    districts = [[] for _ in range(n)]
    
    # No district remains empty
    for i, city in enumerate(cities[:n]):
        districts[i].append(city)
    
    # Random districting
    for city in cities[n:]:
        i = random.randint(0, n-1)
        districts[i].append(city)
    
    return districts


def preprocess_solution(state: list[list[int]], initial_districts: list[list[tuple[int,int]]]):
    """This function preprocesses initial districts and returns what would be used for improving the districts."""
    
    n = len(state)

    district_city_dict = {idx: set(district) for idx, district in enumerate(initial_districts)}

    city_district_dict = {city: idx for idx in range(n) for city in initial_districts[idx]}

    district_votes = {idx: sum([state[city[0]][city[1]] for city in district]) for idx, district in enumerate(initial_districts)}

    num_lost_districts = sum([district_votes[idx] <= 500 * len(district) for idx, district in enumerate(initial_districts)])

    return district_city_dict, city_district_dict, district_votes, num_lost_districts


def post_process(state, district_city_dict):
    """This function reconstructs the districts after the improvement to the preprocessed variables."""

    final_districts = []
    for idx in range(len(district_city_dict)):
        final_districts.append(list(district_city_dict[idx]))

    return final_districts


def city_redistricting_cost(city, target_idx, state):
    """This function calculates the net cost of moving city to the district indexed by target_idx."""

    current_idx = city_district_dict[city]
    if target_idx == current_idx:
        return 0

    n = len(state)
    i,j = city

    city_vote = state[i][j]
    current_size = len(district_city_dict[current_idx])
    target_size = len(district_city_dict[target_idx])

    # vote net cost
    districts_lost_diff = 0
    if (district_votes[target_idx] <= 500 * target_size and district_votes[target_idx] + city_vote > 500 * (target_size + 1))\
        or (district_votes[current_idx] <= 500 * current_size and district_votes[current_idx] - city_vote > 500 * (current_size - 1)):
        districts_lost_diff -= 1
    if (district_votes[current_idx] > 500 * current_size and district_votes[current_idx] - city_vote <= 500 * (current_size - 1))\
        or (district_votes[target_idx] > 500 * target_size and district_votes[target_idx] + city_vote <= 500 * (target_size + 1)):
        districts_lost_diff += 1
    
    vote_cost = 5 * ((num_lost_districts + districts_lost_diff)**2 - num_lost_districts**2)

    # size net cost
    size_cost = 2 * (target_size - current_size + 1) # math jujutsu alert

    # distance net cost
    city_current_distance_contribution = 1 / n * sum([max(0, distance_manhattan(city, other_city) - ceil(n/2)) ** 2
                                                      for other_city in district_city_dict[current_idx]])
    city_target_distance_contribution = 1 / n * sum([max(0, distance_manhattan(city, other_city) - ceil(n/2)) ** 2
                                                     for other_city in district_city_dict[target_idx]])
    distance_cost = city_target_distance_contribution - city_current_distance_contribution

    return size_cost + vote_cost + distance_cost


def move_city(city, target_idx, state):
    """This function moves city to the district indexed by target_idx and updates all relevant variables accordingly."""
    current_idx = city_district_dict[city]

    if current_idx == target_idx: # Moot point
        return

    current_size = len(district_city_dict[current_idx])
    target_size = len(district_city_dict[target_idx])
    i, j = city[0], city[1]
    city_vote = state[i][j]

    # Update district_city_dict
    district_city_dict[current_idx].remove(city)
    district_city_dict[target_idx].add(city)
    
    # Update city_district_dict
    city_district_dict[city] = target_idx
    
    # Update num_lost_districts
    global num_lost_districts
    if (district_votes[target_idx] <= 500 * target_size and district_votes[target_idx] + city_vote > 500 * (target_size + 1))\
        or (district_votes[current_idx] <= 500 * current_size and district_votes[current_idx] - city_vote > 500 * (current_size - 1)):
        num_lost_districts -= 1
    if (district_votes[current_idx] > 500 * current_size and district_votes[current_idx] - city_vote <= 500 * (current_size - 1))\
        or (district_votes[target_idx] > 500 * target_size and district_votes[target_idx] + city_vote <= 500 * (target_size + 1)):
        num_lost_districts += 1
    
    # Update district_votes
    district_votes[current_idx] -= city_vote
    district_votes[target_idx] += city_vote


def improve_attempt(city, target_idx, state):
    """This function moves city to the district indexed by target_idx if the net cost of the move is negative."""
    cost = city_redistricting_cost(city, target_idx, state)    
    if cost < 0:
        move_city(city, target_idx, state)


def random_neighbor(city, state):
    """This function selects a quasi-neighbor of city uniformly randomly.
    A quasi-neighbor is a city whose Manhattan distance to the original city is at most 3.
    """
    row, col = city
    n = len(state)
    neighbors = [
        (row + dr, col + dc)
        for dr in range(-3, 4)
        for dc in range(-3, 4)
        if abs(dr) + abs(dc) <= 3 and 0 <= row + dr < n and 0 <= col + dc < n
    ]
    return random.choice(neighbors)


def improve(state, districts, max_iter):
    """This function performs max_iter improvement attempts. The attempts are not unique."""
    n = len(state)
    for _ in range(max_iter):
        city = (random.randint(0, n-1), random.randint(0, n-1))
        target_idx = city_district_dict[random_neighbor(city, state)]
        improve_attempt(city, target_idx, state)


def iterate_from_random(state, max_attempts, max_iter):
    """This function generates max_attempt random initialization and attempts max_iter times to improve each of them.
    At the end it returns the best solution it finds.
    """
    best_score = float('inf')
    initial_districts = random_disctricts(state)
    districts = initial_districts.copy()
    for _ in range(max_attempts):
        global district_city_dict, city_district_dict, district_votes, num_lost_districts
        district_city_dict, city_district_dict, district_votes, num_lost_districts = preprocess_solution(state, initial_districts)
        improve(state, initial_districts, max_iter)
        improved_districts = post_process(state, district_city_dict)
        current_score = score_solution(state, improved_districts)
        if current_score < best_score:
            districts = improved_districts.copy()
            best_score = current_score
        initial_districts = random_disctricts(state)
    return districts


def iterate_from_batch_gerrymander(state, buffer_min_lengths=range(1,6), max_iter=1000):
    """This function generates several initializations using the gerrymader() equipped with various buffer lengths.
    It then attempts max_iter times to improve each of them, and finally returns the best solution it finds.
    """

    best_score = float('inf')
    for buffer_min_length in buffer_min_lengths:
        initial_districts = batch_gerrymander(state, buffer_min_length)
        global district_city_dict, city_district_dict, district_votes, num_lost_districts
        district_city_dict, city_district_dict, district_votes, num_lost_districts = preprocess_solution(state, initial_districts)
        improve(state, initial_districts, max_iter)
        improved_districts = post_process(state, district_city_dict)
        current_score = score_solution(state, improved_districts)
        if current_score < best_score:
            districts = improved_districts.copy()
            best_score = current_score

    return districts


def gerrymander(state):
    """This function gerrymanders the states and returns the districts."""
    n = len(state)

    if n <= 320:
        max_attempts = 100 if n <= 12 else 0
        if max_attempts > 0:
            from_random_districts = iterate_from_random(state, max_attempts=max_attempts, max_iter=20000)
            from_random_score = score_solution(state, from_random_districts)
        else:
            from_random_score = float('inf')

        step = 1 if n <= 50 else 2 if n <= 150 else 3
        max_iter = 100000 if n < 16 else 50000 if n < 32 else 25000 if n < 64 else 1000
        from_batch_gerrymander_districts = iterate_from_batch_gerrymander(state, buffer_min_lengths=range(max(1, n // 16), min(40, n * (n//4 + 1) + 1), step), max_iter=max_iter)
        from_batch_gerrymander_score = score_solution(state, from_batch_gerrymander_districts)

        return from_batch_gerrymander_districts if from_batch_gerrymander_score < from_random_score else from_random_districts

    else:
        return batch_gerrymander(state)
