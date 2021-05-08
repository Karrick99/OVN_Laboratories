#
import json
import math


class Signal_information:
    def __init__(self, signal_power, path):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path = path[:]

    def update_pwr(self, signal_pwr_incr):
        self.signal_power = self.signal_power + signal_pwr_incr

    def update_noise(self, noise_pwr_incr):
        self.noise_power = self.noise_power + noise_pwr_incr

    def update_latency(self, latency_incr):
        self.latency = self.latency + latency_incr

    def update_path(self):
        self.path.pop(0)

    def get_path(self):
        return self.path


class Node:
    def __init__(self, key, d):
        self.label = key
        self.position = d['position'][:]
        self.connected_nodes = d['connected_nodes'][:]
        self.successive = {}

    def propagate(self, signal_inf_obj):
        """propagates the signal to the end of the path"""

        line_lable = signal_inf_obj.path[0] + signal_inf_obj.path[1]
        signal_inf_obj.update_path()
        next_element = self.successive[line_lable]
        next_element.propagate(signal_inf_obj)

    def get_position(self):
        return self.position

    def get_connected_nodes(self):
        return self.connected_nodes


class Line:
    """Connection between two nodes"""

    def __init__(self, label, length):
        # potrebbe servire costruttore per assegnare length e lable
        self.label = label
        self.length = length
        self.successive = {}

    def latency_generation(self):
        t = self.length / ((5 * 10 ** 5) * 2 / 3)
        return t

    def noise_generation(self, signal_power):
        n = signal_power * self.length * 1e-9
        return n

    def propagate(self, signal_inf_obj):
        signal_inf_obj.update_latency(self.latency_generation())
        signal_inf_obj.update_noise(self.noise_generation(signal_inf_obj.signal_power))
        # signal_inf_obj.get_path[1]


class Network:
    def __init__(self):
        self.nodes = {}
        self.lines = {}

        with open("nodes.json", "r") as in_file:
            data = json.load(in_file)

        for key in data:
            self.nodes[key] = Node(key, data[key])

        for key in self.nodes:
            for target in self.nodes[key].get_connected_nodes():
                self.lines[key + target] = Line(key + target,
                                                self.__distance(self.nodes[key].get_position(),
                                                                self.nodes[target].get_position()))

    def __distance(self, pos1, pos2):
        dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        return dist
