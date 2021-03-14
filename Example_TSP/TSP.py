from Genetic.SingleObjectiveAlgorithms import *
import random
import math


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(A, B):
        return math.sqrt(math.pow(A.x - B.x, 2) + math.pow(A.y - B.y, 2))


class Path(Gene):
    # class properties
    cities = []
    distance_matrix = []

    @classmethod
    def add_city(cls, new_city):
        # adding new city to cities
        cls.cities.append(new_city)
        # adding new city column
        for i in range(len(cls.cities) - 1):
            cls.distance_matrix[i].append(City.get_distance(cls.cities[i], new_city))
        # adding new city row
        cls.distance_matrix.append([])
        for i in range(len(cls.cities) - 1):
            cls.distance_matrix[-1].append(cls.distance_matrix[i][-1])
        cls.distance_matrix[-1].append(0)

    @classmethod
    def calculate_distances(cls):
        if len(cls.cities) > 0:
            cls.distance_matrix = [[-1] * len(cls.cities) for _ in range(len(cls.cities))]
            # calculate distance matrix
            for i in range(len(cls.cities)):
                for j in range(len(cls.cities)):
                    if cls.distance_matrix[j][i] == -1:
                        cls.distance_matrix[i][j] = City.get_distance(cls.cities[i], cls.cities[j])
                    else:
                        cls.distance_matrix[i][j] = cls.distance_matrix[j][i]

    @classmethod
    def create_random(cls):
        gene = list(range(len(cls.cities)))
        random.shuffle(gene)
        return Path(gene)

    def __init__(self, order):
        self.order = order

    def mutate(self):
        OrderedGene.Mutate.single_swap(self.order)

    @staticmethod
    def crossover(parent_a: 'Path', parent_b: 'Path'):
        child_a, child_b = OrderedGene.Crossover.single_point(parent_a.order, parent_b.order, Path.cities)
        return Path(child_a), Path(child_b)

    def calculate_fitness(self):
        if len(self.order) >= 2:
            d = 0
            for j in range(len(self.order)):
                d += Path.distance_matrix[self.order[j]][self.order[(j + 1) % len(self.order)]]
            return 1 / d
        else:
            return 1

    def calculate_distance(self):
        d = 0
        for j in range(len(self.order)):
            d += Path.distance_matrix[self.order[j]][self.order[(j + 1) % len(self.order)]]
        return d


def get_tsp_pool(population_size):
    return GenePool(Path, population_size, mutation_rate=0.05, crossover_rate=1, select_func=Selection.get_tournament(tournament_size=5))
