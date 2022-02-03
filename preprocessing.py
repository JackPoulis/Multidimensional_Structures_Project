import os
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

class Datapoint():
    def __init__(self, vector, id = None):
        self.vector = vector if isinstance(vector, list) else [vector]
        self.id = id
        
    def toString(self) -> str:
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

if __name__ == "__main__":
    fileNames = getListOfFiles(".\\sample_documents")
    inputList = [open(filename, 'r', encoding='utf-8', errors='ignore') for filename in fileNames]
    results = vectorize(inputList)
