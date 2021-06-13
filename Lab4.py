from typing import List

import core.Elements as elems
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

N = elems.Network()

i = 0

nodes = list(N.nodes.keys())
param = ''
snrs = []

while i < 100:
    n1 = random.choices(nodes)[0]
    n2 = random.choices(nodes)[0]
    if n1 != n2:
        conn = elems.Connection(n1, n2, 1)

        param = 'snr'

        N.stream([conn], param)
        snrs.append(conn.snr)
        print(conn.snr)
        i = i + 1

plt.hist(snrs)
plt.xlabel('snr')
plt.ylabel('cases')

print(N.weighted_paths)

plt.show()

print(N.route_space)