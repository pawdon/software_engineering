from ships_module.ships_manager_file import ShipsManager
from ships_module.ship_file import Ship

def test_add():

    """Test check_add 1) if add ship == ship make by constructor 2) if timestamp is not int method return none
        3) If timestamp is int method not return None"""
    sm = ShipsManager()
    s1 = Ship(sid=10, width=51, height=52, length=52, timestamp=2)
    s2 = sm.add("s10,51,52,52", added_timestamp=2)
    s3 = sm.add("s11,51,52,52", added_timestamp=2/3)
    s4 = sm.add("s12,51,52,52", added_timestamp=2)

    assert s2.sid == s1.sid
    assert s2.height == s1.height
    assert s2.length == s1.length
    assert s2.width == s1.width
    assert s2.timestamp == s1.timestamp
    assert s3 is None
    assert s4 is not None

def test_get_available():

    def __eq__(self, other):
        assert self.sid == other.sid
        assert self.width == other.width
        assert self.height == other.height
        assert self.length == other.length

    sm = ShipsManager(max_available=3)
    s1 = sm.add("s10,51,52,52", added_timestamp=2)
    s2 = sm.add("s11,51,52,52", added_timestamp=2)
    s3 = sm.add("s12,51,52,52", added_timestamp=3)
    s4 = sm.add("s13,51,52,52", added_timestamp=3)
    s5 = sm.add("s14,51,52,52", added_timestamp=4)

    sh1 = Ship.from_string("s10,51,52,52")
    sh2 = Ship.from_string("s11,51,52,52")
    sh3 = Ship.from_string("s12,51,52,52")
    sh4 = Ship.from_string("s13,51,52,52")
    sh5 = Ship.from_string("s14,51,52,53")

    shps = sm.get_available(max_timestamp=3)
    """ Checking differences between expecting containers [sh1 - sh5] and result of get_cont [s1 - s5] --- 
    if max_timestamp = 3 available are ships [s1 - s4] and test is pass because sh1-sh4 are the same. 
    If max_timestamp = 4 s5 != sh5, adn test is fail, so - it works :)"""

    if s1 in shps:
        __eq__(s1, sh1)

    if s2 in shps:
        __eq__(s2, sh2)

    if s3 in shps:
        __eq__(s3, sh3)

    if s4 in shps:
        __eq__(s4, sh4)

    if s5 in shps:
        __eq__(s5, sh5)


