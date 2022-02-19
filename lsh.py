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
    one_hot_arrray = np.array(one_hot)
    indexes = np.nonzero(one_hot_arrray)[0]
    value = min(np.array(permutation)[indexes])
    return value

def min_hash(one_hot: list, k: int, seed: list):
    rand = random.Random(seed)
    perm_seeds = [rand.randint(0,1e20) for _ in range(k)]
    linspace = list(range(1,len(one_hot)+1))
    signature = []
    for i in range(k):
        permutation = linspace.copy()
        random.Random(perm_seeds[i]).shuffle(permutation)
        signature.append(sign_value(one_hot, permutation))
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
                if comp.any():
                    candidate = True
                    break
            cand_pairs.append([id, candidate])
    return cand_pairs

def LSH(documents, ids=None, k=3, h=20 , b=2, seed=1):
    if ids is None:
        ids = list(range(0,len(documents)))

    shingles = []
    for doc in documents:
        shingles.append(shingle(doc, k))

    vocab = gen_vocab(shingles)

    one_hot_arrays = []
    for sh in shingles:
        one_hot_arrays.append(one_hot(sh, vocab))

    signatures = []
    for oh in one_hot_arrays:
        signatures.append(min_hash(oh, h, seed))

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
        

if __name__ == "__main__":
    file_names = list_files(".\\sample_documents")
    files_list = [
        open(filename, 'r', encoding='utf-8', errors='ignore') 
        for filename in file_names]
    content_list  = [f.read() for f in files_list]
    names = [f.name for f in files_list]

    lsh_results = LSH(content_list, names, k=5, h=40 , b=2, seed=1)
    # for r in lsh_results:
    #     print(r)

    datapoints, _ = vectorize(content_list)
    vectors = [dp.vector for dp in datapoints]
    cos_results = cosine_sim_pairs(names, vectors)
    # for r in cos_results:
    #     print(r)

    x_axis = [x[1] for x in cos_results]
    y_axis = [1 if x[1]==True else 0 for x in lsh_results]
    
    plt.scatter(x_axis, y_axis)
    plt.ylabel('candidate')
    plt.xlabel('cosine similarity')
    plt.show()