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

number_connections = 100

while i < number_connections:
    n1 = random.choices(nodes)[0]
    n2 = random.choices(nodes)[0]
    if n1 != n2:
        conn = elems.Connection(n1, n2, 1)

        param = 'snr'

        N.stream([conn], param)

        # control to avoid errors in hist caused by saturation
        if conn.bit_rate is not None and conn.snr != 0:
            snrs.append(conn.snr)
            bit_rates.append(conn.bit_rate / 1e9)
            total_capacity += conn.bit_rate
        # print(conn.snr)
        # print(conn.bit_rate)
        i = i + 1

average_bit_rate = sum(bit_rates)/number_connections


print(N.weighted_paths)

print(N.route_space)

print('Total capacity = ', end='')
print(total_capacity/1e9, end=' ')
print('Gbps')

print('Average bit_rate = ', end='')
print(average_bit_rate, end=' ')
print('Gbps')

plt.hist(snrs)
plt.xlabel('snr [dB]')
plt.ylabel('cases')
plt.show()

plt.hist(bit_rates)
plt.xlabel('bit_rate [Gbps]')
plt.ylabel('cases')
plt.show()

N.draw()

