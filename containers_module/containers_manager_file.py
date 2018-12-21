from .container_file import Container


class ContainersManager:
    """
    Class used for storing a list of containers,
    checking if a container has correct values,
    and managing information about which containers are waiting for sending and which ones have been already sent.
    """
    def __init__(self, **args):
        """
        Constructor.
        :param args: an optional dictionary used for changing default values
        """
        self.waiting_containers = []    # list of containers waiting for sending
        self.sent_containers = []       # list of sent containers

        self.const_h = None             # constant height of containers

        # default values defining a correct container
        self.min_length = args.get("min_length", 1)
        self.max_length = args.get("max_length", 40)
        self.min_width = args.get("min_width", 1)
        self.max_width = args.get("max_width", 40)
        self.min_height = args.get("min_height", 1)
        self.max_height = args.get("max_height", 40)

    def __str__(self):
        """
        Create a string from the containers manager. Used when call print(containers manager).
        :return: A string describing the containers manager.
        """
        return "\n\t".join([f"Waiting containers ({len(self.waiting_containers)})"]
                           + [str(x) for x in self.waiting_containers]) + "\n" + \
               "\n\t".join([f"Sent containers ({len(self.sent_containers)})"]
                           + [str(x) for x in self.sent_containers])

    def add(self, x, min_timestamp):
        """
        Create a container from a given string. Check if it is correct and if so, add to list of waiting containers.
        :param x: a string describing a container
        :param min_timestamp: minimum timestamp a container must have
        :return: a container (if successfully added) or None
        """
        if type(min_timestamp) is not int:
            return None
        container = Container.from_string(x)
        if container is not None:
            check_ok = container.timestamp >= min_timestamp and \
                       self.min_length <= container.length <= self.max_length and \
                       self.min_width <= container.width <= self.max_width and \
                       self.min_height <= container.height <= self.max_height and \
                       container.cid not in [x.cid for x in self.waiting_containers + self.sent_containers]
            if check_ok:
                if self.const_h is None:
                    self.const_h = container.height
                    self.waiting_containers.append(container)
                elif container.height == self.const_h:
                    self.waiting_containers.append(container)
                else:
                    container = None
            else:
                container = None
        return container

    def send(self, containers):
        """
        Move containers from a list of waiting containers to a list of sent containers.
        :param containers: list of containers to sent
        :return:
        """
        for container in containers:
            if container in self.waiting_containers:
                self.waiting_containers.remove(container)
                self.sent_containers.append(container)

    def get_containers(self, max_timestamp):
        """
        Get list of waiting containers with timestamp less than or equal to a given value
        :param max_timestamp: maximum timestamp
        :return: list of waiting containers
        """
        containers_list = []
        for container in self.waiting_containers:
            if container.timestamp <= max_timestamp:
                containers_list.append(container)
            else:
                break
        return containers_list


def test2():
    cm = ContainersManager()
    cm.add("c10,1,2,2,2", min_timestamp=0)
    cm.add("c11,1,2,2,2", min_timestamp=2)
    cm.add("c12,1,2,2,3", min_timestamp=2)
    cm.add("c13,1,2,2,3", min_timestamp=3)
    cm.add("c14,1,2,2,4", min_timestamp=3)
    cm.add("c15,1,2,2,3", min_timestamp=4)
    cm.add("c16,41,2,2,4", min_timestamp=4)
    cm.add("c14,2,2,2,4", min_timestamp=4)
    print(cm)
    containers = cm.get_containers(max_timestamp=3)
    print(containers)
    cm.send([containers[1], containers[2]])
    print(cm)


if __name__ == "__main__":
    test2()
