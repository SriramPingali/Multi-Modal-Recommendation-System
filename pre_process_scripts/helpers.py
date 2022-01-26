
import os
import pickle
from pathlib import Path

def path_of(location):
    me_dir, me_file= os.path.split(os.path.abspath(__file__))
    return os.path.join(me_dir, location)



def load_pkl(filename):
    filename= path_of(filename)
    data= None
    with open(filename, "rb") as handle:
        data= pickle.load(handle)
        handle.close()
    return data

def store_pkl(object, filename):
    filename= path_of(filename)
    with open(filename, "wb") as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

def is_valid_file(filename):
    filename= path_of(filename)
    file= Path(filename)
    if file.is_file():
        return True
    return False


def to_same_shape(arr_of_items, required_shape):
    if len(arr_of_items) == 0:
        print("Error: tried to make shape: ", required_shape, ", but item is empty...")
        exit()
    if len(arr_of_items)>required_shape:
        return arr_of_items[:required_shape]
    res= []
    ind=0
    while len(res)<required_shape:
        res.append(arr_of_items[ind])
        ind= (ind+1)%len(arr_of_items)
    return res