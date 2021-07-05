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
bit_rates = []
total_capacity = 0.0

while i < 100:
    n1 = random.choices(nodes)[0]
    n2 = random.choices(nodes)[0]
    if n1 != n2:
        conn = elems.Connection(n1, n2, 1e-3)

        param = 'snr'

        N.stream([conn], param)

        # control to avoid errors in hist caused by saturation
        if conn.bit_rate is not None and conn.snr != 0:
            snrs.append(conn.snr)
            bit_rates.append(conn.bit_rate/1e9)
        # print(conn.snr)
        # print(conn.bit_rate)
        i = i + 1

plt.hist(snrs)
plt.xlabel('snr [dB]')
plt.ylabel('cases')
plt.show()

plt.hist(bit_rates)
plt.xlabel('bit_rate [Gbps]')
plt.ylabel('cases')
plt.show()

print(N.weighted_paths)



print(N.route_space)