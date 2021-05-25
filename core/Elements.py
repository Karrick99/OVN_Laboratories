#
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


class Signal_information:
    def __init__(self, signal_power, path):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path: str = path

    def update_pwr(self, signal_pwr_incr):
        self.signal_power = self.signal_power + signal_pwr_incr

    def update_noise(self, noise_pwr_incr):
        self.noise_power = self.noise_power + noise_pwr_incr

    def update_latency(self, latency_incr):
        self.latency = self.latency + latency_incr

    def update_path(self):
        self.path = self.path[1:]

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
        if len(signal_inf_obj.path) > 1:
            line_label = signal_inf_obj.path[0] + signal_inf_obj.path[1]
            signal_inf_obj.update_path()
            next_line = self.successive[line_label]
            signal_inf_obj = next_line.propagate(signal_inf_obj)
        return signal_inf_obj

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
        next_node = self.successive[signal_inf_obj.path[0]]
        signal_inf_obj = next_node.propagate(signal_inf_obj)
        return signal_inf_obj


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

        # creation of the pandas dataframe:

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
                        for i in range(len(p) - 1):
                            line_temp = self.nodes[p[i]].get_successive(p[i] + p[i + 1])
                            total_latency += line_temp.latency_generation()
                            total_noise += line_temp.noise_generation(1e-4)

                        # CALCOLO DEL SNR
                        if total_noise != 0:
                            snr = 10 * np.log10(10e-4 / total_noise)

                        temp_row = [path_sep.join(p), total_latency, total_noise, snr]
                        tab.append(temp_row)

        self.weighted_paths = pd.DataFrame(tab, columns=columns_list)

        # print(self.weighted_paths)
        # print(self.weighted_paths.path.values)

    def __distance(self, pos1, pos2):
        dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        return dist

    def connect(self):
        """sets the 'successive' attribute of nodes and lines as a dictionary"""

        for key1 in self.nodes:
            n = self.nodes[key1]
            for key2 in n.connected_nodes:
                n.set_successive(key1 + key2, self.lines[key1 + key2])
                self.lines[key1 + key2].set_successive(key2, self.nodes[key2])

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
        path_to_propagate : str = signal_inf_obj.get_path()
        label = path_to_propagate[0]
        # modificata qua:
        return self.nodes[label].propagate(signal_inf_obj)

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

    def find_best_snr(self, input_node, output_node):
        # migliorabile/ottimizzabile
        """Returns the path with highest latency from input_node to output_node"""
        paths = self.weighted_paths.path.values
        best_snr = 0.0
        best_snr_path = ""
        for p in paths:
            if p[0] == input_node and p[-1] == output_node:
                current_snr = self.weighted_paths.loc[self.weighted_paths['path'] == p]['SNR [dB]'].values[0]
                if best_snr < current_snr:
                    best_snr = current_snr
                    best_snr_path = p.replace('->', '')

        return best_snr_path

    def find_best_latency(self, input_node, output_node):
        # migliorabile/ottimizzabile
        """Returns the path with lowest latency from input_node to output_node"""
        paths = self.weighted_paths.path.values

        # vedere se è corretto:
        best_latency = sys.float_info.max

        best_latency_path = ""
        for p in paths:
            if p[0] == input_node and p[-1] == output_node:
                current_latency = self.weighted_paths.loc[self.weighted_paths['path'] == p]['total latency'].values[0]
                if best_latency > current_latency:
                    best_latency = current_latency
                    best_latency_path = p.replace('->', '')
        return best_latency_path

    def stream(self, connections_list, parameter='latency'):
        processed_conn = []
        for conn in connections_list:
            input_node = conn.input
            output_node = conn.output
            signal_power = conn.signal_power
            if parameter == 'snr':
                path = self.find_best_snr(input_node, output_node)
            elif parameter == 'latency':
                path = self.find_best_latency(input_node, output_node)
            else:
                print("Parameter not recognized (it should be 'snr' or 'latency')")
                return []

            if len(path) > 1:
                # futuri task
                input_signal = Signal_information(signal_power, path)
                output_signal = self.propagate(input_signal)
                conn.latency = output_signal.latency

                if output_signal.noise_power != 0:
                    conn.snr = 10 * np.log10(signal_power / output_signal.noise_power)

            else:
                conn.latency = 0
                conn.snr = 0

            processed_conn.append(conn)

        return processed_conn


class Connection:
    def __init__(self, input, output, signal_power):
        self.input: str = input
        self.output: str = output
        self.signal_power: float = signal_power
        self.latency: float = 0
        self.snr: float = 0


if __name__ == '__main__':
    N = Network()
    # print(N.weighted_paths)
    # var = N.weighted_paths[N.weighted_paths.where(
    # N.weighted_paths['path'][0] == 'A' and N.weighted_paths['path'][-1] == 'D')]
    # print(N.weighted_paths['path'][0] == 'A' and N.weighted_paths['path'][-1] == 'D')

    conn_list = [Connection('A', 'F', 1e-4), Connection('C', 'D', 2e-4), Connection("F", "B", 3e-4)]

    a = N.stream(conn_list, 'latency')
    print(a[0].snr)

    # ancora da fare commit del Connection funzionante

    # problema [RISOLTO!]: il path nell'oggetto Signal_information è come lista,
    # ma noi lo prendiamo/usiamo come stringa e questo crea problemi
