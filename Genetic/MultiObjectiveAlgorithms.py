import math
import random
from abc import ABC, abstractmethod
from typing import List


class Gene(ABC):
    """
    Gene is template to make a genotype of the solution.
    """

    @classmethod
    @abstractmethod
    def create_random(cls) -> 'Gene':
        """
        Create a gene with random data.

        :return: a gene with random data.
        """
        pass

    @abstractmethod
    def mutate(self) -> None:
        """
        Mutate the gene.

        :return: None
        """
        pass

    @staticmethod
    @abstractmethod
    def crossover(parent_a: 'Gene', parent_b: 'Gene') -> ('Gene', 'Gene'):
        """
        Crossover between parent genes.

        :param parent_a: First Parent gene
        :param parent_b: Second Parent gene
        :return: Two children gene of parent genes
        """
        pass

    @abstractmethod
    def calculate_fitness(self) -> List[float]:
        """
        calculate fitness of gene.

        :return: fitness
        """
        pass


class GeneWrapper:
    """ Wrapper for gene in a population."""

    def __init__(self, gene: Gene):
        self.gene = gene
        self.fitness = gene.calculate_fitness()
        self.rank = 0
        self.cDist = 0

    def __eq__(self, other):
        return self.rank == other.rank and self.cDist == other.cDist

    def __lt__(self, other):
        return self.rank > other.rank or (self.rank == other.rank and self.cDist < self.cDist)

    def __gt__(self, other):
        return self.rank < other.rank or (self.rank == other.rank and self.cDist > self.cDist)

    @staticmethod
    def dominates(p: 'GeneWrapper', q: 'GeneWrapper') -> bool:
        """
        Returns  if p dominates q.

        :param p: List of fitness of solution p.
        :param q: List of fitness of solution q (in same order as of p).
        :return: if p dominates q.
        """
        length = min(len(p.fitness), len(q.fitness))
        for i in range(length):
            if p.fitness[i] < q.fitness[i]:
                return False
        for i in range(length):
            if p.fitness[i] > q.fitness[i]:
                return True
        return False


def fast_non_dominated_sort(genes: List[GeneWrapper]) -> List[List[GeneWrapper]]:
    """
    Returns non dominated sorted front(list of index of solutions that are non dominating to each other) of solutions in increasing order of ranks.

    :param genes: List of gene wrappers.
    :return: list of fronts.
    """
    pop_len = len(genes)
    S = [set() for _ in range(pop_len)]  # solutions dominated by gene(solution) at that index.
    N = [0 for _ in range(pop_len)]  # number of solutions dominating gene(solution) at that index.
    F = []  # solution fronts
    F_0 = []  # zeroth front
    r = 1
    for i in range(pop_len):
        for j in range(pop_len):
            if GeneWrapper.dominates(genes[i], genes[j]):
                S[i].add(j)
            elif GeneWrapper.dominates(genes[j], genes[i]):
                N[i] += 1
        if N[i] == 0:
            genes[i].rank = r
            F_0.append(i)
    F.append(F_0)
    F_i = F_0
    while F_i:
        H = []
        r += 1
        for i in F_i:
            for j in S[i]:
                N[j] -= 1
                if N[j] == 0:
                    H.append(j)
                    genes[j].rank = r
        F_i = H
        if F_i:
            F.append(F_i)
    fronts = []
    for i in F:
        t = []
        for j in i:
            t.append(genes[j])
        fronts.append(t)

    return fronts


def crowding_distance_assignment(front: List[GeneWrapper]) -> None:
    """
    crowding distance for the front.

    :param front: front.
    :return: None.
    """
    for i in range(len(front[0].fitness)):
        front.sort(key=lambda x: x.fitness[i])
        front[0].cDist = math.inf
        front[-1].cDist = math.inf
        for j in range(1, len(front) - 1):
            front[j].cDist += abs(front[j + 1].fitness[i] - front[j - 1].fitness[i])


class NonDominatedGenePool:
    def __init__(self, gene_type, population_size: int, tournament_fraction: float = 0.1,
                 mutation_rate: float = 0.1, crossover_rate: float = 1):
        """
        Create a gene pool.

        :param gene_type: type of gene.
        :param population_size: size of population.
        :param tournament_fraction: faction of population as size of tournament.
        :param mutation_rate: rate of mutation.
        :param crossover_rate: rate of crossover.
        """
        self.tournament_fraction = tournament_fraction
        self.population_size = population_size
        self.population = []
        self.fronts = []
        self.wrappers = []
        self.gene_type = gene_type
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def initialize_population(self) -> None:
        """
        Initialize population with random genes.

        :return: None
        """
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.gene_type.create_random())
        # evaluate
        self.wrappers = NonDominatedGenePool.evaluate(self.population)

    def generate(self) -> None:
        """
        generate next population.
        1. selection
        2. crossover
        3. mutate
        4. evaluate

        :return: None
        """
        # selection
        selected = self.select(self.wrappers, self.population_size)

        # crossover
        new_population = self.crossover(selected)

        # mutation
        self.mutate(new_population)
        new_population = self.population + new_population

        # evaluate
        wrappers = NonDominatedGenePool.evaluate(new_population)
        wrappers.sort(reverse=True)

        self.population = []
        for i in wrappers[:self.population_size]:
            self.population.append(i.gene)
        self.wrappers = wrappers[:self.population_size]

    def select(self, wrappers: List[GeneWrapper], selection_size: int) -> List[Gene]:
        """
        select a population of selection_size with tournament on basis of fitness.

        :param wrappers: list of gene wrappers.
        :param selection_size: size of population to be selected.
        :return: selected list of genes.
        """
        selected = []
        for i in range(selection_size):
            tournament_list = random.choices(wrappers,
                                             k=int(len(wrappers) * self.tournament_fraction))
            winner = max(tournament_list)
            selected.append(winner.gene)
        return selected

    def crossover(self, selected_population: List[Gene]) -> List[Gene]:
        """
        Crossover the selected population.

        :param selected_population: selected population
        :return: crossed population
        """
        new_population = []
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                if random.random() <= self.crossover_rate:
                    child_a, child_b = self.gene_type.crossover(selected_population[i], selected_population[i + 1])
                    new_population.append(child_a)
                    new_population.append(child_b)
                else:
                    new_population.append(selected_population[i])
                    new_population.append(selected_population[i + 1])
            else:
                new_population.append(selected_population[i])
        return new_population

    def mutate(self, crossed_population: List[Gene]) -> None:
        """
        Mutate the population.

        :param crossed_population: list of genes to mutate.
        :return:
        """
        for i in crossed_population:
            if random.random() <= self.mutation_rate:
                i.mutate()

    @staticmethod
    def evaluate(population: List[Gene]) -> List[GeneWrapper]:
        """
        Evaluate the rank and crowding distance of population.

        :param population: population to evaluate.
        :return: list of rank and crowding distance.
        """
        wrappers = []
        for i in population:
            wrappers.append(GeneWrapper(i))
        fronts = fast_non_dominated_sort(wrappers)
        for i in fronts:
            crowding_distance_assignment(i)
        return wrappers

    def get_population(self) -> List[Gene]:
        """
        get population of current generation.

        :return: population
        """
        return self.population

    def get_fitness(self) -> List[List[float]]:
        """
        get fitness of current generation.

        :return: fitness
        """
        return [i.fitness for i in self.wrappers]

    def get_best_genes(self) -> List[Gene]:
        """
        get best genes of the generation.

        :return: best genes
        """
        front = [i.gene for i in self.wrappers if i.rank == 1]
        return front

    def get_best_fitness(self) -> List[List[float]]:
        """
        get fitness of best gene of the generation.

        :return: fitness of best gene of the generation.
        """
        front = [i.fitness for i in self.wrappers if i.rank == 1]
        return front
