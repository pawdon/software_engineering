import pytest
from ships_module import ship_file


def test_from_string():
    """Comparing ship build by constructor(s1) with ship build by method from_string() [s2-s3]"""
    s1 = ship_file.Ship(sid=10, width=1, height=5, length=3)
    s2 = ship_file.Ship.from_string("s10,1,5,3")
    s3 = ship_file.Ship.from_string("s11,1,5,3")

    assert s1.sid == s2.sid
    assert s1.width == s2.width
    assert s1.height == s2.height
    assert s1.length == s2.length
    assert s1.timestamp == s2.timestamp

    assert s1.sid != s3.sid
    assert s1.width == s3.width
    assert s1.height == s3.height
    assert s1.length == s3.length
    assert s1.timestamp == s3.timestamp

def test_to_string_with_timestamp():
    """ This test check method which add timestamp to string varsion of ship. Test is past when string which
    represent built ship is the same with string wrote from keyboard"""

    s1 = ship_file.Ship(sid=10, width=1, height=5, length=3, timestamp=10)

    assert s1.to_str_with_timestamp() == f"s10,1,5,3;t=10"
