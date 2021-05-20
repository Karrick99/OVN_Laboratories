import core.Elements as elems
import numpy as np
import matplotlib.pyplot as plt


N = elems.Network()

#lista = N.find_paths("A", "D")
#print(lista)

N.draw()

a = N.find_best_snr("A", "E")
print(a)
