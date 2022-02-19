import kdtree
import quadtree
import rangetree
# import rtree
import lsh
from tools import *

fileNames = list_files(".\\sample_documents")
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
datapoints = vectorize(inputList, input='file')
[f.close() for f in inputList]