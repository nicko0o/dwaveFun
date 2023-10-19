from asyncio.windows_events import NULL
from socket import timeout
from dwave.samplers import SteepestDescentSolver, SimulatedAnnealingSampler
import numpy as np
import math
import os

#SIMULATED ANNEALING PLUS GRADIENT DESCENT


#import qubo and construct sparse dictionary representation
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

#find some solutions with simmulated annealing
solver_sa = SimulatedAnnealingSampler()
sampleset_sa = solver_sa.sample_qubo(dic, num_reads=500, seed=45, num_sweeps=10)

print(sampleset_sa)

#further explore the solutions summulated annealing found with steepest descent
solver_gd = SteepestDescentSolver()
sampleset_gd = solver_gd.sample_qubo(dic, num_reads=500, seed=45, initial_states=sampleset_sa.samples(), initial_states_generator='none', large_sparse_opt=False)

print(sampleset_gd)