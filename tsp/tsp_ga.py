import networkx as nx
import numpy as np
import random


# Function to read the adjacency matrix from a file and create a graph
def create_graph_from_adjacency_matrix(file_path) -> nx.Graph:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    adjacency_matrix = []
    for line in lines:
        row = [int(weight) for weight in line.split()]
        adjacency_matrix.append(row)

    num_nodes = len(adjacency_matrix)
    G = nx.Graph()

    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i][j] != 0:
                G.add_edge(i + 1, j + 1, weight=adjacency_matrix[i][j])

    return G

# Function that generates a given number of random solutions to the TSP
def generate_random_solutions(G: nx.Graph, number_solutions: int) -> list:
    solutions = []
    temp = list(G.nodes())

    for _ in range(number_solutions):
        np.random.shuffle(temp)
        solutions.append(temp[:])

    return solutions

# Objective function that return the length of a given solution
def objective_function(G: nx.Graph, solutions: list) -> int:
    path_weight = 0
    for i in range(len(solutions) - 1):
        x, y = solutions[i], solutions[i + 1]
        edge_data = G.get_edge_data(x, y)
        if edge_data:
            cost = edge_data['weight']
            path_weight += cost
    x, y = solutions[0], solutions[-1]
    edge_data = G.get_edge_data(x, y)
    if edge_data:
        cost = edge_data['weight']
        path_weight += cost
    return path_weight

# Selection function that return the parents for the GA
def roulette_wheel_selection(population: list, number_of_parents: int) -> list:
    total_fitness = 0
    for i in range(len(population)):
        total_fitness += population[i][1]
    relative_fitness = []
    for i in range(len(population)):
        relative_fitness.append(population[i][1] / total_fitness)
    cumulative_probability = [sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))]
    population_indices = list(range(len(population)))

    parents = []
    while len(parents) < number_of_parents:
        rand = random.random()
        for i, cp in enumerate(cumulative_probability):
            if rand <= cp and population_indices[i] not in parents:
                parents.append(population_indices[i])
                break
            
    return [population[i] for i in parents]

# Function that returns a new population based on the parents
def crossover(parents: list, population_number: int, number_of_cities: int, number_of_parents: int, crossover_rate: int) -> list:
    new_population = []
    
    while len(new_population) < population_number:
        # Select two random parents
        f_parent = parents[random.randint(0, number_of_parents - 1)][0]
        s_parent = parents[random.randint(0, number_of_parents - 1)][0]

        # Select random positions
        selected_positions = sorted(random.sample(range(number_of_cities), crossover_rate))
        # Start the first child with the positions given by the first parent, and -1 on the other positions
        f_child = [-1] * number_of_cities
        for i in selected_positions:
            f_child[i] = f_parent[i]
        
        positions_to_fill = [i for i in range(number_of_cities) if i not in selected_positions]
        # Fill the rest of the first child with data from the second parent
        s_parent_index = 0
        for i in positions_to_fill:
            while s_parent[s_parent_index] in f_child:
                s_parent_index = (s_parent_index + 1) % number_of_cities
            f_child[i] = s_parent[s_parent_index]
            s_parent_index = (s_parent_index + 1) % number_of_cities

        new_population.append(f_child)

        # Select random positions
        selected_positions = sorted(random.sample(range(number_of_cities), crossover_rate))
        # Start the second child with the positions given by the second parent, and -1 on the other positions
        s_child = [-1] * number_of_cities
        for i in selected_positions:
            s_child[i] = s_parent[i]

        positions_to_fill = [i for i in range(number_of_cities) if i not in selected_positions]
        # Fill the rest of the second child with data from the first parent
        f_parent_index = 0
        for i in positions_to_fill:
            while f_parent[f_parent_index] in s_child:
                f_parent_index = (f_parent_index + 1) % number_of_cities
            s_child[i] = f_parent[f_parent_index]
            f_parent_index = (f_parent_index + 1) % number_of_cities

        new_population.append(s_child)

    return new_population

def mutation(population: list, mutation_rate: float):
    for individual in population:
        if random.random() <= mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

def genetic_algorithm_for_tsp(G: nx.Graph, population_number: int, number_of_cities: int, number_of_parents: int, mutation_rate: float, elitism_rate: int, crossover_rate: int, number_of_iterations: int):
    # Create random solutions
    solutions = generate_random_solutions(G, population_number)
    number_of_loops = 0
    while number_of_loops < number_of_iterations:
        # Checking the distance in each solution
        length_array = []
        for i in range(population_number):
            length_array.append(tuple((solutions[i], objective_function(G, solutions[i]))))
            
        # Getting solutions as parents
        parents = roulette_wheel_selection(length_array, number_of_parents)
        length_array.sort(key=lambda a: a[1])
        # Generating a new population with ox-crossover
        solutions = crossover(parents, population_number - elitism_rate, number_of_cities, number_of_parents, crossover_rate)
        mutation(solutions, mutation_rate)
        for i in range(elitism_rate):
            solutions.append(length_array[i][0])
        number_of_loops += 1
    
    length_array = []
    for i in range(population_number):
        length_array.append(tuple((solutions[i], objective_function(G, solutions[i]))))
        
    # Getting the best solution as result
    length_array.sort(key=lambda a: a[1])
    return length_array[0]

# File path to the adjacency matrix file
file_path = 'att48_d.txt'

# Creating the graph from the adjacency matrix
G = create_graph_from_adjacency_matrix(file_path)

number_of_iterations = 480
population_number = 480
number_of_parents = 216
mutation_rate = 0.08
elitism_rate = 120
crossover_rate = 7
number_of_cities = G.number_of_nodes()

result = genetic_algorithm_for_tsp(G, population_number, number_of_cities, number_of_parents, mutation_rate, elitism_rate, crossover_rate, number_of_iterations)
print(result)
