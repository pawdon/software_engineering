import numpy as np
from .shipments_manager_file import ShipmentsManager, Shipment, PlacedContainer, CornerPosition


class IOptimizer:
    """
    An abstract optimizer class.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.shipments_manager = None
        self.container_height = None
        self.ships = None
        self.containers = None
        self.timestamp = None
        self.previous_shipment = None
        self.report_generator = None

    @staticmethod
    def info():
        """
        Return a string with information describing the optimizer.
        :return: a string with information describing the optimizer
        """
        return "Abstract optimizer interface"

    @staticmethod
    def place_container(shipment, container, single_level=None, if_sort_by_width=False):
        """
        Place container in a first empty place.
        :param shipment: a shipment
        :param container: a container to place
        :param single_level: (int) a level number where to place the container (if None, place wherever)
        :param if_sort_by_width: (bool) if True, sort empty points by width, else sort them by length
        :return: True if successfully placed the container on the ship, else False
        """
        if single_level is None:
            empty_points = np.argwhere(shipment.occupancy_map == 0)
            if if_sort_by_width:
                empty_points = empty_points[empty_points[:, 2].argsort(kind='mergesort')]
        else:
            empty_points = np.argwhere(shipment.occupancy_map[single_level] == 0)
            if if_sort_by_width:
                empty_points = empty_points[empty_points[:, 1].argsort(kind='mergesort')]

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
        """
        Place containers on ships in an optimal way (an abstract method).
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
        self.shipments_manager = ShipmentsManager(timestamp)
        return self.shipments_manager
