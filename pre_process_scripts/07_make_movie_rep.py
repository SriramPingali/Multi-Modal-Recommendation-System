

import helpers

# make_movie_from_files= ["meta_processed.obj", "video_processed.obj", "smile_processed.obj"]
make_movie_from_files= ["meta_processed.obj", "video_processed.obj"]
path_of_obj= "../objs/"

movie_enc_op_path= helpers.path_of("../objs/enc_movie.obj")


make_movie_from_files= [helpers.path_of(path_of_obj+x) for x in make_movie_from_files]
make_movie_from_files= [helpers.load_pkl(x) for x in make_movie_from_files]

movie_ids= None
for f in make_movie_from_files:
    if movie_ids is None:
        movie_ids= set(f.keys())
    else:
        movie_ids= movie_ids.intersection(set(f.keys()))
movie_ids= list(movie_ids)



final_movie_rep= dict()


for movie_id in movie_ids:
    rep= list()
    for m in make_movie_from_files:
        rep= rep+m.get(movie_id)
    final_movie_rep.update({
        movie_id: rep,
    })

print("REP SHAPE: ", len(rep))
helpers.store_pkl(final_movie_rep, movie_enc_op_path)







