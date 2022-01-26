
import spacy
from spacy.matcher import Matcher
from tqdm import tqdm


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')

# doc = nlp("The 22-year-old recently won ATP Challenger tournament.")
# doc = nlp("Nagal won the first set.")
# for tok in doc:
#     print(tok.text, "...", tok.dep_)








def get_entities(sent):
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""
    prv_tok_text = ""

    prefix = ""
    modifier = ""

    
    for tok in nlp(sent):
        if tok.dep_ != "punct":
            if tok.dep_ == "compound":
                prefix = tok.text
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " "+ tok.text

            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " "+ tok.text

            if tok.dep_.find("subj") == True:
                ent1 = modifier +" "+ prefix + " "+ tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""            

            if tok.dep_.find("obj") == True:
                ent2 = modifier +" "+ prefix +" "+ tok.text

            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text

    return [ent1.strip(), ent2.strip()]


def get_relation(sent):
    doc = nlp(sent)

    matcher = Matcher(nlp.vocab)

    pattern =           [{'DEP':'ROOT'}, 
                        {'DEP':'prep','OP':"?"},
                        {'DEP':'agent','OP':"?"},    
                        {'POS':'ADJ','OP':"?"}] 

    matcher.add("matching_1", None, pattern) 
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]] 
    return(span.text)


def get_elements(sent_arr):
    head= []
    tail= []
    relation= []

    for sen in tqdm(sent_arr):
        try:
            entity= get_entities(sen)
            rel= get_relation(sen)
        except:
            entity= ["None", "None"]
            rel= "None"
        head.append(entity[0])
        tail.append(entity[1])
        relation.append(rel)
    return head, relation, tail


def draw_graph(head, relation, tail):
    kg_df = pd.DataFrame({'source':head, 'target':tail, 'edge':relation})
    G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    # G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="composed by"], "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    # G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="written by"], "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    # G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="released in"], "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
    
    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.show()


def inner_preprocess_sen(sen:str):
    sen= sen.rstrip("\n").lstrip(" ").rstrip(" ").lstrip("\"").rstrip("\"")
    return sen
def preprocess_sen(sen):
    if type(sen) == str:
        return inner_preprocess_sen(sen)
    elif type(sen) == list:
        res= list()
        for s in sen:
            res.append(inner_preprocess_sen(s))
        return res
    else:
        raise "\n\tPreprocess sen takes string or list of string...\n"


def build_and_encode(sentence_arr:list):
    sen_arr= []
    for sen in sentence_arr:
        sen= preprocess_sen(sen)
        sen_arr.append(sen)
    h,r,t= get_elements(sen_arr)
    import kg_encoder as kg_encoder
    encoded= kg_encoder.encode(h,r,t)
    return encoded




if __name__ == "__main__":
    sen_arr= []
    lines_to_run_for, count= 5000, 0
    with open("./kg_ip.txt") as file:
        for line in file:
            count+=1
            if count == lines_to_run_for: break
            sen= preprocess_sen(line)
            sen_arr.append(sen)
    file.close()
    h,r,t= get_elements(sen_arr)
    draw_graph(h,r,t)