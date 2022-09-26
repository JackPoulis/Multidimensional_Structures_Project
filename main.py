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

max_N = 150 #max number of documents
min_N = 10 #min number of documents
test_step = 5
dimensions = 10
test_range = range(min_N, max_N+1, test_step)

fileNames = list_files(".\\samples\\samples1")
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
datapoints, features = vectorize(inputList, input='file', max_features=dimensions)
datapoints = compress(datapoints)
[f.close() for f in inputList]

d = len(features) #Dimensions
print(len(datapoints))

kdtree_sizes = []
quadtree_sizes = []
rangetree_sizes = []

for N in test_range:
    #Quad tree boundary (In case we measure quad trees)
    # mbr = calc_mbr(datapoints[:N])
    # boundary = Rect(math.ceil(mbr[0][1]/2), math.ceil(mbr[1][1]/2), mbr[0][1]-mbr[0][0]+1, mbr[1][1]-mbr[1][0]+1)

    kd_tree = kdtree.KDTree(datapoints[:N])
    # quad_tree = quadtree.QuadTree(boundary, datapoints[:N])
    # range_tree = rangetree.RangeTree(datapoints[:N])

    kdtree_sizes.append(kd_tree.size())
    # quadtree_sizes.append(quad_tree.size())
    # rangetree_sizes.append(range_tree.size()) 

#space complexity labels
kdtree_label = r'$4{n}$'
quadtree_label = r'$\frac{n}{2}$'
rangetree_label = r'$3{n}(\frac{log({n})}{log(log({n}))})^{{d}-1}$'

linspace = np.linspace(4,max_N,100)
x_axis = test_range
a_points = kdtree_sizes
b_line = [kdtree_space_complexity(x) for x in linspace]
plt.scatter(x_axis, a_points, s=120, alpha=1)
plt.plot(linspace, b_line, color="red", label=quadtree_label, linewidth=3)
plt.title("KD tree space complexity", size=18)
plt.xlabel('n', size=18)
plt.ylabel('number of nodes in tree', size=18)
plt.legend(prop={"size":16}, loc='upper left')
plt.box(False)
plt.show()