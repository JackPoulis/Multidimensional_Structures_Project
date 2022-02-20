from tools import *
import numpy as np
import random
from numpy.linalg import norm
import matplotlib.pyplot as plt

def shingle(text, k):
    shingle_set = []
    for i in range(len(text) - k + 1):
        shingle_set.append(text[i:i+k])
    return set(shingle_set)

def gen_vocab(shingles: list):
    vocab = set().union(*shingles)
    return vocab

def one_hot(shingle, vocab):
    # one_hot_array = np.where(np.isin(vocab, shingle), 1, 0)
    one_hot_array = [1 if x in shingle else 0 for x in vocab]
    return one_hot_array

def sign_value(one_hot, permutation):
    indexes = np.nonzero(one_hot)[0]
    value = min(permutation[indexes])
    return value

def gen_permutations(length, k):
    linspace = np.arange(1, length+1, 1)
    permutations = []
    for _ in range(k):
        random.shuffle(linspace)
        permutations.append(np.array(linspace))
    return np.array(permutations)

def min_hash(one_hot, permutations):
    signature = []
    for i in range(len(permutations)):
        signature.append(sign_value(one_hot, permutations[i]))
    return signature

def split_signature(sign, b):
    #len(sign)%b should be 0
    matrix = np.array(sign)
    matrix = matrix.reshape(b, len(sign)//b)
    return matrix

def calc_candidate_pairs(names, sign_matrix):
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

def LSH(documents, ids=None, k=3, sign_length=20 , b=2):
    if ids is None:
        ids = list(range(0,len(documents)))

    shingles = []
    for doc in documents:
        shingles.append(shingle(doc, k))

    vocab = gen_vocab(shingles)
    length = len(vocab)

    one_hot_arrays = []
    for sh in shingles:
        one_hot_arrays.append(one_hot(sh, vocab))
    one_hot_arrays = np.array(one_hot_arrays)

    signatures = []
    permutations = gen_permutations(length, sign_length)
    for i, oh in enumerate(one_hot_arrays):
        signatures.append(min_hash(oh, permutations))
        
    sign_matrix = []
    for sign in signatures:
        sign_matrix.append(split_signature(sign, b))

    results = calc_candidate_pairs(ids, sign_matrix)
    return results

def cosine_sim(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))

def cosine_sim_pairs(names, vectors):
    similarities = []
    for i in range(len(names)):
        for j in range(i):
            id = str(names[i]) + '-' + str(names[j])
            sim = cosine_sim(vectors[i], vectors[j])
            similarities.append([id, sim])

    return similarities
        
def jaccard_binary(x,y):
    intersection = np.logical_and(x, y)
    union = np.logical_or(x, y)
    similarity = intersection.sum() / float(union.sum())
    return similarity

def jaccard_sim_pairs(names, vectors):
    similarities = []
    for i in range(len(names)):
        for j in range(i):
            id = str(names[i]) + '-' + str(names[j])
            sim = jaccard_binary(vectors[i], vectors[j])
            similarities.append([id, sim])

    return similarities

if __name__ == "__main__":
    # file_names = list_files(".\\sample_documents")
    file_names = list_files(".\\sample_documents\\samples2")
    files_list = [
        open(filename, 'r', encoding='utf-8', errors='ignore') 
        for filename in file_names]
    content_list  = [f.read() for f in files_list]
    names = [f.name for f in files_list]
    content_list = [preprocess_string(cont) for cont in content_list]

    datapoints, _ = vectorize(content_list)
    vectors = [dp.vector for dp in datapoints]
    cos_results = cosine_sim_pairs(names, vectors)
    vectors_bin = np.where(np.array(vectors) > 0, 1, 0)
    jac_results = jaccard_sim_pairs(names, vectors_bin)
    lsh_results = LSH(content_list, names, k=2, sign_length=40 , b=4)
    # for c,l in zip(cos_results, lsh_results):
    #     print(c,l)

    a_axis = [x[1] for x in cos_results]
    b_axis = [x[1] for x in jac_results]
    c_axis = [1 if x[1]==True else 0 for x in lsh_results]
    
    plt.scatter(a_axis, c_axis, s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)
    plt.show()