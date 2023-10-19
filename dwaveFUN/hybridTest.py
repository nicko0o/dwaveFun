
from dimod.generators import and_gate
from dwave.system import LeapHybridSampler
import dimod
import numpy as np
import math
import os

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

bqm = dimod.BinaryQuadraticModel.from_qubo(dic)



sampler = LeapHybridSampler()    


answer = sampler.sample(bqm)   
print(answer)    



samples = answer.samples()

resultCount = len(os.listdir('./results'))
fname  = 'results\dwave-result-' + str(resultCount+1) + '.txt'

with open(fname, 'w') as f:
    for i in range(len(answer.first.sample)):
        f.write(str(samples[0, i]))
        f.write('\n')

with open('dwave-log.txt', 'a') as f:

    f.write(str(resultCount+1) + ', ')
    f.write('energy=' + str(answer.first.energy))
    f.write('\n')