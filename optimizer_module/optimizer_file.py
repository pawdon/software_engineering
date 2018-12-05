import numpy as np
import random
#from .shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition
from optimizer_module.shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition
from containers_module.containers_manager_file import ContainersManager


class OptimizerSelector:
    @staticmethod
    def select(nr=1):
        optimizers = [IOptimizer, Optimizer1, Optimizer2]
        return optimizers[nr]()

    @staticmethod
    def correct_algorithms_ids():
        return [1, 2]


class IOptimizer:
    def __init__(self):
        self.shipments_manager = None
        self.container_height = None
        self.ships = None
        self.containers = None
        self.timestamp = None
        self.previous_shipment = None
        self.report_generator = None

    @staticmethod
    def info():
        return "Abstract optimizer interface"

    @staticmethod
    def place_container(shipment, container, single_level=None):
        if single_level is None:
            empty_points = np.argwhere(shipment.occupancy_map == 0)
        else:
            empty_points = np.argwhere(shipment.occupancy_map[single_level] == 0)

        for coordinates in empty_points:
            if single_level is None:
                h, l, w = coordinates
            else:
                h = single_level
                l, w = coordinates

            if shipment.check_and_add(PlacedContainer(container, CornerPosition(length=l, width=w, height_level=h))):
                return True
        return False

    def optimize(self, ships, containers, timestamp, container_height, previous_shipment):
        self.shipments_manager = ShipmentsManager(timestamp)
        return self.shipments_manager


class Optimizer1(IOptimizer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def info():
        return "Stupid optimizer"

    def new_shipment(self):
        ship = random.choice(self.ships)
        shipment = Shipment(ship, containers_height=self.container_height)
        return shipment

    def optimize(self, ships, containers, timestamp, container_height, previous_shipment):
        """

        :param ships:
        :param containers:
        :param timestamp:
        :param container_height:
        :param previous_shipment:
        Sytuacja w której to jest użyte:
        W poprzedniej turze mieliśmy duży fajny statek. Nie zapakowaliśmy go do końca, więc nie wysłaliśmy ostatniej
        partii. Teraz nie mamy już tego statku. Okazało się, że nie jesteśmy w stanie wysłać naraz zalegających
        kontenerów nowymi statkami, ale musimy to jakoś zrobić. W związku z tym wysyłamy tamten duży statek tak,
        jak mogliśmy.
        :return:
        """
        self.container_height = container_height
        self.containers = containers
        self.ships = ships
        self.timestamp = timestamp
        self.previous_shipment = previous_shipment
        self.shipments_manager = ShipmentsManager(timestamp)

        use_previous_shipment = False

        shipment = self.new_shipment()
        for container in self.containers:
            if use_previous_shipment:
                if container in self.previous_shipment.get_all_containers():
                    continue
            if_success = self.place_container(shipment, container)
            if not if_success:
                if container.timestamp < self.timestamp:
                    """
                    To jest właśnie ta sytuacja
                    """
                    use_previous_shipment = True
                    self.shipments_manager.check_and_add(self.previous_shipment)
                else:
                    self.shipments_manager.check_and_add(shipment)
                    shipment = self.new_shipment()
                    self.place_container(shipment, container)
        self.shipments_manager.check_and_add(shipment)
        return self.shipments_manager


class Optimizer2(IOptimizer):
    def __init__(self):
        super().__init__()
        self.sorted_containers = None

    @staticmethod
    def info():
        return "Greedy optimizer"

    @staticmethod
    def prioritize_containers(c):
        return c.timestamp, -(c.length * c.width)

    def optimize_single_level(self, shipment, sorted_containers, single_level=None):
        if single_level is None:
            single_level = shipment.get_used_levels_nr()
        for container in sorted_containers:
            self.place_container(shipment, container, single_level)

    def optimize_single_shipment(self, shipment, sorted_containers, check_urgent_containers=False, main_timestamp=None):
        correct_shipment = True

        containers_copy = sorted_containers.copy()
        one_level_shipments = [shipment.copy(only_ship=True) for _ in range(shipment.levels_nr)]
        one_level_used = [False for _ in range(shipment.levels_nr)]
        for sh in one_level_shipments:
            self.optimize_single_level(sh, containers_copy, single_level=0)
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
        success = self.shipments_manager.check_and_add(shipment)
        if success:
            for container in shipment.get_all_containers():
                self.sorted_containers.remove(container)
        return success

    def choose_and_add_shipment(self, shipments_list):
        success = False
        shipments_list.sort(key=lambda x: x.get_empty_volume())
        for sh in shipments_list:
            success = self.check_and_add_shipment(sh)
            if success:
                break
        return success

    def optimize(self, ships, containers, timestamp, container_height, previous_shipment):
        """

        :param ships:
        :param containers:
        :param timestamp:
        :param container_height:
        :param previous_shipment:
        Sytuacja w której to jest użyte:
        W poprzedniej turze mieliśmy duży fajny statek. Nie zapakowaliśmy go do końca, więc nie wysłaliśmy ostatniej
        partii. Teraz nie mamy już tego statku. Okazało się, że nie jesteśmy w stanie wysłać naraz zalegających
        kontenerów nowymi statkami, ale musimy to jakoś zrobić. W związku z tym wysyłamy tamten duży statek tak,
        jak mogliśmy.
        :return:
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

    opt = Optimizer2()
    containers = cm.waiting_containers
    print(containers)
    s = sorted(containers, key=opt.prioritize_containers)
    print(s)


if __name__ == "__main__":
    test()

