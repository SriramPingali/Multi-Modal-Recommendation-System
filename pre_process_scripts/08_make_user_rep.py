

import helpers

ratings_obj_path= helpers.path_of("../objs/ratings.obj")
movie_enc_path= helpers.path_of("../objs/enc_movie.obj")

user_meta_path= helpers.path_of("../objs/user_meta.obj")

user_enc_op_path= helpers.path_of("../objs/enc_user.obj")

rating_obj= helpers.load_pkl(ratings_obj_path)
movie_enc= helpers.load_pkl(movie_enc_path)
user_meta= helpers.load_pkl(user_meta_path)



def avg_arr(arr_of_arr):
    res= [0 for x in arr_of_arr[0]]
    for arr in arr_of_arr:
        for ind in range(len(arr)):
            res[ind]+=arr[ind]
    for ind in range(len(res)):
        res[ind]= res[ind]/len(arr_of_arr)
    return res


movies_to_take_at_least= 15
rating_cutoff= 3

def filter_movies(movies_and_rate_arr):
    res= []
    for m in movies_and_rate_arr:
        if m[1]>rating_cutoff or len(res)<movies_to_take_at_least:
            res.append(m[0])
    return res


user_movie_dict= dict()

for user_id, movie_id, rate in rating_obj:
    if user_movie_dict.get(user_id) is None:
        user_movie_dict.update({
            user_id: list()
        })
    if not movie_enc.get(movie_id) is None:
        user_movie_dict.get(user_id).append((movie_enc.get(movie_id), rate))





for user_id in list(user_movie_dict.keys()):
    user_movie_dict.get(user_id).sort(key= lambda x: x[1], reverse=True)
    filtered= filter_movies(user_movie_dict.get(user_id))
    avg_of_movies= avg_arr(filtered)
    user_movie_dict.update({
        user_id: avg_of_movies
    })
    

# add the metadata of users

for user_id in list(user_movie_dict.keys()).copy():
    user_movie_dict.update({
        user_id: user_movie_dict.get(user_id)+user_meta.get(user_id)
    })


enc_size= len(user_movie_dict.get(1))
# print(user_movie_dict.get(1))

print("Encoding size: ", enc_size)

helpers.store_pkl(user_movie_dict, user_enc_op_path)