import random

POPULATION_SIZE = 100

MAX_GENERATIONS = 100  

MUTATION_PROBABILITY = 0.1  

def generate_chromosome(size):
    return [random.randint(0, size - 1) for _ in range(size)]


def fitness(chromosome):
    horizontal_collisions = sum(
        [chromosome.count(queen) - 1 for queen in chromosome]
    ) / 2
    diagonal_collisions = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i + 1, n):
            dx = abs(i - j)
            dy = abs(chromosome[i] - chromosome[j])
            if dx == dy:
                diagonal_collisions += 1
    return int(maxFitness - (horizontal_collisions + diagonal_collisions))


def crossover(parent1, parent2):
    crossover_point = random.randint(0, N - 1)
    return parent1[0:crossover_point] + parent2[crossover_point:]


def mutate(chromosome):
    if random.random() < MUTATION_PROBABILITY:
        index = random.randint(0, N - 1)
        chromosome[index] = random.randint(0, N - 1)
    return chromosome


if __name__ == '__main__':
    N = int(input("Enter the value of N: "))
    population = [generate_chromosome(N) for _ in range(POPULATION_SIZE)]
    maxFitness = (N * (N - 1)) / 2

    generation = 1
    while True:
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        if fitness(population[0]) == maxFitness:
            break

        new_population = [population[0]]

        for i in range(POPULATION_SIZE - 1):
            parent1 = random.choice(population[: POPULATION_SIZE // 2])
            parent2 = random.choice(population[: POPULATION_SIZE // 2])
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        generation += 1
        if generation > MAX_GENERATIONS:
            break

    print("Solution found in generation:", generation)
    print("Solution:", population[0])
