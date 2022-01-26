
import re
import helpers

ratings= helpers.load_pkl("../objs/ratings.obj")

# user_enc_path= helpers.path_of("../objs/enc_user.obj")
# movie_enc_path= helpers.path_of("../objs/enc_movie.obj")

user_enc_path= helpers.path_of("../objs/enc_user_from_rates.obj")
movie_enc_path= helpers.path_of("../objs/enc_movie_from_rates.obj")

# print(len(ratings))

user_count, movie_count= 0,0

for user, movie, rate in ratings:
    user_count= max(user_count, user)
    movie_count= max(movie_count, movie)



ratings= ratings[:int(len(ratings)*0.8)]



def normalize(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j]/=5 # devided everything by 5 for normalize

def make_dict(arr):
    d= dict()
    for i in range(len(arr)):
        d.update({
            (i+1): arr[i]
        })
    return d


def make_user_arr():
    user_arr= [[0 for _ in range(movie_count)] for _ in range(user_count)]

    for user_id, movie_id, rate in ratings:
        user_id= user_id-1
        movie_id= movie_id-1

        user_arr[user_id][movie_id]= rate # filled with rate... may be filled with ones for bin
    
    normalize(user_arr)

    user_dict= make_dict(user_arr)

    print("Shape: ", len(user_dict.get(list(user_dict.keys())[0])))

    helpers.store_pkl(user_dict, user_enc_path)


def make_movie_arr():
    movie_arr= [[0 for _ in range(user_count)] for _ in range(movie_count)]

    for user_id, movie_id, rate in ratings:
        user_id= user_id-1
        movie_id= movie_id-1

        movie_arr[movie_id][user_id]= rate

    normalize(movie_arr)

    movie_dict= make_dict(movie_arr)

    print("Shape: ", len(movie_dict.get(list(movie_dict.keys())[0])))

    helpers.store_pkl(movie_dict, movie_enc_path)





if __name__=="__main__":
    print("[*] Making user enc...")
    make_user_arr()
    print("[*] Making movie enc...")
    make_movie_arr()
    print("[*] Done...")

