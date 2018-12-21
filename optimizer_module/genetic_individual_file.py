class GeneticIndividual:
    """
    A class defining a single individual of genetic algorithm.
    """
    def __init__(self, containers, shipment, sorting_opt=0):
        """
        Constructor.
        :param containers: a list of containers in an unique order (a list of genes)
        :param shipment: a shipment
        :param sorting_opt: a value defining how to sort empty places in a ship (a gene)
                            if 0: sort by length
                            else if 1: sort by width
                            else: random each time if sort by length or width
        """
        self.containers = containers
        self.shipment = shipment
        self.sorting_opt = sorting_opt
        self.alive = False
        self.value = 0

    def evaluate(self):
        """
        Evaluate this individual.
        :return:
        """
        self.value = self.shipment.get_occupied_volume()

    def set_alive(self, alive):
        """
        A setter for alive.
        :param alive: (bool)
        :return:
        """
        self.alive = alive

    def copy(self):
        """
        Return a copy of this individual.
        :return: a copy of this individual
        """
        return GeneticIndividual(containers=self.containers.copy(),
                                 shipment=self.shipment.copy(only_ship=True),
                                 sorting_opt=self.sorting_opt)
