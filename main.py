import Lab3.Elements as elems
import numpy as np
import matplotlib.pyplot as plt

N = elems.Network()
lista = N.find_paths("A", "D")
print(lista)

N.draw()