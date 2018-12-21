class Container:
    """
    Class used for storing a single container.
    """
    def __init__(self, cid, length, width, height, timestamp):
        """
        Constructor.
        :param cid: container id (int)
        :param length: container length (int)
        :param width: container width (int)
        :param height: container height (int)
        :param timestamp: container timestamp (int)
        """
        self.cid = cid              # id of a container
        self.length = length        # length of a container
        self.width = width          # width of a container
        self.height = height        # height of a container
        self.timestamp = timestamp  # timestamp of a container

    def __str__(self):
        """
        Create a string from the container. It is inversion of from_string(). Used when call print(container).
        :return: A string describing the container.
        """
        return f"c{self.cid},{self.width},{self.height},{self.length},{self.timestamp}"

    def __repr__(self):
        """
        Create a string from the container. Used when call print(list of containers).
        :return: A string describing the container.
        """
        return f"Container({self.__str__()})"

    def to_ordered_string(self, order=None):
        """
        Create a string from the container with named values in a given order.
        :param order: list of strings of named values, eg. ["length", "width", "height"]
        :return: A string describing the container.
        """
        if order is None:
            order = ["length", "width", "height"]
        d = {"length": self.length,
             "width": self.width,
             "height": self.height}
        return f"c{self.cid}," \
               f"{order[0]}={d[order[0]]},{order[1]}={d[order[1]]},{order[2]}={d[order[2]]}," \
               f"timestamp={self.timestamp}"

    @staticmethod
    def from_string(text):
        """
        Creates a container from string and return it. Check only if the string can be split to correct number of ints.
        :param text: string in format c{id},{width},{height},{length},{timestamp}
        :return: a container or None
        """
        if text[0] != "c":
            return None
        if text[-1] == "\n":
            text = text[0:-1]
        try:
            cid, width, height, length, timestamp = [int(x) for x in text[1:].split(",")]
        except ValueError:
            return None
        return Container(cid=cid, width=width, height=height, length=length, timestamp=timestamp)


def test1():
    c1 = Container(cid=2, length=4, width=5, height=7, timestamp=39)
    text = c1.to_ordered_string()
    print(text)
    c2 = Container.from_string(text)
    print(c2)
    print(Container.from_string("c10,1,2,2,2"))
    print(Container.from_string("c10,f,2,2,2"))
    print(Container.from_string("c10,1,2,2"))
    print(Container.from_string("c10,1,2,2,2,3"))


if __name__ == "__main__":
    test1()
