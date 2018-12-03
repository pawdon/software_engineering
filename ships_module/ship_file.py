class Ship:
    """
    Class used for storing a single ship.
    """
    def __init__(self, sid, length, width, height, timestamp=None):
        """
        Constructor.
        :param sid: ship id (int)
        :param length: ship length (int)
        :param width: ship width (int)
        :param height: ship height (int)
        :param timestamp: ship timestamp (int) (optional)
        """
        self.sid = sid              # id of a ship
        self.length = length        # length of a ship
        self.width = width          # width of a ship
        self.height = height        # height of a ship
        self.timestamp = timestamp  # timestamp of a ship

    def __str__(self):
        """
        Create a string from the ship without timestamp. It is inversion of from_string(). Used when call print(ship).
        :return: A string describing the ship.
        """
        return f"s{self.sid},{self.width},{self.height},{self.length}"

    def __repr__(self):
        """
        Create a string from the ship without timestamp. Used when call print(list of ships).
        :return: A string describing the ship.
        """
        return f"Ship({self.__str__()})"

    def to_str_with_timestamp(self):
        """
        Create a string from the ship with timestamp.
        :return: A string describing the ship.
        """
        return f"{self.__str__()};t={self.timestamp}"

    def to_string(self):
        """
        The same as __str__()
        :return: A string describing the ship.
        """
        return self.__str__()

    @staticmethod
    def from_string(text):
        """
        Creates a ship from string and return it. Check only if the string can be split to correct number of ints.
        :param text: string in format s{id},{width},{height},{length}
        :return: a ship
        """
        if text[0] != "s":
            return None
        if text[-1] == "\n":
            text = text[0:-1]
        try:
            sid, width, height, length = [int(x) for x in text[1:].split(",")]
        except ValueError:
            return None
        return Ship(sid=sid, width=width, height=height, length=length)


def test1():
    s1 = Ship(sid=2, length=4, width=5, height=7, timestamp=39)
    text = s1.to_string()
    print(text)
    s2 = Ship.from_string(text)
    print(s2)
    print(Ship.from_string("s10,1,2,2"))
    print(Ship.from_string("c10,1,2,2"))


if __name__ == "__main__":
    test1()
