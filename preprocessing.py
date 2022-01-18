import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer

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

def preprocessor():
    pass

def tokenizer():
    pass

def vectorize(filenames):
    
    countvectorizer = CountVectorizer(input='file', stop_words='english', max_df=0.75, min_df=0.25)
    count_wm = countvectorizer.fit_transform([open(filename, 'r', encoding='utf-8', errors='ignore') for filename in filenames])

    count_tokens = countvectorizer.get_feature_names_out()

    df_countvect = pd.DataFrame(data = count_wm.toarray(), index = ['Doc0', 'Doc1', 'Doc2', 'Doc3', 'Doc4'], columns = count_tokens)
    return df_countvect.to_json(orient='index')

if __name__ == "__main__":
    directory = ".\\sample_documents"
    fileNames = getListOfFiles(directory)
    print(vectorize(fileNames))