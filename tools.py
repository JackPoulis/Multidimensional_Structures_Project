import os
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# try:
#     nltk.data.find('tokenizers/stopwords')
# except LookupError:
#     nltk.download('stopwords')

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
        it contains the min and max bounds. 
        e.x. 3D region: [[x1,x2],[y1,y2],[z1,z2]]
        :type region: list
        :return: True if datapoint is in the region else False
        :rtype: bool
        """

        for axis in range(len(region)):
            if self.vector[axis] < min(region[axis]) or self.vector[axis] > max(region[axis]):
                return False
        return True

class Node():
    def __init__(self, value, axis, l_child = None, r_child = None, datapoint: Datapoint = None, subtree = None):
        self.value = value
        self.axis = axis
        self.left_child: Node = l_child
        self.right_child: Node = r_child
        self.datapoint: Datapoint = datapoint
        self.subtree = subtree
        
    def is_leaf(self):
        """Checks if the node is a leaf. A leaf node has no child nodes

        :return: True if the node is leaf else False
        :rtype: bool
        """
        if self.left_child or self.right_child:
            return False
        else:
            return True  

    def __str__(self) -> str:
        head_str = "axis {axis}: ({value}) -> "
        childs_str = "left: ({lvalue}), right: ({rvalue})"
        lvalue = rvalue = '-'
        axis = self.axis

        if self.is_leaf():
            if self.datapoint:
                output = str(self.datapoint)
            else:
                output = str(self.value)
        else:
            value = self.value
            if self.left_child:
                if self.left_child.is_leaf():
                    lvalue = str(self.left_child.datapoint)
                else:
                    lvalue = str(self.left_child.value)

            if self.right_child:
                if self.right_child.is_leaf():
                    rvalue = str(self.right_child.datapoint)
                else:
                    rvalue = str(self.right_child.value)
            
            output = head_str.format(axis = axis, value = value)
            output += childs_str.format(lvalue = lvalue, rvalue = rvalue)

        if self.subtree:
            output += ", subtree: " + str(self.subtree.root)
            
        return output

def extract_leafs(node: Node):
    """Takes a node of a tree/subtree and returns 
    all the leaf nodes below that node

    :param node: The root/subroot node of the tree/subtree to extract leafs
    :type node: Node
    :return: A list of all leaf nodes found below the node
    including the node if it is a leaf node
    :rtype: list
    """

    leafs = []
    if node.is_leaf():
        leafs.append(node)
    else:
        for child in [node.left_child, node.right_child]:
            if child:
                leafs = leafs + extract_leafs(child)
    return leafs

def calc_mbr(datapoints: Datapoint):
    """Calculate the minimum bounding rectangle that contains the datapoints

    :param datapoints: The input datapoints to calculate the MBR
    :type datapoints: Datapoint
    :return: The MBR in the form [[x1,x2],[y1,y2],[z1,z2],...] where every element
    in the list is the bounds of the corresponding dimension
    :rtype: list
    """

    dim = len(datapoints[0].vector)
    region = []
    for axis in range(dim):
        axis_vector = [datapoint.vector[axis] for datapoint in datapoints]
        min_value = min(axis_vector)
        max_value = max(axis_vector)
        region.append([min_value, max_value])

    return region

def list_files(dir):
    # create a list of file and sub directories 
    # names in the given directory 
    files_list = os.listdir(dir)
    file_names = list()
    # Iterate over all the entries
    for entry in files_list:
        # Create full path
        full_path = os.path.join(dir, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(full_path):
            file_names = file_names + list_files(full_path)
        else:
            file_names.append(full_path)
                
    return file_names

def custom_preprocessor(string: str):
    return string.lower()

def custom_tokenizer(string):
    words = word_tokenize(string)
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    return [stemmer.stem(word) for word in words if word.isalpha() and word not in stop_words]

def vectorize(input_list, input='content', vocabulary=None):

    countvectorizer = CountVectorizer(
        input = input, 
        preprocessor = custom_preprocessor, 
        tokenizer = custom_tokenizer, 
        max_df = 0.75,
        min_df = 0.25, 
        vocabulary = vocabulary)

    count_wm = countvectorizer.fit_transform(input_list)
    features = countvectorizer.get_feature_names_out()
    if input=='file':
        ids = [f.name for f in input_list]
    else:
        ids = list(range(0,len(input_list)))
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
    # file_names = list_files(".\\sample_documents")
    # input_list = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in file_names]
    # results = vectorize(input_list, input='file')
    pass
