from typing import List

import core.Elements as elems
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

N = elems.Network()

i = 0
snrs = []
bit_rates = []
total_capacity = 0.0

nodes = list(N.nodes.keys())
T = pd.DataFrame(columns=nodes, index=nodes)

# totally random situation:

# for M in range(1, 10):
#    for i in nodes:
#        for j in nodes:
#            x = random.randint(1, 3)
#            if i == j:
#                T.at[i, j] = 0
#            elif x == 1:
#                T.at[i, j] = 0
#            elif x == 2:
#                T.at[i, j] = np.Inf
#            elif x == 3:
#                T.at[i, j] = M * 100e9

# uniform traffic matrix

processed_conn_list = []

for M in range(1, 10):
    for i in nodes:
        for j in nodes:
            if i == j:
                T.at[i, j] = 0
            else:
                T.at[i, j] = M * 100e9

    returned_data = N.manage_connection_from_traffic_matrix(T)

    if returned_data == 13:
        print('SATURATION WITH M = ', end='')
        print(M)
        break
    elif returned_data != 0:
        processed_conn_list += returned_data

for conn in processed_conn_list:
    snrs.append(conn.snr)
    bit_rates.append(conn.bit_rate)

print(T)

average_bit_rate = sum(bit_rates) / len(processed_conn_list)
total_capacity = sum(bit_rates)

print(N.weighted_paths)

print(N.route_space)

print('Total capacity = ', end='')
print(total_capacity / 1e9, end=' ')
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
