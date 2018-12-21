from .abstract_optimizer_file import IOptimizer
from .shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition
from containers_module.containers_manager_file import ContainersManager


class GreedyOptimizer(IOptimizer):
    """
    A greedy optimize class.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self.sorted_containers = None

    @staticmethod
    def info():
        """
        Return a string with information describing the optimizer.
        :return: a string with information describing the optimizer
        """
        return "Greedy optimizer"

    @staticmethod
    def prioritize_containers(c):
        """
        A function defining how to sort containers.
        :param c: a container
        :return: a tuple of arguments used for comparing containers
        """
        return c.timestamp, -(c.length * c.width)

    def optimize_single_level(self, shipment, sorted_containers, single_level=None, if_sort_by_width=False):
        """
        Place containers on a single level of a single ship in an optimal way.
        :param shipment: a shipment with a ship
        :param sorted_containers: a sorted list of containers
        :param single_level: (int) a level number where to place containers (if None, place wherever)
        :param if_sort_by_width: (bool) if True, sort empty points by width, else sort them by length
        :return: None
        """
        if single_level is None:
            single_level = shipment.get_used_levels_nr()
        for container in sorted_containers:
            self.place_container(shipment, container, single_level, if_sort_by_width)

    def optimize_single_shipment(self, shipment, sorted_containers,
                                 check_urgent_containers=False,
                                 main_timestamp=None,
                                 if_sort_by_width=False):
        """
        Place containers on a single ship in an optimal way using a greedy algorithm.
        :param shipment: a shipment with a ship
        :param sorted_containers: a sorted list of containers
        :param check_urgent_containers: (bool) if True, check timestamps of containers
        :param main_timestamp: a main timestamp
        :param if_sort_by_width: (bool) if True, sort empty points by width, else sort them by length
        :return: a shipment with containers
        """
        correct_shipment = True

        containers_copy = sorted_containers.copy()
        one_level_shipments = [shipment.copy(only_ship=True) for _ in range(shipment.levels_nr)]
        one_level_used = [False for _ in range(shipment.levels_nr)]
        for sh in one_level_shipments:
            self.optimize_single_level(sh, containers_copy, single_level=0, if_sort_by_width=if_sort_by_width)
            for cont in sh.get_all_containers():
                containers_copy.remove(cont)
        one_level_shipments.sort(key=lambda x: x.get_empty_volume(only_used_levels=True))

        while True:
            anything_joined = False
            for i, sh in enumerate(one_level_shipments):
                if not one_level_used[i]:
                    success = shipment.check_and_join(sh)
                    one_level_used[i] = success
                    if success:
                        anything_joined = True
            if not anything_joined or all(one_level_used):
                break

        if not all(one_level_used):
            for container in sorted_containers:
                self.place_container(shipment, container)

        placed_containers = shipment.get_all_containers()
        if check_urgent_containers:
            for container in sorted_containers:
                if container.timestamp == main_timestamp:
                    break
                elif container not in placed_containers:
                    correct_shipment = False
        return correct_shipment

    def check_and_add_shipment(self, shipment):
        """
        Check if a given shipment can be added to the shipments manager.
        If so, do it and remove used containers from the list.
        :param shipment: a shipment to add
        :return: True if successfully added, else False
        """
        success = self.shipments_manager.check_and_add(shipment)
        if success:
            for container in shipment.get_all_containers():
                self.sorted_containers.remove(container)
        return success

    def choose_and_add_shipment(self, shipments_list):
        """
        Add a shipment with the smallest relative empty volume to the shipments manager.
        :param shipments_list: a list of shipments
        :return: True if successfully added, else False
        """
        success = False
        shipments_list.sort(key=lambda x: x.get_empty_volume() / x.get_full_volume())
        for sh in shipments_list:
            success = self.check_and_add_shipment(sh)
            if success:
                break
        return success

    def optimize(self, ships, containers, timestamp, container_height, previous_shipment):
        """
        Place containers on ships in an optimal way.
        :param ships: list of available ships
        :param containers: a list container to place
        :param timestamp: a main timestamp of containers
        :param container_height: a constant height of containers
        :param previous_shipment: the last (unsent) shipment returned by previous optimization
                                  Situation when it is used:
                                  During the latest optimization we had a big ship and we could place 100 containers
                                  on it. We placed 75 containers and hoped we would place more so we didn't send
                                  this shipment. Now the biggest ship can contain 50 containers. In this situation
                                  we send the shipment based on the previous big ship.
        :return: a shipment manager with list of shipment to send
        """
        self.container_height = container_height
        self.containers = containers
        self.ships = ships
        self.timestamp = timestamp
        self.previous_shipment = previous_shipment
        self.shipments_manager = ShipmentsManager(timestamp)
        if self.report_generator is not None:
            self.report_generator.log("******* OPTIMIZER LOG START *******")
            self.report_generator.increase_indent()

        self.sorted_containers = sorted(containers, key=self.prioritize_containers)
        if self.report_generator is not None:
            self.report_generator.log(f"{len(self.sorted_containers)} containers to place.")
        first_shipments = [Shipment(ship=s, containers_height=container_height) for s in ships]
        correct_first_shipments = [sh for sh in first_shipments if
                                   self.optimize_single_shipment(sh, self.sorted_containers,
                                                                 check_urgent_containers=True,
                                                                 main_timestamp=timestamp)]

        if len(correct_first_shipments) == 0:
            if self.report_generator is not None:
                """
                That is the described situation when to use previous_shipment.
                """
                self.report_generator.log("CAN NOT SEND CONTAINERS WITH PREVIOUS TIMESTAMPS USING CURRENT SHIPS."
                                          "PREVIOUS SHIP IS USED")
            self.check_and_add_shipment(previous_shipment)
        else:
            self.choose_and_add_shipment(correct_first_shipments)

        while len(self.sorted_containers) > 0:
            self.report_generator.log(f"{len(self.sorted_containers)} containers to place.")
            shipments = [Shipment(ship=s, containers_height=container_height) for s in ships]
            for sh in shipments:
                self.optimize_single_shipment(sh, self.sorted_containers)
            self.choose_and_add_shipment(shipments)

        if self.report_generator is not None:
            self.report_generator.decrease_indent()
            self.report_generator.log("******* OPTIMIZER LOG STOP ********\n")
        return self.shipments_manager


def test():
    cm = ContainersManager()
    cm.add("c10,1,2,2,5", min_timestamp=0)
    cm.add("c11,1,2,2,2", min_timestamp=0)
    cm.add("c12,3,2,2,3", min_timestamp=0)
    cm.add("c13,1,2,2,3", min_timestamp=0)
    cm.add("c14,1,2,2,4", min_timestamp=0)

    opt = GreedyOptimizer()
    containers = cm.waiting_containers
    print(containers)
    s = sorted(containers, key=opt.prioritize_containers)
    print(s)


if __name__ == "__main__":
    test()