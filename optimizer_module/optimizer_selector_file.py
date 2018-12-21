from .abstract_optimizer_file import IOptimizer
from .fast_optimizer_file import FastOptimizer
from .greedy_optimizer_file import GreedyOptimizer
from .genetic_optimizer_file import GeneticOptimizer


class OptimizerSelector:
    """
    Class used for choosing an instance of an optimizer class.
    """
    @staticmethod
    def select(nr=1):
        """
        Return an instance of an optimizer class based on a given number.
        :param nr: a number for an optimizer class (correct_algorithms_ids() return a list of correct numbers)
        :return: an instance of an optimizer class
        """
        optimizers = [IOptimizer, FastOptimizer, GreedyOptimizer, GeneticOptimizer]
        return optimizers[nr]()

    @staticmethod
    def correct_algorithms_ids():
        """
        Return a list of correct numbers for an optimizer class.
        :return: a list of correct numbers for an optimizer class
        """
        return [1, 2, 3]
