from optimizer_module.corner_position_file import CornerPosition
from optimizer_module.placed_container_file import PlacedContainer
from containers_module.container_file import Container
from ships_module.ship_file import Ship
from optimizer_module.shipment_file import Shipment


def test_check_and_add():
    """ add 1  - cont. c1 which have all correct parameters(eg. width height etc) - check_and_add return True.
        add 2  - cont. c2 which have that same params like c1 and is placed on the same place  - check_and_add
                 return false because place is unoccupied by c1 and check_if_unoccupied() working
        add 3  - cont. c3 which have that same params like c1 and is placed "on air" next to c1 - check_and_add
                 return false because on lvl we don't have container - _check_if_stable() working
        add 4  - cont. c4 which have that same params like c1 and placed ON c1 - check_and_add return True
                 because we have space on lvl 1 because on lvl 0 standing C1 equal or more than c4 - _check_if_stable W
        add 5  -  cont. c5 which have good params but placed in bad position where some parts of this cont. could be over
                 the ship so check_and_add return False _check_if_inside_ship() working
        add 6  - check_and_add return False because in add6 we use c1, and this container is in our shipment
                 _check_redundancy working"""

    s1 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh = Shipment(s1, containers_height=10)
    c1 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    c2 = Container(cid=2, length=2, width=2, height=10, timestamp=39)
    c3 = Container(cid=3, length=2, width=2, height=10, timestamp=39)
    c4 = Container(cid=4, length=2, width=2, height=10, timestamp=39)
    c5 = Container(cid=5, length=2, width=2, height=10, timestamp=39)
    pc1 = PlacedContainer(container=c1, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc2 = PlacedContainer(container=c2, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc3 = PlacedContainer(container=c3, corner1=CornerPosition(height_level=1, length=2, width=2))
    pc4 = PlacedContainer(container=c4, corner1=CornerPosition(height_level=1, length=0, width=0))
    pc5 = PlacedContainer(container=c5, corner1=CornerPosition(height_level=0, length=4, width=4))
    pc6 = PlacedContainer(container=c1, corner1=CornerPosition(height_level=0, length=3, width=3))
    add1 = sh.check_and_add(pc1)
    add2 = sh.check_and_add(pc2)
    add3 = sh.check_and_add(pc3)
    add4 = sh.check_and_add(pc4)
    add5 = sh.check_and_add(pc5)
    add6 = sh.check_and_add(pc6)

    assert add1
    assert not add2
    assert not add3
    assert add4
    assert not add5
    assert not add6


def test_check_and_join():
    """ join 1 - it is situation when we want connect shipments: sh1(based on Ship s1) and sh2(based on s1)
                 check_and_join should return False because connecting shipments should base on the same ships
        join 2 - sh1 has 1 height_level and sh2 has 1 height_level. Method add containers from sh2 on the top of
                 sh1 containers and return True.
        join 3 - sh1 has 1 height_level snd sh3 has 2 height_level . Method check_and_join return False because sum of
                 height_levels = 3, and max height_level in ship is 2
        join 4 - sh1 has container c112x2 on position length = 0 width= 0. sh4 has container c51 3x3 on this same
                 position, and should add c51 On the top of c11 but it will be not stable so method return False
        join 5 - sh1 has container c11 2x2 on position length = 0 width= 0. sh5 has thi same container on position
                 length = 3 width= 0. Container can be add correctly but it is the same container in both shipments
                 and we don't want redundancy so method return False"""

    """ Shipment sh0"""
    s0 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh0 = Shipment(s0, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    c02 = Container(cid=2, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc02 = PlacedContainer(container=c02, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh0.check_and_add(pc01)
    sh0.check_and_add(pc02)

    """ Shipment sh1"""
    s1 = Ship(sid=11, length=5, width=5, height=20, timestamp=39)
    sh1 = Shipment(s1, containers_height=10)

    """ Shipment sh2"""
    sh2 = Shipment(s0, containers_height=10)
    c21 = Container(cid=21, length=2, width=2, height=10, timestamp=39)
    c22 = Container(cid=22, length=2, width=2, height=10, timestamp=39)
    pc21 = PlacedContainer(container=c21, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc22 = PlacedContainer(container=c22, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh2.check_and_add(pc21)
    sh2.check_and_add(pc22)

    """ Shipment sh3"""
    sh3 = Shipment(s0, containers_height=10)
    c31 = Container(cid=31, length=2, width=2, height=10, timestamp=39)
    c32 = Container(cid=32, length=2, width=2, height=10, timestamp=39)
    c33 = Container(cid=33, length=2, width=2, height=10, timestamp=39)
    pc31 = PlacedContainer(container=c31, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc32 = PlacedContainer(container=c32, corner1=CornerPosition(height_level=0, length=2, width=2))
    pc33 = PlacedContainer(container=c33, corner1=CornerPosition(height_level=1, length=2, width=2))
    sh3.check_and_add(pc31)
    sh3.check_and_add(pc32)
    sh3.check_and_add(pc33)

    """ Shipment sh4 """
    sh4 = Shipment(s0, containers_height=10)
    c41 = Container(cid=41, length=3, width=3, height=10, timestamp=39)
    pc41 = PlacedContainer(container=c41, corner1=CornerPosition(height_level=0, length=0, width=0))
    sh4.check_and_add(pc41)

    """ Shipment sh5 """
    sh5 = Shipment(s0, containers_height=10)
    pc51 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=3, width=0))
    sh5.check_and_add(pc51)

    """ Implements different examples of using method"""
    join1 = sh0.check_and_join(sh1)
    join2 = sh0.check_and_join(sh2)
    join3 = sh0.check_and_join(sh3)
    join4 = sh0.check_and_join(sh4)
    join5 = sh0.check_and_join(sh5)

    """ Checking different examples of using method """
    assert not join1
    assert join2
    assert not join3
    assert not join4
    assert not join5


def test_check_and_remove():

    """ We have ship with 2 height_levels. On height_level=0 we have 2 containers 2x2 c01 and c03.
        c01 is on length=0, width=0 c03 is on length=2, width=2. On height_level=1 we have container 2x2 c02
        length=0, width=0 - c02 is on the top of c01.
            rm 1 - We want to remove c01. Method return False because c02 will be not stable
            rm 2 - We want to remove c02. It is possible so method return True
            rm 3 - After removing c02 we want to remove c01. Now it is possible so method return True"""

    s1 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh = Shipment(s1, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    c02 = Container(cid=2, length=2, width=2, height=10, timestamp=39)
    c03 = Container(cid=3, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc02 = PlacedContainer(container=c02, corner1=CornerPosition(height_level=1, length=0, width=0))
    pc03 = PlacedContainer(container=c03, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh.check_and_add(pc01)
    sh.check_and_add(pc02)
    sh.check_and_add(pc03)
    """ Implements different examples of using method"""
    rm1 = sh.check_and_remove(pc01)
    rm2 = sh.check_and_remove(pc02)
    rm3 = sh.check_and_remove(pc01)
    """ Checking different examples of using method """
    assert not rm1
    assert rm2
    assert rm3


def test_remove_recursively():
    """ We have ship with 2 height_levels. On height_level=0 we have 2 containers 2x2 c01 and c03.
        c01 is on length=0, width=0 c03 is on length=2, width=2. On height_level=1 we have container 2x2
        c02 is on length=0, width=0 - c02 is on the top of c01.
        rmr 1 - We want to remove c01 so method remove c01 and c03 because after removing c01 c03 will be not stable """

    s1 = Ship(sid=1, length=5, width=5, height=20, timestamp=39)
    sh = Shipment(s1, containers_height=10)
    c01 = Container(cid=1, length=2, width=2, height=10, timestamp=39)
    c02 = Container(cid=2, length=2, width=2, height=10, timestamp=39)
    c03 = Container(cid=3, length=2, width=2, height=10, timestamp=39)
    pc01 = PlacedContainer(container=c01, corner1=CornerPosition(height_level=0, length=0, width=0))
    pc02 = PlacedContainer(container=c02, corner1=CornerPosition(height_level=1, length=0, width=0))
    pc03 = PlacedContainer(container=c03, corner1=CornerPosition(height_level=0, length=2, width=2))
    sh.check_and_add(pc01)
    sh.check_and_add(pc02)
    sh.check_and_add(pc03)

    rmr1 = sh.remove_recursively(pc01)

    assert rmr1
