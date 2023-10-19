
from dimod import ConstrainedQuadraticModel
from dimod import Binary
from dimod import Integer
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridCQMSampler 
import numpy as np
import math
import csv
import os

### READ LINEAR TERMS ###

filename = open('miqp_linear.csv', 'r')
file = csv.DictReader(filename)

grb_vtype2 = []
obj = []
lower = []
upper = []
idx = []
 
for row in file:
    grb_vtype2.append(row['TYPE'])
    obj.append(float(row['OBJ_LIN']))
    lower.append(int(row['LOWER']))
    upper.append(int(row['UPPER']))
    idx.append(int(row['INDEX']))

#print(type(grb_vtype2[1]))
#print(type(obj[1]))
#print(type(lower[1]))
#print(type(idx[1]))
 
#print('type:', grb_vtype2)
#print('obj:', obj)
#print('lower', lower)
#print('upper', upper)

varInfo = list(zip(grb_vtype2, lower, upper, idx))

variables = [Integer(f"{i}", lower_bound=l, upper_bound=u) if vt == "I"
                                            else Binary(f"{i}")
                                            for vt, l, u, i in varInfo ]

linTuples = list(zip(idx, obj))

linTerms = [o*variables[i] for i, o in linTuples ]

### READ QUADRATIC TERMS ###

filename = open('miqp_quadratic.csv', 'r')
file = csv.DictReader(filename)

bias = []
vardex1 = []
vardex2 = []
 
for row in file:
    bias.append(float(row['OBJ_QUAD']))
    vardex1.append(int(row['ROW']))
    vardex2.append(int(row['COL']))

quadTuples = list(zip(bias, vardex1, vardex2))

quadTerms = [b*variables[v1]*variables[v2] for b, v1, v2 in quadTuples]


### SET OBJECTIVE ###

cqm = ConstrainedQuadraticModel()

print("setting objective")

cqm.set_objective(sum(quadTerms) + sum(linTerms))


print(len(cqm.objective.linear))
print(len(cqm.objective.quadratic))
print(len(cqm.objective.variables))

sampler = LeapHybridCQMSampler()   
print(sampler.properties["minimum_time_limit_s"] )


sampleset = sampler.sample_cqm(cqm)       
print(sampleset)




feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)   
print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset))) 

resultCount = len(os.listdir('./results'))
fname  = 'results\dwave-result-' + str(resultCount+1) + '.txt'

with open(fname, 'w') as f:
    for i in range(len(sampleset.first.sample)):
        f.write(str(int(sampleset.first.sample[str(i)])))
        f.write('\n')

with open('dwave-log.txt', 'a') as f:
    f.write(str(resultCount+1) + ', ')
    f.write('cqm: energy=' + str(sampleset.first.energy))
    f.write('\n')