from tools import *
import numpy as np
import random
from numpy.linalg import norm
import matplotlib.pyplot as plt

def shingle(text: str, k: int):
    """Generates a list of strings length k 
    with all the unique length k substrings that text contains 
    for example: text="Hey Hello", k=2 returns {"He","ey","y "," H","el","ll","lo"}

    :param text: A string of characters
    :type text: str
    :param k: The length of its 
    :type k: int
    :raises ValueError: k cannot be less than 1
    :return: A set of all unique length k substrings contained in text
    :rtype: set
    """    
    shingle_set = []
    if k < 1:
        raise ValueError('k cannot be less than 1')
    for i in range(len(text) - k + 1):
        shingle_set.append(text[i:i+k])
    return set(shingle_set)

def gen_vocab(shingles: list):
    """Generates a vocabulary from a list of shigles(sets)

    :param shingles: List of shigles(sets) e.x. [{...},{...},...]
    :type shingles: list
    :return: A vocabulary with unique values
    :rtype: set
    """    
    vocab = set().union(*shingles)
    return vocab

def one_hot(shingle: set, vocab: list):
    """Generates the one hot encoding array 
    given a shingle(set) and a vocabulary. The result has
    the same length as the vocab list and has 1 at indexes
    which the elements of vocab match an element of shingle
    and zeros everywhere else
    For example: 
    one_hot({"b"}, ["a", "b", "c", "d"]) -> [0,1,0,0]

    :param shingle: A set of shingles
    :type shingle: set
    :param vocab: A vocabulary of shingles
    :type vocab: list
    :return: A list that has 1 at indexes
    which the elements of vocab match an element of shingle
    and zeros everywhere else
    :rtype: list
    """    
    one_hot_array = [1 if x in shingle else 0 for x in vocab]
    return one_hot_array

def sign_value(one_hot, permutation):
    """It returns the signature's value that corresponds to the given permutation. 
    It is used for the min hashing of the vectors

    :param one_hot: The input one hot vector from which we want to generate it's signature
    :type one_hot: list
    :param permutation: The random permutation that will yield a value for the signature
    as described by the min hash algorithm
    :type permutation: list
    :return: It returns the min index of the new permuted one hot vector  
    :rtype: int
    """    
    indexes = np.nonzero(one_hot)[0]
    value = min(permutation[indexes])
    return value

def gen_permutations(length, k):
    """Generates the permutations that min hashing will use. A permutation is a list
    with the same length as the input vectors and have all the integer numbers from 1 
    to length randomly shuffled.

    :param length: The length of the permutation vector. It must be same as the input 
    vectors that must be permuted. 
    :type length: int
    :param k: The number of permutation vectors to generate.
    The number of permuations should be at least the same 
    as the length of the desired signature that min hash generates.
    :type k: int
    :return: A list of permutatition vectors
    :rtype: list
    """    
    linspace = np.arange(1, length+1, 1)
    permutations = []
    for _ in range(k):
        random.shuffle(linspace)
        permutations.append(np.array(linspace))
    return np.array(permutations)

def min_hash(one_hot, permutations):
    """The min hash function. It takes a list of one hot vectors and a 
    list of random permutations andgenerates signatures for every one hot vector. 
    Every signature represents the one hot vector that generated the signature. 
    The idea is to take the sparse one hot vectors and make them dense. 
    If two vectors are similar then their signatures are similar too and the opposite.  

    :param one_hot: The one hot vector from which the signature will be generated.
    :type one_hot: list
    :param permutations: The random permutations that will yield every value that make up the signature
    :type permutations: list
    :return: The signature of the one hot vector.
    :rtype: list
    """    
    signature = []
    for i in range(len(permutations)):
        signature.append(sign_value(one_hot, permutations[i]))
    return signature

def split_signature(sign, b):
    """Splits the signature into b bands. For example if signature is 100 values long
    and b is 50 then it will split the singature to 50 bands of 2 values each.

    :param sign: The signature to split
    :type sign: list
    :param b: Number of bands
    :type b: int
    :raises ValueError: The length of the signature must be divisible by b
    :return: A matrix that contains the sigature bands
    :rtype: list
    """    
    #len(sign)%b should be 0
    if len(sign)%b != 0:
        raise ValueError('b should divide signature\'s length to an integer')
    matrix = np.array(sign)
    matrix = matrix.reshape(b, len(sign)//b)
    return matrix

def calc_candidate_pairs(names, sign_matrix):
    """Calculates for every possible pair of signatures if they are considered candidate pairs
    meaning if they have at least one identical band.
    If that is the case then those enties belong to the same bucket. 

    :param names: The names of the original documents. 
    The names are used to trace back which signatures belong to the input documents.
    :type names: list
    :param sign_matrix: The splitted signatures
    :type sign_matrix: list
    :return: A list of all possible pairs with a value TRUE or FALSE that
    indicates if a pair is cadidate pair or not.
    :rtype: list
    """    
    cand_pairs = []
    for i in range(len(names)):
        for j in range(i):
            candidate = False
            id = str(names[i]) + '-' + str(names[j])
            for a,b in zip(sign_matrix[i], sign_matrix[j]):
                comp = (a == b)
                if comp.all():
                    candidate = True
                    break
            cand_pairs.append([id, candidate])
    return cand_pairs

def LSH(documents, ids=None, k=8, sign_length=100 , b=20):
    if ids is None:
        ids = list(range(0,len(documents)))

    shingles = []
    for doc in documents:
        shingles.append(shingle(doc, k))

    vocab = list(gen_vocab(shingles))
    length = len(vocab)

    one_hot_arrays = []
    for sh in shingles:
        one_hot_arrays.append(one_hot(sh, vocab))
    one_hot_arrays = np.array(one_hot_arrays)

    signatures = []
    permutations = gen_permutations(length, sign_length)
    for oh in one_hot_arrays:
        signatures.append(min_hash(oh, permutations))
        
    sign_matrix = []
    for sign in signatures:
        sign_matrix.append(split_signature(sign, b))

    results = calc_candidate_pairs(ids, sign_matrix)
    return results

def cosine_sim(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))

def similarity_pairs_generator(names, vectors, method):
    """Generates all possible pairs with their coresponding similarity score

    :param names: The names of the input vectors
    :type names: list
    :param vectors: The vectors that are meassured
    :type vectors: list
    :param method: The method used to meassure the similarity e.x. Jaccard or Cosine
    :type method: callable
    :return: Returns a list with all pairs and their similarity score
    :rtype: list
    """    

    similarities = []
    for i in range(len(names)):
        for j in range(i):
            id = str(names[i]) + '-' + str(names[j])
            sim = method(vectors[i], vectors[j])
            similarities.append([id, sim])

    return similarities

def jaccard_sim(x: str, y: str):
    """Calculates the Jaccard similarity of 2 strings. 
    The Jaccard similarity of 2 strings is calculated by the
    formula #intersection(X,Y)/#union(X,Y)

    :param x: The first input string
    :type x: str
    :param y: The second input string
    :type y: str
    :return: The Jaccard similarity. It ranges from 0 to 1
    :rtype: float
    """    

    x_set = set(x.split())
    y_set = set(y.split())
    intersection = x_set.intersection(y_set)
    union = x_set.union(y_set)
    return len(intersection)/len(union)

def jaccard_set_sim(x: set, y: set):
    intersection = len(list(set(x).intersection(y)))
    union = (len(x) + len(y)) - intersection
    return float(intersection)/union

def jaccard_binary(x,y):
    """
    A function for finding the similarity between two binary vectors
    :param x: Binary vector
    :param y: Binary Vector
    :intersection: calculates the number of members shared between both vectors
    :union: calculates the total number of members in both vectors (shared and un-shared)
    :returns: The similarity rate between the two given binary vectors
    """
    intersection = np.logical_and(x, y)
    union = np.logical_or(x, y)
    similarity = intersection.sum() / float(union.sum())
    return similarity

def p(x, r, b):
    return (1 - np.power((1 - np.power(x,r)),b))

if __name__ == "__main__":

    k = 8 #shingles size
    s = 500 #singature length
    b = 50 #number of signature bands

    file_names = list_files(".\\samples\\samples4")
    files_list = [
        open(filename, 'r', encoding='utf-8', errors='ignore') 
        for filename in file_names]
    content_list  = [f.read() for f in files_list]
    names = [f.name for f in files_list]

    #trim lists
    content_list = content_list[:100]
    names = names[:100]

    # content_list = [preprocess_string(cont) for cont in content_list]

    # datapoints, _ = vectorize(content_list)
    # vectors = [dp.vector for dp in datapoints]
    # cos_results = similarity_pairs_generator(names, vectors, cosine_sim)
    # vectors_bin = np.where(np.array(vectors) > 0, 1, 0)
    jac_results = similarity_pairs_generator(names, content_list, jaccard_sim)
    lsh_results = LSH(content_list, names, k=k, sign_length=s , b=b)
    # for c,l in zip(cos_results, lsh_results):
        # print(c,l)
    linspace = np.linspace(0,1,100)
    # a_axis = [x[1] for x in cos_results]
    b_axis = [x[1] for x in jac_results]
    c_axis = [1 if x[1]==True else 0 for x in lsh_results]
    p_line = [p(x, s/b, b) for x in linspace]
    plt.scatter(b_axis, c_axis, s=8)
    plt.plot(linspace, p_line, color="red")
    plt.title("LSH candidate pairs")
    plt.xlabel('Jaccard similarity')
    plt.ylabel('LSH candidate pairs')
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)
    plt.show()