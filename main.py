import kdtree
import quadtree
import rangetree
import math
from tools import *
import matplotlib.pyplot as plt
import numpy as np

"""This python script measures and tests space 
complexity of the the 3 data structures
Kd tree, Quad tree and Range tree.

With this script we can measure the size of the tree generated and
compare it with the space complexity formulas that each tree has
"""

max_N = 45 #max number of datapoints
min_N = 10 #min number of datapoints
test_step = 1
dimensions = 2
test_range = range(min_N, max_N+1, test_step)
test_tree = "Range tree" #Options are 'KD tree', 'Quad tree', 'Range tree'
#If tree is quad tree dimensions should not be more than 2

fileNames = list_files(".\\samples\\samples1")# The documents directory from which to generate the points
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
datapoints, features = vectorize(inputList, input='file', max_features=dimensions)
datapoints = compress(datapoints) #Group duplicates 
[f.close() for f in inputList]

d = len(features) #Dimensions
print(len(datapoints))

kdtree_sizes = []
quadtree_sizes = []
rangetree_sizes = []

for N in test_range:

    if test_tree=='KD tree':
        kd_tree = kdtree.KDTree(datapoints[:N])
        kdtree_sizes.append(kd_tree.size())
    elif test_tree=='Quad tree':
        mbr = calc_mbr(datapoints[:N])
        boundary = Rect(math.ceil(mbr[0][1]/2), math.ceil(mbr[1][1]/2), mbr[0][1]-mbr[0][0]+1, mbr[1][1]-mbr[1][0]+1)
        quad_tree = quadtree.QuadTree(boundary, datapoints[:N])
        quadtree_sizes.append(quad_tree.size())
    elif test_tree=='Range tree':
        range_tree = rangetree.RangeTree(datapoints[:N])
        rangetree_sizes.append(range_tree.size()) 

if test_tree=='KD tree':
    complexity = kdtree_space_complexity
    formula = r'${n}$'
    a_points = kdtree_sizes
elif test_tree=='Quad tree':
    complexity = quadtree_space_complexity
    formula = r'${n}$'
    a_points = quadtree_sizes
elif test_tree=='Range tree':
    complexity = rangetree_space_complexity
    formula = r'${n}(\frac{log({n})}{log(log({n}))})^{{d}-1}$'
    a_points = rangetree_sizes
else:
    complexity = lambda x : x
    formula = r'${n}$'

linspace = np.linspace(4,max_N,100)
x_axis = test_range
b_line = [complexity(x) for x in linspace]
plt.scatter(x_axis, a_points, s=120, alpha=1)
plt.plot(linspace, b_line, color="red", label=formula, linewidth=3)
plt.title(test_tree + " space complexity", size=18)
plt.xlabel('n', size=18)
plt.ylabel('number of nodes in tree', size=18)
plt.legend(prop={"size":16}, loc='upper left')
plt.box(False)
plt.show()