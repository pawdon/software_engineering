import random
from .greedy_optimizer_file import GreedyOptimizer, ShipmentsManager, Shipment
from .genetic_population_file import GeneticIndividual, GeneticPopulation


class GeneticOptimizer(GreedyOptimizer):
    """
    A genetic optimize class.
    """
    def __init__(self):
        super().__init__()
        self.generation_numbers = 10
        self.base_population_size = 40
        self.survivors_nr = 20
        self.mutation_probability = 0.1
        self.shuffle_len = -1

    @staticmethod
    def info():
        """
        Return a string with information describing the optimizer.
        :return: a string with information describing the optimizer
        """
        return "Genetic optimizer"

    def process_generation(self, genetic_population, check_urgent_containers, main_timestamp):
        """
        Process a single generation of genetic algorithm.
        :param genetic_population: a population of individuals of genetic algorithm
        :param check_urgent_containers: (bool) if True, check timestamps of containers
        :param main_timestamp: a main timestamp
        :return: None
        """
        for individual in genetic_population.population:
            if individual.value == 0:
                if individual.sorting_opt == 0:
                    if_sort_by_width = False
                elif individual.sorting_opt == 1:
                    if_sort_by_width = True
                else:
                    if_sort_by_width = bool(random.getrandbits(1))
                correct = super().optimize_single_shipment(individual.shipment, individual.containers,
                                                           check_urgent_containers, main_timestamp, if_sort_by_width)
                individual.set_alive(correct)
                if correct:
                    individual.evaluate()
        genetic_population.next_generation()

    def optimize_single_shipment(self, shipment, sorted_containers,
                                 check_urgent_containers=False,
                                 main_timestamp=None,
                                 if_sort_by_width=False):
        """
        Place containers on a single ship in an optimal way using a genetic algorithm.
        :param shipment: a shipment with a ship
        :param sorted_containers: a sorted list of containers
        :param check_urgent_containers: (bool) if True, check timestamps of containers
        :param main_timestamp: a main timestamp
        :param if_sort_by_width: (bool) if True, sort empty points by width, else sort them by length
        :return: a shipment with containers
        """

        genetic_population = GeneticPopulation(timestamp=self.timestamp,
                                               base_population_size=self.base_population_size,
                                               survivors_nr=self.survivors_nr,
                                               mutation_probability=self.mutation_probability,
                                               shuffle_len=self.shuffle_len)
        genetic_population.generate_initial_population(sorted_containers, shipment)

        self.report_generator.increase_indent()
        self.report_generator.log(f"Genetic algorithm for ship {shipment.ship}")
        self.report_generator.increase_indent()
        for i in range(self.generation_numbers):
            self.report_generator.log(f"Generation {i + 1}/{self.generation_numbers}")
            self.process_generation(genetic_population, check_urgent_containers, main_timestamp)
        correct = [individual for individual in genetic_population.population if individual.alive]
        bests = [individual for individual in correct if individual.value == correct[0].value]
        self.report_generator.log(f"{len(correct)} correct individuals")
        self.report_generator.log(f"{len(correct)} bests individuals")
        self.report_generator.decrease_indent()
        self.report_generator.decrease_indent()

        if len(bests) > 0:
            winner = random.choice(bests)
        else:
            winner = genetic_population.population[0]
        shipment.load(winner.shipment)
        return winner.alive
