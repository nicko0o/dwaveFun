from asyncio.windows_events import NULL
from socket import timeout
from dwave.samplers import TabuSampler, SteepestDescentSolver, RandomSampler, SimulatedAnnealingSampler
import numpy as np
import math
import os
import networkx as nx
import dimod


#pip install necessary dwave packages from anaconda terminal 


arr = np.fromfile('qubo-matrix.raw', dtype=np.float32)

d = int(math.sqrt(arr.size))
print(d)
arr = np.reshape(arr, (d, d))
print(arr.shape)
 
dic = {}
 
for i in range(d):
    for j in range(i, d):
        if arr[i, j] != 0:
            dic[i, j] = arr[i, j]
 



"""
from dwave.samplers import SteepestDescentSolver
solver = SteepestDescentSolver()


sampleset = solver.sample_qubo(dic, num_reads=1)
print("GRADIENT DESCENT")
print(sampleset)
print("\n")
"""

#offset = 5085508.6444301605


#solver2 = TabuSampler()
#solver2 = SteepestDescentSolver()
#solver2 = RandomSampler()
solver2 = SimulatedAnnealingSampler()

tout = None
s = 156
nr = 1
ns = 1500000
nspb = None
lso = None


#sampleset2 = solver2.sample_qubo(dic, num_reads=nr, seed=s, timeout=tout)
sampleset2 = solver2.sample_qubo(dic, num_reads=nr, seed=s, num_sweeps=ns)

print(type(solver2))

print(sampleset2, '\n')

samples = sampleset2.samples()

t0 = np.zeros(len(sampleset2.first.sample))
#t1 = np.zeros(len(sampleset2.first.sample))
#t2 = np.zeros(len(sampleset2.first.sample))

resultCount = len(os.listdir('./results'))

params = []
params.append(('result_num=', resultCount + 1))
params.append(('solver=', type(solver2)))
params.append(('timeout=', tout))
params.append(('seed=', s))
params.append(('num_reads=', nr))
params.append(('large_sparse_opt=', lso))
params.append(('num_sweeps=', ns))
params.append(('num_sweeps_per_beta=', nspb))

with open('dwave-log.txt', 'a') as f:
    for p in params:
        if p[1] is not None:
            f.write(p[0] + str(p[1]))
            f.write(', ')
    f.write('energy=' + str(sampleset2.first.energy))
    f.write('\n')

with open('dwave-result-Tabu0.txt', 'w') as f:
    for i in range(len(sampleset2.first.sample)):
        f.write(str(samples[0, i]))
        f.write('\n')
        t0[i] = samples[0, i]

fname  = 'results\dwave-result-' + str(resultCount+1) + '.txt'

with open(fname, 'w') as f:
    for i in range(len(sampleset2.first.sample)):
        f.write(str(samples[0, i]))
        f.write('\n')
        

"""
with open('dwave-result-Tabu1.txt', 'w') as f:
    for i in range(len(sampleset2.first.sample)):
        f.write(str(samples[1, i]))
        f.write('\n')
        t1[i] = samples[1, i]


with open('dwave-result-Tabu2.txt', 'w') as f:
    for i in range(len(sampleset2.first.sample)):
        f.write(str(samples[2, i]))
        f.write('\n')
        t2[i] = samples[2, i]
"""

t0 = t0.astype(int)
#t1 = t1.astype(int)
#t2 = t2.astype(int)

unique, counts = np.unique(t0, return_counts=True)
print('t0 counts: ', dict(zip(unique, counts)))
#
#unique, counts = np.unique(t1, return_counts=True)
#print('t1 counts: ', dict(zip(unique, counts)))
#
#t01 = np.bitwise_and(t0, t1)
#unique, counts = np.unique(t01, return_counts=True)
#print('t01 anded counts: ', dict(zip(unique, counts)))