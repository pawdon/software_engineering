from .ship_file import Ship


class ShipsManager:
    """
    Class used for storing a list of ships,
    checking if a ship has correct values
    and managing information about available ships.
    """
    def __init__(self, max_available=3, **args):
        """
        Constructor.
        :param max_available: maximum number of ships available in the same time
        :param args: an optional dictionary used for changing default values
        """
        self.max_available = max_available  # maximum number of ships available in the same time
        self.ships = []                     # list of ships
        self.available = []                 # list of available ships

        # default values defining a correct ship
        self.min_length = args.get("min_length", 50)
        self.max_length = args.get("max_length", 100)
        self.min_width = args.get("min_width", 50)
        self.max_width = args.get("max_width", 100)
        self.min_height = args.get("min_height", 50)
        self.max_height = args.get("max_height", 100)

    def __str__(self):
        """
        Create a string from the ships manager. Used when call print(ships manager).
        :return: A string describing the ships manager.
        """
        result = "\n\t".join([f"Ships ({len(self.ships)})"]
                             + [x.to_str_with_timestamp() for x in self.ships])
        if len(self.available) > 0:
            result += "\n" + "\n\t".join([f"Available ({len(self.available)})"]
                                         + [x.to_str_with_timestamp() for x in self.available])
        return result

    def add(self, x, added_timestamp):
        """
        Create a ship from a given string. Check if it is correct and if so, add to list of ships.
        :param x: a string describing a ship
        :param added_timestamp: timestamp added to a ship
        :return: a ship (if successfully added) or None
        """
        if type(added_timestamp) is not int:
            return None
        ship = Ship.from_string(x)
        if ship is not None:
            check_ok = self.min_length <= ship.length <= self.max_length and \
                       self.min_width <= ship.width <= self.max_width and \
                       self.min_height <= ship.height <= self.max_height and \
                       ship.sid not in [x.sid for x in self.ships]
            if check_ok:
                ship.timestamp = added_timestamp
                self.ships.append(ship)
            else:
                ship = None
        return ship

    def get_available(self, max_timestamp):
        """
        Save and get list of available ships.
        :param max_timestamp: maximum timestamp a ship must have
        :return: a list of available ships
        """
        self.available = []
        for ship in reversed(self.ships):
            if ship.timestamp <= max_timestamp:
                self.available.append(ship)
                if len(self.available) >= self.max_available:
                    break
        return self.available


def test2():
    sm = ShipsManager(max_available=3)
    sm.add("s10,51,52,52", added_timestamp=2)
    sm.add("s11,51,52,52", added_timestamp=2)
    sm.add("s12,51,52,52", added_timestamp=2)
    sm.add("s13,51,52,52", added_timestamp=3)
    sm.add("s14,51,52,52", added_timestamp=3)
    sm.add("s15,51,52,52", added_timestamp=4)
    sm.add("s12,51,52,52", added_timestamp=4)
    print(sm)
    sm.get_available(max_timestamp=3)
    print(sm)


if __name__ == "__main__":
    test2()
