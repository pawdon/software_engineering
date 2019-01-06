import pytest
from containers_module import container_file


def test_to_ordered_string():
    con = container_file.Container(2, 30, 20, 10, 15)
    con1 = container_file.Container(4, 20, 10, 14, 15)

    assert con.to_ordered_string() == f"c{con.cid},length={con.length},width={con.width},"\
                                     f"height={con.height},timestamp={con.timestamp}"
    assert con1.to_ordered_string() == f"c{con1.cid},length={con1.length},width={con1.width}," \
                                       f"height={con1.height},timestamp={con1.timestamp}"


def test_from_string():
    """Comparing container build by constructor with container build by method from_string()"""

    def __eq__(self, other):
        assert self.cid == other.cid
        assert self.width == other.width
        assert self.height == other.height
        assert self.length == other.length
        assert self.timestamp == other.timestamp

    c1 = container_file.Container(cid=10, width=1, height=5, length=3, timestamp=2)
    c2 = container_file.Container.from_string("c10,1,5,3,2")
    c3 = container_file.Container.from_string("c10,1,5,3,3")

    __eq__(c1, c2)

    assert c1.cid == c3.cid
    assert c1.width == c3.width
    assert c1.height == c3.height
    assert c1.length == c3.length
    assert c1.timestamp != c3.timestamp



