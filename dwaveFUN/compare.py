import numpy as np
import math



t0 = np.zeros(930)
t1 = np.zeros(930)

with open('converged-300s/dwave-result-Tabu0.txt') as f:
    i=0
    for line in f.readlines():
        t0[i] = int(line)
        i+=1

with open('converged-1000s/dwave-result-Tabu0.txt') as f:
    i=0
    for line in f.readlines():
        t1[i] = int(line)
        i+=1


t0 = t0.astype(int)
t1 = t1.astype(int)

unique, counts = np.unique(t0, return_counts=True)
print('t0 counts: ', dict(zip(unique, counts)))

unique, counts = np.unique(t1, return_counts=True)
print('t1 counts: ', dict(zip(unique, counts)))

t01 = np.bitwise_and(t0, t1)
unique, counts = np.unique(t01, return_counts=True)
print('t01 anded counts: ', dict(zip(unique, counts)))