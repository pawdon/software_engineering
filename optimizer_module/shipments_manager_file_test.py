from optimizer_module.corner_position_file import CornerPosition
from optimizer_module.placed_container_file import PlacedContainer
from optimizer_module.shipment_file import Shipment
from containers_module.container_file import Container
from ships_module.ship_file import Ship
from optimizer_module.shipments_manager_file import ShipmentsManager


def test_check_and_add():
    """ We have 3 sh sh0 with c01 2x2 on height_level =0 on length=0, width=0; - shipment correct
                  sh1 with c11 2x2 on height_level =0 on length=3, width=0; - shipment correct
                  sh2 with c01 2x2 on height_level =0 on length=2, width=2  - shipment correct
         We add sh0 to shipment manager list:
             add1 - we add to shipment manager list sh1 with container with wrong timestamp - method return False
                    method _check_shipment_timestamp working
             add2 - we add to shipment manager list sh2 with container c01 from sh0 - method return False because
                    redundancy is forbidden  - method _check_redundancy working"""

    shm = ShipmentsManager(main_timestamp=39)

    """ Shipment sh0"""
    s0 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh0 = Shipment(s0, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    sh0.check_and_add(pc01)
    """ Shipment sh1 - empty  - c11 not stable """
    sh1 = Shipment(s0, containers_height=10)
    c11 = Container(cid=11, length=2, width=2, height=10, timestamp=29)
    pc11 = PlacedContainer(container=c11, corner1=CornerPosition(height_level=0, length=3, width=0))
    sh1.check_and_add(pc11)
    """ Shipment sh2"""
    sh2 = Shipment(s0, containers_height=10)
    pc21 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh2.check_and_add(pc21)

    shm.check_and_add(sh0)
    add1 = shm.check_and_add(sh1)
    add2 = shm.check_and_add(sh2)

    assert not add1
    assert not add2


def test_get_containers():
    """ We have 3 sh sh0 with c01 2x2 on height_level =0 on length=0, width=0; - shipment correct
                  sh1 with c11 2x2 on height_level =1 on length=0, width=0; - shipment empty - c11 not stable
                  sh2 with c21 2x2 on height_level =0 on length=2, width=2  - shipment correct
        Method add 3 sh1 and sh2 to sh3 and return all containers of added shipments.
        At finish we check if all.containers are correct by comparing them with expected containers.  """

    shm = ShipmentsManager(main_timestamp=39)

    def __eq__(self, other):
        assert self.cid == other.cid
        assert self.width == other.width
        assert self.height == other.height
        assert self.length == other.length
        assert self.timestamp == other.timestamp


    """ Shipment sh0"""
    s0 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh0 = Shipment(s0, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    sh0.check_and_add(pc01)
    """ Shipment sh1 - empty  - c11 not stable """
    sh1 = Shipment(s0, containers_height=10)
    c11 = Container(cid=11, length=2, width=2, height=10, timestamp=39)
    pc11 = PlacedContainer(container=c11, corner1=CornerPosition(height_level=1, length=0, width=0))
    sh1.check_and_add(pc11)
    """ Shipment sh2"""
    sh2 = Shipment(s0, containers_height=10)
    c21 = Container(cid=21, length=2, width=2, height=10, timestamp=39)
    pc21 = PlacedContainer(container=c21, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh2.check_and_add(pc21)

    shm.check_and_add(sh0)
    shm.check_and_add(sh1)
    shm.check_and_add(sh2)
    cons = shm.get_containers()

    cc1 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    cc3 = Container(cid=21, length=2, width=2, height=10, timestamp=39)

    cons_c = [cc1,cc3]
    __eq__(cons_c[0], cons[0])
    __eq__(cons_c[1], cons[1])


def test_check_and_remove():
    """ We have 3 sh sh0 with c01 2x2 on height_level =0 on length=0, width=0; - shipment correct
                  sh1 with c11 2x2 on height_level =0 on length=3, width=0; - shipment correct
                  sh2 with c01 2x2 on height_level =0 on length=2, width=2  - shipment correct
          rm 1 - we want to remove sh0 but it is 1st shipment so method return False
          rm 2 - we want to remove sh1, it is not 1st shipment so it is ok and method return True"""

    s0 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh0 = Shipment(s0, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    sh0.check_and_add(pc01)
    """ Shipment sh1 - empty  - c11 not stable """
    sh1 = Shipment(s0, containers_height=10)
    c11 = Container(cid=11, length=2, width=2, height=10, timestamp=39)
    pc11 = PlacedContainer(container=c11, corner1=CornerPosition(height_level=0, length=3, width=0))
    sh1.check_and_add(pc11)
    """ Shipment sh2"""
    sh2 = Shipment(s0, containers_height=10)
    c21 = Container(cid=21, length=2, width=2, height=10, timestamp=39)
    pc21 = PlacedContainer(container=c21, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh2.check_and_add(pc21)

    shm = ShipmentsManager(main_timestamp=39)
    shm.check_and_add(sh0)
    shm.check_and_add(sh1)
    shm.check_and_add(sh2)
    rm1 = shm.check_and_remove(sh0)
    rm2 = shm.check_and_remove(sh1)
    assert not rm1
    assert rm2


