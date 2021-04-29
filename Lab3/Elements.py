#

class Signal_information:
    def __init__(self, signal_power, path = []):
        self.signal_power = signal_power
        self.noise_power = 0.0
        self.latency = 0.0
        self.path = []

    def updatePwr(self, signalPwrIncr):
        self.signal_power = self.signal_power + signalPwrIncr

    def updateNoise(self, noisePwrIncr):
        self.noise_power = self.noise_power + noisePwrIncr

    def updateLatency(self, latencyIncr):
        self.latency = self.latency + latencyIncr

    def updatePath(self, newPath):
        self.path.pop(0)



class Node :
    def __init__(self, dict):
            self.label = dict['label']
            self.position = dict['position']
            self.connected_nodes = dict['connected_nodes']
            self.successive = {}

    def propagate(self, signalInfObj):
        signalInfObj.updatePath()
        path = signalInfObj.path[0]

        #here I have to refer to the next node:
        path.propagate()


class Line:
    def __init__(self):

