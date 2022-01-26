
from tqdm import tqdm
import numpy as np

import helpers

vector_file= helpers.path_of("../word_vector_300d.vec")

def get_unique_words(ctnr:set, phases:list):
    for words in phases:
        for word in words:
            if len(word) > 0:
                ctnr.add(word)

def get_vector(word_vec:dict, words:set):
    with open(vector_file) as file:
        for line in tqdm(file):
            word_and_vals= line.split(" ")
            w= word_and_vals[0]
            if w in words:
                vec= word_and_vals[1:]
                vec= list(map(float, vec))
                vec= np.array(vec, dtype=float)
                word_vec.update({
                    w: vec
                })
    file.close()

def split_by_words(arr:list):
    res= []
    for ele in arr:
        words= ele.split(" ")
        r= list()
        for w in words:
            if len(w)>0:
                r.append(w)
        res.append(r)
    return res
                    
def avg_vec(words_arr:list, word_vec:dict):
    res= np.zeros(300)
    found_words= 0
    for w in words_arr:
        if not word_vec.get(w) is None:
            res= res+word_vec.get(w)
            found_words+=1
    if found_words>0:
        res= res/found_words
    return res


def transE_single(head, relation, tail, word_vec):
    head_v= avg_vec(head, word_vec)
    relation_v= avg_vec(relation, word_vec)
    tail_v= avg_vec(tail, word_vec)
    enc= head_v+relation_v-tail_v
    return enc


def transE(head:list, relation:list, tail:list, word_vec:dict):
    if len(head) != len(relation) or len(head)!= len(tail):
        raise "\n\tError!! head, tail, relation doesnot have same length\n"
    res= []
    for index in range(len(head)):
        vec= transE_single(head[index],relation[index], tail[index], word_vec)
        res.append(vec)
    res= np.array(res)
    return res




def encode(head:list, relation:list, tail:list):
    unique_words= set()
    
    head= split_by_words(head)
    relation= split_by_words(relation)
    tail= split_by_words(tail)

    get_unique_words(unique_words, head)
    get_unique_words(unique_words, relation)
    get_unique_words(unique_words, tail)

    word_vec= dict()    
    get_vector(word_vec, unique_words)

    res= transE(head, relation, tail, word_vec)
    return res



