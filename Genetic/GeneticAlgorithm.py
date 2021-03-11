import random
from abc import ABC, abstractmethod
from typing import Callable, List


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
    def calculate_fitness(self) -> float:
        """
        calculate fitness of gene.

        :return: fitness
        """
        pass


class OrderedGene:
    """ Crossover and Mutation function for ordered genes."""

    class Crossover:
        """ Collection of crossover functions for ordered genes."""

        @staticmethod
        def single_point(parent_a: List, parent_b: List, items: List) -> (List, List):
            """
            copies gene of one parent upto a random point and rest in order of other parent.

            :param parent_a: First Parent gene
            :param parent_b: Second Parent gene
            :param items: List of items in a ordered genes.
            :return: Two children gene of parent genes
            """
            x = random.randint(0, len(items))
            child_a = parent_a[:x]
            child_b = parent_b[:x]
            for i in parent_b:
                if i not in child_a:
                    child_a.append(i)
            for i in parent_a:
                if i not in child_b:
                    child_b.append(i)
            return child_a, child_b

    class Mutate:
        @staticmethod
        def single_swap(gene: List) -> None:
            """
            Swap a random point of gene with another random part.

            :param gene: gene to be mutated.
            :return: None
            """
            a = random.randint(0, len(gene) - 1)
            b = random.randint(0, len(gene) - 1)
            gene[a], gene[b] = gene[b], gene[a]


class Selection:
    """ Collection of selection algorithms."""

    @staticmethod
    def proportionate(population: List[Gene], fitness: List[float], selection_size: int) -> List[Gene]:
        """
        select a population of selection_size proportional to fitness.
        Note: it may not work if fitness*selection_size is 0 for some genes . if the 
        function fails to select enough genes it will choose randomly.

        :param population: list of genes in population.
        :param fitness: list of fitness of genes in same order of population (sum should be normalized to 1).
        :param selection_size: size of population to be selected.
        :return: selected list of genes.
        """
        selected = []
        for i in range(len(population)):
            p = int(round(fitness[i] * selection_size))
            for j in range(p):
                selected.append(population[i])
        while len(selected) < selection_size:
            selected.append(population[random.randint(0, len(population) - 1)])
        return selected[:selection_size]

    @staticmethod
    def roulette_wheel(population: List[Gene], fitness: List[float], selection_size: int) -> List[Gene]:
        """
        select a population of selection_size by creating a roulette wheel made according to fitness.

        :param population: list of genes in population.
        :param fitness: list of fitness of genes in same order of population (sum should be normalized to 1).
        :param selection_size: size of population to be selected.
        :return: selected list of genes.
        """
        selected = []
        for j in range(selection_size):
            x = random.random()
            s = 0
            for i in range(len(population)):
                s += fitness[i]
                if x < s:
                    selected.append(population[i])
                    break
            else:
                selected.append(population[-1])
        return selected

    @staticmethod
    def ranked(population: List[Gene], fitness: List[float], selection_size: int) -> List[Gene]:
        """
        select a population of selection_size ranked according to fitness.

        :param population: list of genes in population.
        :param fitness: list of fitness of genes in same order of population (sum should be normalized to 1).
        :param selection_size: size of population to be selected.
        :return: selected list of genes.
        """
        sorted_fitness, sorted_population = list(zip(*sorted(zip(fitness, population), key=lambda pair: -pair[0])))
        ranks = []
        prev_fitness = 1
        prev_rank = 0

        for i in range(len(sorted_fitness)):
            if prev_fitness > sorted_fitness[i]:
                ranks.append(prev_rank + 1)
                prev_fitness = sorted_fitness[i]
                prev_rank = prev_rank + 1
            else:
                ranks.append(prev_rank)

        max_rank = max(ranks)
        inverse_rank = [max_rank - r + 1 for r in ranks]
        sum_inverse_rank = sum(inverse_rank)
        normalized_inverse_rank = [i / sum_inverse_rank for i in inverse_rank]
        selected = Selection.roulette_wheel(sorted_population, normalized_inverse_rank, selection_size)
        return selected

    @staticmethod
    def get_tournament(tournament_size: int = 1) -> Callable[[List[Gene], List[float], int], List[Gene]]:
        """
        returns an tournament based selection function.

        :param tournament_size: size of tournament. (1 means random selection.)
        :return: selection function.
        """

        def tournament_inner(population: List[Gene], fitness: List[float], selection_size: int) -> List[Gene]:
            """
            select a population of selection_size with tournament on basis of fitness.

            :param population: list of genes in population.
            :param fitness: list of fitness of genes in same order of population (sum should be normalized to 1).
            :param selection_size: size of population to be selected.
            :return: selected list of genes.
            """
            selected = []
            for i in range(selection_size):
                tournament_list = random.choices(list(range(len(population))), k=tournament_size)
                winner = population[tournament_list[0]]
                max_fitness = fitness[tournament_list[0]]
                for j in tournament_list:
                    if fitness[j] >= max_fitness:
                        max_fitness = fitness[j]
                        winner = population[j]
                selected.append(winner)
            return selected

        return tournament_inner


class GenePool:
    def __init__(self, gene_type, population_size: int, mutation_rate: float = 0.1, crossover_rate: float = 1,
                 select_func: Callable[[List[Gene], List[float], int], List[Gene]] = Selection.roulette_wheel):
        """
        Create a gene pool.

        :param gene_type: type of gene.
        :param population_size: size of population.
        :param mutation_rate: rate of mutation.
        :param crossover_rate: rate of crossover.
        :param select_func: function to select.
        """
        self.population_size = population_size
        self.population = []
        self.fitness = []
        self.gene_type = gene_type
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.select_func = select_func

    def initialize_population(self) -> None:
        """
        Initialize population with random genes.

        :return: None
        """
        self.population = []
        for i in range(self.population_size):
            self.population.append(self.gene_type.create_random())
        # evaluate
        fitness = []
        for i in self.population:
            fitness.append(i.calculate_fitness())
        sum_fitness = sum(fitness)
        normalized_fitness = [i / sum_fitness for i in fitness]
        self.fitness = normalized_fitness

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
        selected = self.select_func(self.population, self.fitness, self.population_size)

        # crossover
        new_population = self.crossover(selected)

        # mutation
        self.mutate(new_population)
        self.population = new_population

        # evaluate
        self.fitness = GenePool.evaluate(new_population)

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
    def evaluate(population: List[Gene]) -> List[float]:
        """
        Evaluate the fitness of population.

        :param population: population to evaluate
        :return: normalized fitness.
        """
        fitness = []
        for i in population:
            fitness.append(i.calculate_fitness())
        sum_fitness = sum(fitness)
        normalized_fitness = [i / sum_fitness for i in fitness]
        return normalized_fitness

    def get_population(self) -> List[Gene]:
        """
        get population of current generation.

        :return: population
        """
        return self.population

    def get_fitness(self) -> List[float]:
        """
        get fitness of current generation.

        :return: fitness
        """
        return self.fitness

    def get_best_index(self) -> int:
        """
        get index of best gene of the generation.

        :return: best index
        """
        return self.fitness.index(max(self.fitness))

    def get_best_gene(self) -> Gene:
        """
        get best gene of the generation.

        :return: best gene
        """
        ind = self.get_best_index()
        return self.population[ind]

    def get_best_fitness(self) -> float:
        """
        get fitness of best gene of the generation.

        :return: fitness of best gene of the generation.
        """
        ind = self.get_best_index()
        return self.fitness[ind]
