import os
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

try:
    nltk.data.find('tokenizers/stopwords')
except LookupError:
    nltk.download('stopwords')

class Datapoint():
    def __init__(self, vector, id = None):
        self.vector = vector if isinstance(vector, list) else [vector]
        self.id = id
        
    def __str__(self) -> str:
        string = str(self.id) + ' = [' + str(self.vector[0])
        for a in self.vector[1:]:
            string += ', ' + str(a)
        string += ']'
        return string

    def in_range(self, region) -> bool:
        """Check if the Datapoint is inside the given region.
        The datapoint dimensions should be greater or equal to region dimensions

        :param region: The region to check if the datapoint belongs to.
        The region is a list with length = dimensions and for each dimension
        it contains the min and max bounds. e.x. 3D region: [[x1,x2],[y1,y2],[z1,z2]]
        :type region: list
        :return: True if datapoint is in the region else False
        :rtype: bool
        """

        for axis in range(len(region)):
            if self.vector[axis] < min(region[axis]) or self.vector[axis] > max(region[axis]):
                return False
        return True

class Node():
    def __init__(self, value, axis, leftC = None, rightC = None, datapoint: Datapoint = None, subTree = None):
        self.value = value
        self.axis = axis
        self.leftChild: Node = leftC
        self.rightChild: Node = rightC
        self.datapoint: Datapoint = datapoint
        self.subTree = subTree
        
    def isLeaf(self):
        """Checks if the node is a leaf. A leaf node has no child nodes

        :return: True if the node is leaf else False
        :rtype: bool
        """
        if self.leftChild or self.rightChild:
            return False
        else:
            return True  

    def __str__(self) -> str:
        string = "Axis: {axis}, Value: {value} -> "
        tail = "Left: {leftvalue}, Right: {rightvalue}"
        leftstr = rightstr = "-"
        if self.leftChild:
            leftstr = str(self.leftChild.value)
        if self.rightChild:
            rightstr = str(self.rightChild.value)
        tail = tail.format(leftvalue = leftstr, rightvalue = rightstr)
        if self.isLeaf():
            tail = str(self.datapoint)
        return string.format(axis = self.axis, value = self.value) + tail

def extractLeafs(node):
    """Takes a node of a tree/subtree and returns all the leaf nodes below that node

    :param node: The root/subroot node of the tree/subtree to extract leafs
    :type node: Node
    :return: A list of all leaf nodes found below the node
    including the node if it is a leaf node
    :rtype: list
    """

    leafs = []
    if node.isLeaf():
        leafs.append(node)
    else:
        for child in [node.leftChild, node.rightChild]:
            if child:
                leafs = leafs + extractLeafs(child)
    return leafs

def getListOfFiles(dir):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFiles = os.listdir(dir)
    fileNames = list()
    # Iterate over all the entries
    for entry in listOfFiles:
        # Create full path
        fullPath = os.path.join(dir, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            fileNames = fileNames + getListOfFiles(fullPath)
        else:
            fileNames.append(fullPath)
                
    return fileNames

def custom_preprocessor(string: str):
    return string.lower()

def custom_tokenizer(string):
    words = word_tokenize(string)
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [stemmer.stem(word) for word in words if word.isalpha() and word not in stop_words]

def vectorize(inputList, input='content', vocabulary=None):

    countvectorizer = CountVectorizer(input=input, preprocessor=custom_preprocessor, tokenizer=custom_tokenizer, max_df=0.75, min_df=0.25, vocabulary=vocabulary)
    count_wm = countvectorizer.fit_transform(inputList)
    features = countvectorizer.get_feature_names_out()
    if input=='file':
        ids = [f.name for f in inputList]
    else:
        ids = list(range(0,len(inputList)))
    datapoints = [Datapoint(list(pair[0]),pair[1]) for pair in zip(count_wm.toarray(), ids)]

    return datapoints, features

def contained(region_a, region_b):
    return intersection(region_a, region_b) == region_a

def intersects(region_a, region_b):
    inter_a_b = intersection(region_a, region_b)
    return True if not inter_a_b is None else False

def intersection(region_a, region_b):
    dim = len(region_a)
    new_region = []
    for axis in range(dim):
        a = max([min(region_a[axis]),min(region_b[axis])])
        b = min([max(region_a[axis]),max(region_b[axis])])
        if b < a:
            return None
        new_region.append([a,b])

    return new_region

if __name__ == "__main__":
    # fileNames = getListOfFiles(".\\sample_documents")
    # inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
    # results = vectorize(inputList, input='file')
    pass
