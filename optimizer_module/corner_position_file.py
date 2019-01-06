class CornerPosition:
    """
    Class used for storing information about position of a corner of a container.
    """
    def __init__(self, length, width, height_level):
        """
        Constructor
        :param length: corner position in the length axis
        :param width: corner position in the width axis
        :param height_level: corner position in the height axis
        """
        self.length = length                # corner position in the length axis
        self.width = width                  # corner position in the width axis
        self.height_level = height_level    # corner position in the height axis

    def to_ordered_string(self, order=None):
        """
        Create a string from the corner position with named values in a given order.
        :param order: list of strings of named values, eg. ["length", "width", "height"]
        :return: A string describing the corner position.
        """
        if order is None:
            order = ["length", "width", "height"]
        d = {"length": self.length,
             "width": self.width,
             "height": self.height_level}
        return f"{order[0]}={d[order[0]]},{order[1]}={d[order[1]]},{order[2]}={d[order[2]]}"

    def to_str_with_real_dimensions(self, const_height):
        """
        Create a string from the corner position. The height level is scaled to real height. An order of dimensions
        is like in input file.
        :return: A string describing the corner position.
        """
        return f"{self.width},{self.height_level * const_height},{self.length}"

    def __str__(self):
        """
        Create a string from the corner position. Used when call print(corner position).
        :return: A string describing the corner position.
        """
        return self.to_ordered_string()


if __name__ == "__main__":
    pass
