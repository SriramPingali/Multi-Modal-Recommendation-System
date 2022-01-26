

import helpers
import csv




def process_this_file(ip_file, op_file):

    rating_file= helpers.path_of(ip_file)

    ratings_op_path= helpers.path_of(op_file)

    ratings_obj= list()

    with open(rating_file) as file:
        for line in file:
            items= list(csv.reader([line], delimiter ="\t"))[0]
            user_id, movie_id, rate= [int(x) for x in items[:3]]
            ratings_obj.append([user_id, movie_id, rate])
        file.close()

    helpers.store_pkl(ratings_obj, ratings_op_path)




splits_and_ops= [
    ["../Text/u1.base", "../objs/splits/u1.train.obj"],
    ["../Text/u1.test", "../objs/splits/u1.test.obj"],
    ["../Text/u2.base", "../objs/splits/u2.train.obj"],
    ["../Text/u2.test", "../objs/splits/u2.test.obj"],
    ["../Text/u3.base", "../objs/splits/u3.train.obj"],
    ["../Text/u3.test", "../objs/splits/u3.test.obj"],
    ["../Text/u4.base", "../objs/splits/u4.train.obj"],
    ["../Text/u4.test", "../objs/splits/u4.test.obj"],
    ["../Text/u5.base", "../objs/splits/u5.train.obj"],
    ["../Text/u5.test", "../objs/splits/u5.test.obj"],
    ["../Text/ua.base", "../objs/splits/ua.train.obj"],
    ["../Text/ua.test", "../objs/splits/ua.test.obj"],
    ["../Text/ub.base", "../objs/splits/ub.train.obj"],
    ["../Text/ub.test", "../objs/splits/ub.test.obj"],
    
]

for ip, op in splits_and_ops:
    process_this_file(ip,op)