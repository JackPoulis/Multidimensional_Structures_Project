import kdtree
import quadtree
import rangetree
import lsh
import math
from tools import *
import matplotlib.pyplot as plt
import numpy as np

# N = 400 #Number of documents
max_N = 150

fileNames = list_files(".\\samples\\samples2")
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
datapoints, features = vectorize(inputList, input='file', max_features=2)
datapoints = compress(datapoints)
[f.close() for f in inputList]

d = len(features) #Dimensions
print(len(datapoints))

# kdtree_sizes = []
quadtree_sizes = []
# rangetree_sizes = []

test_range = range(10, max_N+1, 2)
for N in test_range:
    
    mbr = calc_mbr(datapoints[:N])
    boundary = Rect(math.ceil(mbr[0][1]/2), math.ceil(mbr[1][1]/2), mbr[0][1]-mbr[0][0]+1, mbr[1][1]-mbr[1][0]+1)

    # kd_tree = kdtree.KDTree(datapoints[:N])
    quad_tree = quadtree.QuadTree(boundary, datapoints[:N])
    # range_tree = rangetree.RangeTree(datapoints[:N])

    # kdtree_sizes.append(kd_tree.size())
    quadtree_sizes.append(quad_tree.size())
    # rangetree_sizes.append(range_tree.size()) 
    
def rangetree_space_complexity(n, factor=3): #Bernard Chazelle complexity
    base = math.log(n, 2)/math.log(math.log(n,2),2) 
    return factor*(n*math.pow(base,(d-1)))

def kdtree_space_complexity(n, factor=4): #O(n)
    return factor*n

def quadtree_space_complexity(n, factor=1/2): #O(n)
    return factor*n

linspace = np.linspace(4,max_N,100)
x_axis = test_range
a_points = quadtree_sizes
b_line = [quadtree_space_complexity(x) for x in linspace]
plot_text = f'Tree dimensions = {len(features)}'
plt.scatter(x_axis, a_points, s=120, alpha=1)
plt.text(5, 40, plot_text, fontsize = 16)
plt.plot(linspace, b_line, color="red", label=r'$\frac{n}{2}$', linewidth=3)
# plt.plot(linspace, b_line, color="red", label=r'$3{n}(\frac{log({n})}{log(log({n}))})^{{d}-1}$', linewidth=3)
plt.title("Quad tree space complexity", size=18)
plt.xlabel('n', size=18)
plt.ylabel('number of nodes in tree', size=18)
plt.legend(prop={"size":16}, loc='upper left')
plt.box(False)
plt.show()