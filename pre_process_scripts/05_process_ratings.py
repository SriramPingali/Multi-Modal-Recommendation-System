
import helpers
import csv

rating_file= helpers.path_of("../Text/u.data")

ratings_data_path= helpers.path_of("../objs/ratings.obj")

ratings_obj= list()

with open(rating_file) as file:
    for line in file:
        items= list(csv.reader([line], delimiter ="\t"))[0]
        user_id, movie_id, rate= [int(x) for x in items[:3]]
        ratings_obj.append([user_id, movie_id, rate])
    file.close()

helpers.store_pkl(ratings_obj, ratings_data_path)
