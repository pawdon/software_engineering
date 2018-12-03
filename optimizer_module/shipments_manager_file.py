import numpy as np
from .corner_position_file import CornerPosition
from .placed_container_file import PlacedContainer
from .shipment_file import Shipment
from containers_module.container_file import Container
from ships_module.ship_file import Ship


class ShipmentsManager:
    """
    Class used for storing and managing shipments.
    """
    def __init__(self, main_timestamp):
        """
        Constructor.
        :param main_timestamp: main timestamp for the shipments
        """
        self.main_timestamp = main_timestamp    # main timestamp for the shipments
        self.shipments = []                     # list of shipments

    def __str__(self):
        """
        Create a string describing the shipments manager. Used when call print(shipments manager).
        :return: a string describing the shipments manager
        """
        result = f"ShipmentManager (timestamp = {self.main_timestamp}, " \
                 f"empty volume = {self.get_summary_empty_volume()})"
        for sh in self.shipments:
            result += "\n" + sh.to_ordered_string(get_map=False)
        return result

    def get_summary_empty_volume(self, only_used_levels=False):
        """
        Get a summary empty volume in all shipments.
        :param only_used_levels: (bool) if True than include only information about used height levels
        :return: a summary empty volume in all shipments
        """
        return sum([sh.get_empty_volume(only_used_levels) for sh in self.shipments])

    def get_containers(self, skip_first_shipment=False, skip_last_shipment=False):
        """
        Get a list of containers in all shipments.
        :param skip_first_shipment: (bool) if True, skip first shipment
        :param skip_last_shipment:  (bool) if True, skip last shipment
        :return: a list of containers in all shipments
        """
        shipments_list = self.shipments
        if skip_first_shipment:
            shipments_list = shipments_list[1:]
        if skip_last_shipment:
            shipments_list = shipments_list[0:-1]
        containers_list = []
        for sh in shipments_list:
            containers_list += sh.get_all_containers()
        return containers_list

    def _check_shipment_timestamps(self, shipment):
        """
        Private method.
        Check timestamps of all containers in a given shipment. In first shipment there can be timestamps lower than
        or equal to the main timestamp. In all other shipments there can be only timestamps equal to the main timestamp.
        :param shipment: a shipment to verify
        :return: True if timestamps in a given shipment are correct, else False
        """
        if_ok = False
        timestamps_set = shipment.get_timestamps_set()
        if len(self.shipments) == 0:
            if max(timestamps_set) <= self.main_timestamp:
                if_ok = True
        else:
            if len(timestamps_set) == 1 and self.main_timestamp in timestamps_set:
                if_ok = True
        return if_ok

    def _check_redundancy(self, shipment):
        """
        Private method.
        Check if there is no containers redundancy in the already added shipments and a given shipment.
        :param shipment: a shipment to verify
        :return: True if there is no redundancy, else False
        """
        if_ok = True
        loaded_containers = self.get_containers()
        for container in shipment.get_all_containers():
            if container in loaded_containers:
                if_ok = False
                break
        return if_ok

    def check_and_add(self, shipment):
        """
        Check if a given shipment can be added to list and if so, add it.
        A shipment can be added if
            - its containers have correct timestamps,
            - no container from the given shipment is in the already added shipments (redundancy is forbidden).
        :param shipment: a shipment to add
        :return: True if successfully added, else False
        """
        if_can = False
        if type(shipment) is Shipment:
            if_can = self._check_shipment_timestamps(shipment) and self._check_redundancy(shipment)
        if if_can:
            self.shipments.append(shipment)
        return if_can

    def check_and_remove(self, shipment):
        """
        Check if a given shipment can be removed and if so, remove it.
        A shipment can not be removed only if it is the first shipment and there are other shipments.
        Read a description of _check_shipment_timestamps() to know why.
        :param shipment: a shipment to remove.
        :return: True if successfully removed, else False
        """
        if_can = False
        if shipment in self.shipments:
            if len(self.shipments) == 1:
                if_can = True
            elif shipment != self.shipments[0]:
                if_can = True
        if if_can:
            self.shipments.remove(shipment)
        return if_can


def test2():
    sh1 = Shipment(Ship(sid=1, length=5, width=5, height=20, timestamp=39), containers_height=10)
    sh2 = Shipment(Ship(sid=1, length=5, width=5, height=20, timestamp=39), containers_height=10)
    sh3 = Shipment(Ship(sid=1, length=5, width=5, height=20, timestamp=39), containers_height=10)
    sh4 = Shipment(Ship(sid=1, length=5, width=5, height=20, timestamp=39), containers_height=10)

    sh1.check_and_add(PlacedContainer(container=Container(cid=1, length=1, width=1, height=10, timestamp=39),
                                      corner1=CornerPosition(height_level=0, length=0, width=0)))
    c2 = Container(cid=2, length=1, width=1, height=10, timestamp=40)
    sh1.check_and_add(PlacedContainer(container=c2,
                                      corner1=CornerPosition(height_level=0, length=1, width=0)))

    sh2.check_and_add(PlacedContainer(container=Container(cid=3, length=1, width=1, height=10, timestamp=39),
                                      corner1=CornerPosition(height_level=0, length=0, width=0)))
    sh2.check_and_add(PlacedContainer(container=Container(cid=4, length=1, width=1, height=10, timestamp=40),
                                      corner1=CornerPosition(height_level=0, length=1, width=0)))

    sh3.check_and_add(PlacedContainer(container=Container(cid=5, length=1, width=1, height=10, timestamp=40),
                                      corner1=CornerPosition(height_level=0, length=0, width=0)))
    sh3.check_and_add(PlacedContainer(container=c2,
                                      corner1=CornerPosition(height_level=0, length=1, width=0)))

    sh4.check_and_add(PlacedContainer(container=Container(cid=7, length=1, width=1, height=10, timestamp=40),
                                      corner1=CornerPosition(height_level=0, length=0, width=0)))
    sh4.check_and_add(PlacedContainer(container=Container(cid=8, length=1, width=1, height=10, timestamp=40),
                                      corner1=CornerPosition(height_level=0, length=1, width=0)))

    shm = ShipmentsManager(main_timestamp=40)
    shm.check_and_add(sh1)
    shm.check_and_add(sh2)
    shm.check_and_add(sh3)
    shm.check_and_add(sh4)
    print(shm)
    shm.check_and_remove(sh2)
    shm.check_and_remove(sh1)
    shm.check_and_remove(sh4)
    print(shm)


if __name__ == "__main__":
    test2()
