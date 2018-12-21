import numpy as np
import random
from .shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition
from .abstract_optimizer_file import IOptimizer
#from optimizer_module.shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition
from containers_module.containers_manager_file import ContainersManager


class FastOptimizer(IOptimizer):
    """
    A fast optimizer class.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__()

    @staticmethod
    def info():
        """
        Return a string with information describing the optimizer.
        :return: a string with information describing the optimizer
        """
        return "Fast optimizer"

    def new_shipment(self):
        """
        Random a ship and return a new shipment.
        :return: a new shipment
        """
        ship = random.choice(self.ships)
        shipment = Shipment(ship, containers_height=self.container_height)
        return shipment

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
                    That is the described situation when to use previous_shipment.
                    """
                    use_previous_shipment = True
                    self.shipments_manager.check_and_add(self.previous_shipment)
                else:
                    self.shipments_manager.check_and_add(shipment)
                    shipment = self.new_shipment()
                    self.place_container(shipment, container)
        self.shipments_manager.check_and_add(shipment)
        return self.shipments_manager
