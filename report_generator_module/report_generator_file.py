from datetime import datetime
import numpy as np
import os
import shutil
import cv2

from containers_module.containers_manager_file import ContainersManager, Container
from ships_module.ships_manager_file import ShipsManager, Ship
from optimizer_module.shipments_manager_file import Shipment
from optimizer_module.placed_container_file import PlacedContainer
from optimizer_module.corner_position_file import CornerPosition
from optimizer_module.optimizer_selector_file import OptimizerSelector


class ReportGenerator:
    """
    Class used for logging and generating report.
    """
    def __init__(self, dirname="log", filename="log.txt", if_log_to_file=True, if_print=True):
        """
        Constructor.
        :param dirname: a directory in which logs will be created
        :param filename: a basename of a file to which logs will be written
        :param if_log_to_file: (bool) if log to file
        :param if_print: (bool) if log using print
        """
        self.if_log_to_file = if_log_to_file                    # (bool) if log to file
        self.if_print = if_print                                # (bool) if log using print
        self.root = "log"                                       # a main directory for all logs
        self.dirname = os.path.join(self.root, dirname)         # a directory in which logs will be created
        self.filename = os.path.join(self.dirname, filename)    # a file to which logs will be written
        self.logfile = None                                     # an opened log file

        self.start_datetime = None                          # start datetime
        self.stop_datetime = None                           # stop datetime
        self.optimization_start_datetime = None             # optimization start datetime
        self.optimization_stop_datetime = None              # optimization stop datetime
        self.indentation = 0                                # indentation number

        self.shipments_list = []                            # list of sent shipments

    def __enter__(self):
        """
        Open a log file. Used automatically at the beginning of "with".
        :return: a report generator with opened log file
        """
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        if os.path.exists(self.dirname):
            shutil.rmtree(self.dirname)
        os.mkdir(self.dirname)
        self.logfile = open(self.filename, "a+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close log file. Used automatically at the end of "with".
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.logfile.close()

    def new_section(self):
        """
        Log new section.
        :return:
        """
        self.log("")
        self.log("****************************************************************************************************")
        self.log("")

    def indent(self, indentation):
        """
        Set indentation.
        :param indentation: an indentation to set
        :return:
        """
        self.indentation = indentation

    def increase_indent(self):
        """
        Increase indentation.
        :return:
        """
        self.indentation += 1

    def decrease_indent(self):
        """
        Decrease indentation.
        :return:
        """
        if self.indentation > 0:
            self.indentation -= 1

    def log(self, text, additional_indent=0, new_section=False, temp_line=False):
        """
        Log a message.
        :param text: a message to log
        :param additional_indent: number of additional indentations
        :param new_section: (bool) if call new_section() at the beginning
        :param temp_line: (bool) if True, the line will be only printed (not written to file) and will be overwritten by a next log
        :return:
        """
        end = "\r" if temp_line else "\n"
        if new_section:
            self.new_section()
        for _ in range(additional_indent + self.indentation):
            text = "\t" + text
        if self.if_log_to_file and not temp_line:
            self.logfile.write(text + "\n")
        if self.if_print:
            print(text, end=end)

    @staticmethod
    def datetime2str(x):
        """
        Convert a datetime to a string.
        :param x: a datetime
        :return: a string
        """
        return x.strftime("%Y.%m.%d %H:%M:%S")

    def start(self, ships_manager, containers_manager, optimizer):
        """
        Log start of the program.
        :param ships_manager: ships manager
        :param containers_manager: containers manager
        :param optimizer: optimizer
        :return:
        """
        self.start_datetime = datetime.now()
        self.log(f"Started at {self.datetime2str(self.start_datetime)}")
        self.new_section()
        self.log("Ships settings:")
        self.increase_indent()
        self.log(f"Maximum number of available ships = {ships_manager.max_available}")
        self.log(f"Acceptable length range = ({ships_manager.min_length}, {ships_manager.max_length})")
        self.log(f"Acceptable width range = ({ships_manager.min_width}, {ships_manager.max_width})")
        self.log(f"Acceptable height range = ({ships_manager.min_height}, {ships_manager.max_height})")
        self.decrease_indent()
        self.log("Containers settings:")
        self.increase_indent()
        self.log(f"Acceptable length range = ({containers_manager.min_length}, {containers_manager.max_length})")
        self.log(f"Acceptable width range = ({containers_manager.min_width}, {containers_manager.max_width})")
        self.log(f"Acceptable height range = ({containers_manager.min_height}, {containers_manager.max_height})")
        self.decrease_indent()
        self.log(optimizer.info())

    def stop(self):
        """
        Log stop of the program.
        :return:
        """
        self.stop_datetime = datetime.now()
        delta_time = self.stop_datetime - self.start_datetime
        self.new_section()
        self.log(f"Whole time = {str(delta_time)}")
        self.log(f"Finished at {self.datetime2str(self.stop_datetime)}")

    def add_ship(self, line, timestamp, ship):
        """
        Log adding a ship.
        :param line: a line generating a ship
        :param timestamp: a timestamp
        :param ship: a ship or None
        :return:
        """
        if line[-1] == "\n":
            line = line[0:-1]
        if ship is not None:
            self.log(f"Successfully added a ship {line} with timestamp {timestamp}.")
        else:
            self.log(f"A ship not added. The line {line} is incorrect. "
                     f"The id must be unique, "
                     f"the dimensions must be in the acceptable range.")

    def add_container(self, line, min_timestamp, container):
        """
        Log adding a container.
        :param line: a line generating a container
        :param min_timestamp: a timestamp
        :param container: a container or None
        :return:
        """
        if line[-1] == "\n":
            line = line[0:-1]
        if container is not None:
            self.log(f"Successfully added a container {line}.")
        else:
            self.log(f"A container not added. The line {line} is incorrect. "
                     f"The id must be unique, "
                     f"the dimensions must be in the acceptable range "
                     f"and the timestamp must be greater than or equal to {min_timestamp}")

    def data_summary(self, ships_manager, containers_manager):
        """
        Log data summary.
        :param ships_manager: ships manager
        :param containers_manager: containers manager
        :return:
        """
        self.new_section()
        self.log("Data summary:")
        self.increase_indent()

        self.log(f"Ships ({len(ships_manager.ships)}):")
        self.increase_indent()
        for s in ships_manager.ships:
            self.log(f"{s.to_str_with_timestamp()}")
        self.decrease_indent()

        self.log(f"Containers ({len(containers_manager.waiting_containers)}):")
        self.increase_indent()
        for c in containers_manager.waiting_containers:
            self.log(f"{c}")
        self.decrease_indent()

        self.decrease_indent()

    def start_optimization(self):
        """
        Log start optimization.
        :return:
        """
        self.optimization_start_datetime = datetime.now()
        self.new_section()
        self.log(f"Started optimization at {self.datetime2str(self.optimization_start_datetime)}")
        self.log("")
        self.increase_indent()

    def stop_optimization(self):
        """
        Log stop optimization.
        :return:
        """
        self.decrease_indent()
        self.optimization_stop_datetime = datetime.now()
        delta_time = self.optimization_stop_datetime - self.optimization_start_datetime
        self.log("")
        self.log(f"Optimization time = {str(delta_time)}")
        self.log(f"Finished optimization at {self.datetime2str(self.optimization_stop_datetime)}")

    @staticmethod
    def shipment2str(shipment):
        """
        Convert a shipment to a string.
        :param shipment: a shipment
        :return: a string
        """
        full_volume = shipment.get_full_volume()
        empty_volume = shipment.get_empty_volume()
        return f"Shipment (ship = s{shipment.ship.sid}, " \
               f"empty volume = {empty_volume} ({round(100 * empty_volume / full_volume, 2)}% of full volume), " \
               f"containers number = {len(shipment.get_all_containers())}): " \
               f"{shipment.get_all_containers()}"

    def send_containers(self, timestamp, available_ships, completed_shipments, uncompleted_shipment=None):
        """
        Log sending containers.
        :param timestamp: a main shipment timestamp
        :param available_ships: a list of available ships
        :param completed_shipments: a list of completed shipments
        :param uncompleted_shipment: an uncompleted shipment
        :return:
        """
        self.log(f"Sending containers for timestamp {timestamp}")
        self.increase_indent()
        self.log(f"Available ships: {available_ships}")
        if len(completed_shipments) > 0:
            first_shipment = completed_shipments[0]
            if first_shipment.ship not in available_ships:
                completed_shipments = completed_shipments[1:]
                self.log("Previous shipment:")
                self.log(self.shipment2str(first_shipment), additional_indent=1)
            if len(completed_shipments) > 0:
                self.log("Completed shipments:")
                self.increase_indent()
                for shipment in completed_shipments:
                    self.shipments_list.append(shipment)
                    self.log(self.shipment2str(shipment))
                self.decrease_indent()
        if uncompleted_shipment is not None:
            self.log("Uncompleted shipment:")
            self.log(self.shipment2str(uncompleted_shipment), additional_indent=1)
        self.decrease_indent()
        self.log("")

    def draw_level_arrangement(self, img, placed_containers, scale=20, line_width=4, margin_value=32):
        """
        Draw arrangement of a single level
        :param img: an image with lower levels
        :param placed_containers: a list of placed containers
        :param scale: a scale of an image
        :param line_width: a line width
        :param margin_value: a margin value
        :return: an image with lower levels and the current one
        """
        used_color = [180, 230, 25]
        used_lines_color = (int(used_color[0] / 2), int(used_color[1] / 2), int(used_color[2] / 2))
        unused_color = [25, 60, 230]
        margin_color = [40, 60, 100]
        font = cv2.FONT_HERSHEY_SIMPLEX

        img = np.repeat(img, scale, axis=0).astype(np.uint8)
        img = np.repeat(img, scale, axis=1)

        ones = np.ones_like(img, dtype=np.uint8)
        used = np.dstack((used_color[0] * ones, used_color[1] * ones, used_color[2] * ones))
        unused = np.dstack((unused_color[0] * ones, unused_color[1] * ones, unused_color[2] * ones))

        img = np.dstack((img, img, img))
        img = np.where(img == 1, used, unused)
        shape = np.shape(img)
        for pl_cont in placed_containers:
            w1 = pl_cont.corner1.width * scale
            l1 = pl_cont.corner1.length * scale
            w2 = pl_cont.corner2.width * scale
            l2 = pl_cont.corner2.length * scale
            cv2.rectangle(img, (w1, l1), (w2, l2), used_lines_color, line_width)
            if pl_cont.container.width > 5 and pl_cont.container.length > 5:
                font_size = 2.0
                thickness = 4
            elif pl_cont.container.width > 2 and pl_cont.container.length > 2:
                font_size = 1.0
                thickness = 2
            else:
                font_size = 0.5
                thickness = 1
            cv2.putText(img, f"c{pl_cont.container.cid}", (w1 + line_width, l2 - line_width),
                        font, font_size, used_lines_color, thickness, cv2.LINE_AA)

        shift_margin = int(margin_value / 2)
        full_img = np.ones(shape=(shape[0] + margin_value, shape[1] + margin_value), dtype=np.uint8)
        full_img = np.dstack((margin_color[0] * full_img, margin_color[1] * full_img, margin_color[2] * full_img))
        full_img[shift_margin:shift_margin + shape[0], shift_margin:shift_margin + shape[1], :] = img

        return full_img

    def draw_shipment_arrangement(self, shipment):
        """
        Draw arrangement of a single shipment.
        :param shipment: a single shipment
        :return: an image if an arrangement
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = self.draw_level_arrangement(shipment.occupancy_map[0], shipment.placed_containers_levels[0])

        zeros = np.zeros(shape=(50, np.shape(img)[1], 3), dtype=np.uint8)
        cv2.putText(zeros, f"s{shipment.ship.sid}", (5, 45), font, 2, (0, 220, 220), 8, cv2.LINE_AA)

        img = np.vstack((img, zeros))
        for i in range(1, shipment.levels_nr):
            level_img = self.draw_level_arrangement(shipment.occupancy_map[i], shipment.placed_containers_levels[i])
            img = np.vstack((level_img, img))
        return img

    def draw_arrangement(self):
        """
        Draw arrangement of all shipments.
        :return:
        """
        length = len(self.shipments_list)
        self.increase_indent()
        for i, shipment in enumerate(self.shipments_list):
            self.log(f"Draw a shipment {i+1}/{length}.")
            shipment_img = self.draw_shipment_arrangement(shipment)
            filename = os.path.join(self.dirname, f"arrangement_t{max(shipment.get_timestamps_set())}.png")
            if os.path.exists(filename):
                img = cv2.imread(filename)
                img_h = np.shape(img)[0]
                shipment_img_h = np.shape(shipment_img)[0]
                if img_h > shipment_img_h:
                    zeros = np.zeros(shape=(img_h - shipment_img_h, np.shape(shipment_img)[1], 3), dtype=np.uint8)
                    shipment_img = np.vstack((zeros, shipment_img))
                elif img_h < shipment_img_h:
                    zeros = np.zeros(shape=(shipment_img_h - img_h, np.shape(img)[1], 3), dtype=np.uint8)
                    img = np.vstack((zeros, img))
                img = np.hstack((img, shipment_img))
            else:
                img = shipment_img
            cv2.imwrite(filename, img)
        self.decrease_indent()

    def generate_report(self):
        """
        Generate report.
        :return:
        """
        self.new_section()
        self.log("Report generating\n")

        self.log("Drawing images...")
        self.draw_arrangement()

        self.log("")
        self.log("Report for ships")
        ships_dict = {}
        for shipment in self.shipments_list:
            ship = shipment.ship
            if ship in ships_dict.keys():
                ships_dict[ship].append(shipment)
            else:
                ships_dict[ship] = [shipment]
        for ship in ships_dict.keys():
            shipments = ships_dict[ship]
            available_volume = shipments[0].get_full_volume(only_used_levels=True)
            full_volume = shipments[0].get_full_volume(only_used_levels=False)
            unavailable = round(100 * (full_volume - available_volume) / full_volume, 2)
            self.log(f"Ship {ship} was sent {len(shipments)} times. {unavailable}% of full volume is unavailable "
                     f"due to const containers height.")
            self.increase_indent()
            for sh in shipments:
                self.log(self.shipment2str(sh))
            self.decrease_indent()

        self.log("")
        self.log("Summary")
        sent_containers = sum([len(sh.get_all_containers()) for sh in self.shipments_list])
        self.log(f"Sent {sent_containers} containers in {len(self.shipments_list)} shipments.")

        full_volume = sum([sh.get_full_volume() for sh in self.shipments_list])
        empty_volume = sum([sh.get_empty_volume() for sh in self.shipments_list])
        used_volume = full_volume - empty_volume
        self.log(f"Used {round(100 * used_volume / full_volume, 2)}% of ships volume.")
        self.log(f"Empty volume is {round(100 * empty_volume / used_volume, 2)}% of containers volume.")
        self.log(f"Empty volume is about {int(empty_volume/100)} thous. ({empty_volume}).")

        self.log("")
        self.log("If we skip a surplus of a height")
        full_volume = sum([sh.get_full_volume(only_used_levels=True) for sh in self.shipments_list])
        empty_volume = sum([sh.get_empty_volume(only_used_levels=True) for sh in self.shipments_list])
        used_volume = full_volume - empty_volume
        self.log(f"Used {round(100 * used_volume / full_volume, 2)}% of ships volume.")
        self.log(f"Empty volume is {round(100 * empty_volume / used_volume, 2)}% of containers volume.")
        self.log(f"Empty volume is about {int(empty_volume/100)} thous. ({empty_volume}).")


def save_img(img, scale, filename, line_width=None):
    if line_width is None:
        line_width = int(scale / 10)
    img = np.repeat(img, scale, axis=0)
    img = np.repeat(img, scale, axis=1)
    img = np.dstack((img, img, img))
    img = (255 * img).astype(np.uint8)
    shape = np.shape(img)
    cv2.rectangle(img, (0, 0), (shape[1], shape[0]), (0, 0, 255), line_width)
    cv2.imwrite(filename, img)


def number2str(nr, length=6):
    str_nr = str(nr)
    while len(str_nr) < length:
        str_nr = f"0{str_nr}"
    return str_nr


def test2():
    print(number2str(2))
    print(number2str(211))
    a = np.array([[0, 1, 0, 0],
                  [0, 1, 1, 0],
                  [1, 0, 1, 0]])
    print(a)
    save_img(a, 100, "haha.png")


def test():
    with ReportGenerator() as rg:
        sm = ShipsManager(max_available=3)
        cm = ContainersManager()
        rg.start(sm, cm, OptimizerSelector.select(0))

        rg.new_section()

        s1 = Ship(sid=1, length=100, width=100, height=100, timestamp=10)
        s2 = Ship(sid=2, length=100, width=100, height=100, timestamp=10)
        s3 = Ship(sid=3, length=100, width=100, height=100, timestamp=10)

        sh1 = Shipment(ship=s1, containers_height=10)
        sh2 = Shipment(ship=s2, containers_height=10)
        sh3 = Shipment(ship=s1, containers_height=10)
        sh4 = Shipment(ship=s1, containers_height=10)

        sh1.check_and_add(PlacedContainer(container=Container(cid=1, length=1, width=3, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=0, length=0, width=0)))
        sh1.check_and_add(PlacedContainer(container=Container(cid=2, length=1, width=1, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=0, length=1, width=0)))
        sh2.check_and_add(PlacedContainer(container=Container(cid=3, length=2, width=2, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=0, length=0, width=0)))
        sh2.check_and_add(PlacedContainer(container=Container(cid=4, length=1, width=1, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=1, length=0, width=0)))
        sh3.check_and_add(PlacedContainer(container=Container(cid=5, length=15, width=7, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=0, length=0, width=0)))
        sh4.check_and_add(PlacedContainer(container=Container(cid=6, length=1, width=1, height=10, timestamp=39),
                                          corner1=CornerPosition(height_level=0, length=0, width=0)))

        rg.send_containers(timestamp=39,
                           available_ships=[s1, s2, s3],
                           completed_shipments=[sh1, sh2, sh3],
                           uncompleted_shipment=sh4)

        rg.stop()
        rg.log("haha", temp_line=True)
        rg.log("b", temp_line=True)


if __name__ == "__main__":
    test()
    #print("\thaha", end="\r")
    #print("\tb", end="\n")
