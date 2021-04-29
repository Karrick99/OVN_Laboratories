#

class Signal_information:
    def __init__(self, signal_power : float):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path = []

    def update_pwr(self, signal_pwr_incr):
        self.signal_power = self.signal_power + signal_pwr_incr

    def update_noise(self, noise_pwr_incr):
        self.noise_power = self.noise_power + noise_pwr_incr

    def update_latency(self, latency_incr):
        self.latency = self.latency + latency_incr

    def update_path(self):
        self.path.pop(0)



class Node :
    def __init__(self, dict):
            self.label = dict['label']
            self.position = dict['position']
            self.connected_nodes = dict['connected_nodes']
            self.successive = {}

    def propagate(self, signal_inf_obj):

        line_lable = signal_inf_obj.path[0]+signal_inf_obj.path[1]
        line = self.successive[line_lable]
        signal_inf_obj.update_path()
        line.propagate(signal_inf_obj)



class Line:
    def __init__(self):
        self.label = []
        self.length = 0.0
        self.successive = {}

    def latency_generation(self, signal_inf_obj):
        signal_inf_obj.update_latency()
        return float



class Network:
    def __init__(self):
        nodes = {Node}
        lines = {Line}
