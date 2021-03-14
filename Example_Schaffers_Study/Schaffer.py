from Genetic.MultiObjectiveAlgorithms import *
import random
import math


class SchafferGene(Gene):
    def __init__(self, x):
        self.x = x
        
    @classmethod
    def create_random(cls) -> 'SchafferGene':
        return SchafferGene(random.randint(-10000, 10000))

    def mutate(self) -> None:
        r = random.randint(0, 100)
        if self.x + r <= 10000:
            self.x += r
        else:
            self.x -= r

    @staticmethod
    def crossover(parent_a: 'SchafferGene', parent_b: 'SchafferGene') -> ('SchafferGene', 'SchafferGene'):
        diff = (parent_b.x - parent_a.x)/10
        r = random.randint(1, 10)
        return SchafferGene(parent_a.x+int(r*diff)), SchafferGene(parent_a.x+int((10-r)*diff))

    def calculate_fitness(self) -> List[float]:
        return [-math.pow(self.x, 2), -math.pow(self.x-2, 2)]


def get_schaffer_pool(population_size):
    return NonDominatedGenePool(SchafferGene, population_size, mutation_rate=0.1, crossover_rate=0.8, tournament_fraction=0.1)
