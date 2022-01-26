
import helpers

movie_enc_path= helpers.path_of("../objs/enc_movie.obj")
user_enc_path= helpers.path_of("../objs/enc_user.obj")
ratings_path= helpers.path_of("../objs/ratings.obj")
ratings_op_path= helpers.path_of("../objs/ratings_filtered.obj")

movie_enc= helpers.load_pkl(movie_enc_path)
user_enc= helpers.load_pkl(user_enc_path)
ratings= helpers.load_pkl(ratings_path)


filtered_ratings= []

for user, movie, rate in ratings:
    # if movie>800: continue
    m= movie_enc.get(movie)
    if m is None:
        continue
    u= user_enc.get(user)
    if u is None:
        continue
    filtered_ratings.append([user, movie, rate])


print("Before filter: ", len(ratings), " After filter: ", len(filtered_ratings))

helpers.store_pkl(filtered_ratings, ratings_op_path)

