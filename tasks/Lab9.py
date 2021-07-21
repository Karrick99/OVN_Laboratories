from typing import List

import core.Elements as elems
import pandas as pd
import matplotlib.pyplot as plt
import core.utils as utils
import math

N = elems.Network()

i = 0
snrs = []
gsnrs = []
bit_rates = []
m_values = [0]
free_conns = [N.total_possible_connections]
refused_conns = [0]

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

for M in range(1, 20):
    for i in nodes:
        for j in nodes:
            if i == j:
                T.at[i, j] = 0
            else:
                T.at[i, j] = M * 100e9

    pd.set_option("display.max_columns", None)
    pd.set_option('display.width', None)
    # print(T)

    returned_data = N.manage_connection_from_traffic_matrix(T)

    m_values.append(M)
    free_conns.append(returned_data[0])
    refused_conns.append(returned_data[1])

    if returned_data[2:]:
        processed_conn_list += returned_data[2:]
    if returned_data[0] == 0:
        print(utils.bcolors.YELLOW + 'SATURATION WITH M = ', end='')
        print(M)
        print(utils.bcolors.ENDC)
        print(returned_data[1], end=' ')
        print('connections have been rejected')
        break

# print(T)

occupation_percentage = []

for value in free_conns:
    occupation_percentage.append(((N.total_possible_connections-value)*100)/N.total_possible_connections)

# PLOT OF OCCUPATION PERCENTAGE:

plt.plot(m_values, occupation_percentage, marker='x', mec='r', ms=12)
m_int = range(min(m_values), math.ceil(max(m_values))+1)
plt.xticks(m_int)
plt.xlim(0, 7)
plt.xlabel('M value')
plt.ylabel('occupation percentage (/possible connections)')
plt.show()

# PLOT OF REFUSED CONNECTIONS:

plt.plot(m_values, refused_conns, marker='x', mec='r', ms=12)
m_int = range(min(m_values), math.ceil(max(m_values))+1)
plt.xticks(m_int)
plt.xlim(0, 7)
plt.xlabel('M value')
plt.ylabel('refused connections')
plt.show()


for conn in processed_conn_list:
    snrs.append(conn.snr)
    gsnrs.append(conn.gsnr)
    bit_rates.append(conn.bit_rate/1e9)


average_bit_rate = sum(bit_rates) / len(bit_rates)
average_gsnr = sum(gsnrs)/len(gsnrs)

total_capacity = sum(bit_rates)

# print(N.weighted_paths)

# print(N.route_space)

print(utils.bcolors.CYAN + 'Total capacity = ', end='')
print(total_capacity, end=' ')
print('Gbps' + utils.bcolors.ENDC)

print('Average bit_rate = ', end='')
print(average_bit_rate, end=' ')
print('Gbps')

print('Average GSNR = ', end='')
print(average_gsnr, end=' ')

plt.hist(snrs)
plt.xlabel('snr [dB]')
plt.ylabel('cases')
plt.show()

plt.hist(bit_rates)
plt.xlabel('bit_rate [Gbps]')
plt.ylabel('cases')
plt.show()

N.draw()

latencies = N.weighted_paths.loc[:, 'total latency'].values
plt.hist(latencies)
plt.xlabel('latency')
plt.ylabel('number of paths')
plt.show()

# print(utils.bcolors.YELLOW + "Text here" + utils.bcolors.ENDC)
