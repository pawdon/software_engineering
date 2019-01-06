from containers_module.containers_manager_file import ContainersManager
from containers_module.container_file import Container


def test_add():

    """Test check_add 1) if add container == container make by constructor 2) if timestamp is not int method return none
    3) If timestamp is int method not return None"""

    cm1 = ContainersManager()
    con1 = Container(cid=10, width=1, height=2, length=3, timestamp=4)
    con2 = cm1.add("c10,1,2,3,4", min_timestamp=1)
    con3 = cm1.add("c10,1,2,2,2", min_timestamp=1/3)
    con4 = cm1.add("c13,1,2,2,2", min_timestamp=1)

    assert con2.cid == con1.cid
    assert con2.height == con1.height
    assert con2.length == con1.length
    assert con2.width == con1.width
    assert con2.timestamp == con1.timestamp
    assert con3 is None
    assert con4 is not None


def test_get_containers():
    """This test check if method return list of containers or no and check if containers are correct """
    def __eq__(self, other):
        assert self.cid == other.cid
        assert self.width == other.width
        assert self.height == other.height
        assert self.length == other.length
        assert self.timestamp == other.timestamp

    cm = ContainersManager()
    ch1 = Container.from_string("c9,1,2,4,1")
    ch2 = Container.from_string("c10,2,2,2,2")
    ch3 = Container.from_string("c11,3,2,3,3")
    ch4 = Container.from_string("c12,4,2,4,3")
    ch5 = Container.from_string("c13,5,2,5,5")

    c1 = cm.add("c9,1,2,4,1", min_timestamp=0)
    c2 = cm.add("c10,2,2,2,2", min_timestamp=0)
    c3 = cm.add("c11,3,2,3,3", min_timestamp=0)
    c4 = cm.add("c12,4,2,4,3", min_timestamp=1)
    c5 = cm.add("c13,5,2,5,4", min_timestamp=4)
    cons = cm.get_containers(max_timestamp=3)

    if c1 in cons:
        __eq__(c1, ch1)

    if c2 in cons:
        __eq__(c2, ch2)

    if c3 in cons:
        __eq__(c3, ch3)

    if c4 in cons:
        __eq__(c4, ch4)

    if c5 in cons:
        __eq__(c5, ch5)


def test_send():
    """Test_send check container send status - list sent_containers has some objects"""

    cm = ContainersManager()
    cm.add("c9,1,2,4,1", min_timestamp=0)
    cm.add("c10,1,2,2,2", min_timestamp=0)
    cm.add("c11,3,2,3,3", min_timestamp=0)
    cm.add("c12,4,2,4,4", min_timestamp=1)
    cm.add("c13,4,2,5,5", min_timestamp=4)
    cons = cm.get_containers(max_timestamp=3)
    cm.send(cons)
    assert cm.sent_containers == cons

    cm1 = ContainersManager()
    cm1.add("c9,1,2,4,1", min_timestamp=0)
    cm1.add("c10,1,2,2,2", min_timestamp=0)
    cm1.add("c11,3,2,3,3", min_timestamp=0)
    cm1.add("c12,4,2,4,4", min_timestamp=1)
    cm1.add("c13,4,2,5,5", min_timestamp=4)
    cons = cm1.get_containers(max_timestamp=0)
    cm1.send(cons)
    assert not cm1.sent_containers






