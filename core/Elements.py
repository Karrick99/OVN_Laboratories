#
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

    def set_successive(self, line_label, line_obj):
        self.successive[line_label] = line_obj

    def get_successive(self, line_label):
        return self.successive[line_label]


class Line:
    """Connection between two nodes"""

    def __init__(self, label, length):
        # potrebbe servire costruttore per assegnare length e lable
        self.label = label
        self.length = length
        self.successive = {}

    def set_successive(self, node_label, node_obj):
        self.successive[node_label] = node_obj

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

        #creation of the pandas dataframe:


        path_sep = "->"
        tab = []
        # ogni volta che finisco temp_row
        # faccio tab.append(temp_row)
        # alla fine faccio self.weighted_paths = pd.DataFrame(tab, columns_list)

        self.connect()

        columns_list = ["path", "total latency", "total noise", "SNR [dB]"]

        for key1 in self.nodes:
            for key2 in self.nodes:
                if key1 != key2:
                    for p in self.find_paths(key1, key2):
                        total_latency = 0
                        total_noise = 0
                        snr = 0
                        # for every line in path, add its latency and noise
                        for i in range(len(p)-1):
                            line_temp = self.nodes[p[i]].get_successive(p[i]+p[i+1])
                            total_latency += line_temp.latency_generation()
                            total_noise += line_temp.noise_generation(1)

                        # CALCOLO DEL SNR
                        if total_noise != 0 :
                            snr = 10 * np.log(1 / total_noise)

                        temp_row = [path_sep.join(p), total_latency, total_noise, snr]
                        tab.append(temp_row)

        self.weighted_paths = pd.DataFrame(tab)
        self.weighted_paths.columns = columns_list

        print(self.weighted_paths)

    def __distance(self, pos1, pos2):
        dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        return dist

    def connect(self):
        """sets the 'successive' attribute of nodes and lines as a dictionary"""

        for key1 in self.nodes:
            n = self.nodes[key1]
            for key2 in n.connected_nodes:
                n.set_successive(key1+key2, self.lines[key1+key2])
                self.lines[key1+key2].set_successive(key2, self.nodes[key2])



    def paths_search(self, target, stack, paths):
        current = self.nodes[stack[-1]]
        if current.label != target:
            for n in current.connected_nodes:
                if n not in stack:
                    stack.append(n)
                    self.paths_search(target, stack, paths)
                    stack.pop()
        else:
            new_path = stack[:]
            paths.append(new_path)
            return

        return

    def find_paths(self, src, target):
        """returns the list of all paths between s1 and s2"""
        paths = []
        stack = [src]

        if target not in self.nodes.keys():
            return paths

        self.paths_search(target, stack, paths)
        return paths

    def propagate(self, signal_inf_obj):
        """Propagates the signal_information object through path """
        label = signal_inf_obj.get_path[0]
        self.nodes[label].propagate(signal_inf_obj)

    def draw(self):

        for key in self.lines:
            nodes_string = self.lines[key].label
            n1 = nodes_string[0]
            n2 = nodes_string[1]
            xvals = self.nodes[n1].get_position()[0], self.nodes[n2].get_position()[0]
            yvals = self.nodes[n1].get_position()[1], self.nodes[n2].get_position()[1]
            plt.plot(xvals, yvals, 'y', linewidth=2, markersize=12)
        for key in self.nodes:
            x, y = self.nodes[key].get_position()
            plt.plot(x, y, 'bo')
            plt.annotate(text=self.nodes[key].label, xy=(x, y), xytext=(x + 10000, y + 10000))

        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()



    