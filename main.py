import kdtree
import quadtree
import rangetree
# import rtree
import tools

fileNames = tools.getListOfFiles(".\\sample_documents")
inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
datapoints = tools.vectorize(inputList, input='file')
[f.close() for f in inputList]