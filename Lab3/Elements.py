#

class Signal_information:
    def __init__(self, signal_power, path = []):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path = "ABCDEF"

class Node :
    def __init__(self, dict):
            self.dict = {}

