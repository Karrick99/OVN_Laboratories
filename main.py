import core.Elements as elems
import numpy as np
import matplotlib.pyplot as plt


N = elems.Network()

# lista = N.find_paths("A", "D")
# print(lista)

# N.draw()

snr_path = N.find_best_snr("A", "E")
print(snr_path)

latency_path = N.find_best_latency("A", "E")
print(latency_path)
