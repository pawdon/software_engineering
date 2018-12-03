from .corner_position_file import CornerPosition
from containers_module.container_file import Container


class PlacedContainer:
    """
    Class used for storing information about a container and its position.
    """
    def __init__(self, container, corner1):
        """
        Constructor.
        :param container: a container
        :param corner1: a corner position with lower length, width and height_level
        """
        self.container = container                                                  # a container
        self.corner1 = corner1                                                      # the first corner position
        self.corner2 = CornerPosition(length=corner1.length + container.length,     # the second corner position
                                      width=corner1.width + container.width,
                                      height_level=corner1.height_level)

    def __str__(self):
        """
        Create a string from the placed container. Used when call print(placed container).
        :return: A string describing the placed container.
        """
        order = ["height", "length", "width"]
        return f"Container ({self.container.to_ordered_string(order)}) at ({self.corner1.to_ordered_string(order)})"

    def __repr__(self):
        """
        Create a string from the placed container. Used when call print(list of placed container).
        :return: A string describing the placed container.
        """
        return self.__str__()

    def get_shifted_copy(self, diff_length=0, diff_width=0, diff_height_level=0):
        """
        Get shifted copy of the placed container.
        :param diff_length: difference between a current position in the length axis and a new one
        :param diff_width: difference between a current position in the width axis and a new one
        :param diff_height_level: difference between a current position in the height axis and a new one
        :return: a shifted copy of a placed container
        """
        return PlacedContainer(container=self.container,
                               corner1=CornerPosition(length=self.corner1.length + diff_length,
                                                      width=self.corner1.width + diff_width,
                                                      height_level=self.corner1.height_level + diff_height_level))


if __name__ == "__main__":
    pass
