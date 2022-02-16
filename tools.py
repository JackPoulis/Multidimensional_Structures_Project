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

def contained(range_a, range_b):
    return intersection(range_a, range_b) == range_a

def intersects(range_a, range_b):
    intersects = True if not contained(range_a, range_b) or intersection(range_a, range_b) is None else False
    return intersects

def intersection(range_a, range_b):
    dim = len(range_a[0])
    point1 = [0] * dim
    point2 = [0] * dim
    for axis in range(len(range_a)):
        a1 = range_a[0][axis]
        a2 = range_a[1][axis]
        min_a = min([a1, a2])
        max_a = max([a1, a2])

        b1 = range_b[0][axis]
        b2 = range_b[1][axis]
        min_b = min([b1, b2])
        max_b = max([b1, b2])
        
        if (min_a > max_b) or (max_a < min_b):
            return None

        point1[axis] = max([min_a, min_b])
        point2[axis] = min([max_a, max_b])

    return (point1, point2)

if __name__ == "__main__":
    # fileNames = getListOfFiles(".\\sample_documents")
    # inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
    # results = vectorize(inputList, input='file')
    # dp = Datapoint([1,1], 0)
    # print(dp)
    range_a = ([2,2], [3,3])
    range_b = ([1,1], [3,3])
    con = contained(range_a, range_b)
    print(con)
