import random
from .genetic_individual_file import GeneticIndividual
import sys


class GeneticPopulation:
    """
    A class of a population of individuals of genetic algorithm
    """
    def __init__(self, timestamp, base_population_size=20, survivors_nr=10, mutation_probability=0.1, shuffle_len=8):
        """
        Constructor
        :param timestamp: a main timestamp
        :param base_population_size: a size of an initial population
        :param survivors_nr: a number of individuals that survive after every generation
        :param mutation_probability: a probability of mutation
        :param shuffle_len: a length od sublists to shuffle (see shuffle_list() for more details)
        """
        self.timestamp = timestamp
        self.population = []
        self.base_population_size = base_population_size
        self.survivors_nr = survivors_nr
        self.mutation_probability = mutation_probability
        self.shuffle_len = shuffle_len

    def split_containers_list(self, containers_list):
        """
        Split containers according to timestamps.
        :param containers_list: a list of containers
        :return: a tuple (a list of containers with previous timestamps, a list of containers with current timestamps)
        """
        previous_containers = []
        current_containers = []
        for container in containers_list:
            if container.timestamp < self.timestamp:
                previous_containers.append(container)
            else:
                current_containers.append(container)
        return previous_containers, current_containers

    def shuffle_list(self, containers_list):
        """
        Divide a list of containers to lists with a length self.shuffle_len and shuffle every sublist.
        If self.shuffle_len == -1, do not divide the list.
        :param containers_list: a non-shuffled list of containers
        :return: a shuffled list of containers
        """
        shuffle_len = self.shuffle_len if self.shuffle_len > 0 else len(containers_list)
        shuffled = []
        list_len = len(containers_list)
        start = 0
        stop = shuffle_len
        while start < list_len:
            sub = containers_list[start:stop]
            random.shuffle(sub)
            shuffled.extend(sub)
            start = stop
            stop += shuffle_len
        return shuffled

    def get_rand_ordered_list(self, previous_containers, current_containers):
        """
        previous_copy = previous_containers.copy()
        current_copy = current_containers.copy()
        random.shuffle(previous_copy)
        random.shuffle(current_copy)
        return previous_copy + current_copy
        """
        return self.shuffle_list(previous_containers) + self.shuffle_list(current_containers)

    def generate_initial_population(self, containers_list, shipment):
        """
        Generate an initial population.
        :param containers_list: a list of containers
        :param shipment: a shipment
        :return:
        """
        self.population.append(GeneticIndividual(containers_list.copy(), shipment.copy(only_ship=True), sorting_opt=0))
        self.population.append(GeneticIndividual(containers_list.copy(), shipment.copy(only_ship=True), sorting_opt=1))
        self.population.append(GeneticIndividual(containers_list.copy(), shipment.copy(only_ship=True), sorting_opt=2))
        previous_containers, current_containers = self.split_containers_list(containers_list)
        for _ in range(self.base_population_size - 1):
            self.population.append(GeneticIndividual(self.get_rand_ordered_list(previous_containers, current_containers),
                                                     shipment.copy(only_ship=True),
                                                     sorting_opt=random.choice([0, 1, 2])))

    def selection(self):
        """
        Process selection. Kill weak individuals.
        :return:
        """
        self.population.sort(key=lambda x: x.value, reverse=True)
        self.population = self.population[0:self.survivors_nr]

    @staticmethod
    def add_gene(parent, child, ind, genes_length):
        """
        Add a single gene of parent to a child.
        :param parent: a parent individual
        :param child: a child individual
        :param ind: an index of a parent gene
        :param genes_length: a length of genes
        :return: a new index of a parent gene
        """
        gene_added = False
        while not gene_added and ind < genes_length:
            gene = parent.containers[ind]
            if gene not in child.containers:
                child.containers.append(gene)
            ind += 1
        return ind

    def cross(self, mother, father):
        """
        Cross 2 individuals.
        :param mother: the first individual
        :param father: the second individual
        :return: a new individual
        """
        containers_nr = len(mother.containers)
        child = mother.copy()
        child.containers = []
        mother_ind = 0
        father_ind = 0

        child.sorting_opt = random.choice([mother.sorting_opt, father.sorting_opt])
        while mother_ind < containers_nr and father_ind < containers_nr:
            if random.random() < 0.5:
                mother_ind = self.add_gene(mother, child, mother_ind, containers_nr)
            else:
                father_ind = self.add_gene(father, child, father_ind, containers_nr)

        if len(child.containers) != containers_nr:  # TODO remove
            print("ERROR IN CROSSOVER")
            sys.exit(1)
        return child

    def crossover(self):
        """
        Process crossover among individuals in population.
        :return:
        """
        for _ in range(self.base_population_size - self.survivors_nr):
            mother_nr = random.randint(0, self.survivors_nr - 1)
            father_nr = mother_nr
            while father_nr == mother_nr:
                father_nr = random.randint(0, self.survivors_nr - 1)
            self.population.append(self.cross(mother=self.population[mother_nr],
                                              father=self.population[father_nr]))

    @staticmethod
    def mutate(original_individual):
        """
        Mutate a single individual.
        :param original_individual: an individual to mutate
        :return: a new individual
        """
        new_individual = original_individual.copy()
        containers_nr = len(new_individual.containers)
        old_position = random.randint(0, containers_nr - 1)
        new_position = random.randint(0, containers_nr - 1)
        container = new_individual.containers[old_position]
        new_individual.containers.remove(container)
        new_individual.containers.insert(new_position, container)

        new_individual.sorting_opt = random.choice([0, 1, 2])
        return new_individual

    def mutation(self):
        """
        Process a random mutation.
        :return:
        """
        for i in range(self.survivors_nr):
            individual = self.population[i]
            if random.random() < self.mutation_probability:
                self.population.append(self.mutate(individual))

    def next_generation(self):
        """
        Process a single generation: selection, crossover and mutation.
        :return:
        """
        self.selection()
        self.crossover()
        self.mutation()


if __name__ == "__main__":
    pass
