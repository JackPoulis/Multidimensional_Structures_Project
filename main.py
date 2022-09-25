import kdtree
import quadtree
import rangetree
import lsh
import math
from tools import *

N = 100 #Number of documents

fileNames = list_files(".\\samples\\samples2")
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
inputList = inputList[:N]
datapoints, features = vectorize(inputList, input='file', max_features=2)
[f.close() for f in inputList]

datapoints = compress(datapoints)
mbr = calc_mbr(datapoints)
print(mbr)

boundary = Rect(math.ceil(mbr[0][1]/2), math.ceil(mbr[1][1]/2), mbr[0][1]-mbr[0][0]+1, mbr[1][1]-mbr[1][0]+1)

kdtree = kdtree.KDTree(datapoints)
quadtree = quadtree.QuadTree(boundary, datapoints)
rangetree = rangetree.RangeTree(datapoints)
print("sizes ---------------------")
print(kdtree.size())
print(rangetree.size())
print(quadtree.size())
