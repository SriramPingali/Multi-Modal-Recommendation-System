
import helpers

import katna_vid

from tqdm import tqdm

meta_raw_path= helpers.path_of("../objs/meta_raw.obj")
meta_raw= helpers.load_pkl(meta_raw_path)

video_processed_op_oath= helpers.path_of("../objs/video_processed.obj")
processed_video_obj= helpers.load_pkl(video_processed_op_oath)




def get_avg_vec(vec_arr):
    res= [0 for x in vec_arr[0]]
    for v in vec_arr:
        for ind in range(len(res)):
            res[ind]+= v[ind]
    for ind in range(len(res)):
        res[ind]/=len(vec_arr)

    return res

def make_video_encoding():

    res= dict() 

    could_not_do= list()

    op_path= helpers.path_of("../tmp_files")
    all_movie_id= list(meta_raw.keys())
    for movie_id in tqdm(all_movie_id):
        movie_meta= meta_raw.get(movie_id)
        video_id= movie_meta.get("yt-id")
        if processed_video_obj.get(movie_id):
            res.update({
                movie_id: processed_video_obj.get(movie_id),
            })
            continue
        print("Processing: ", movie_id, " : ", video_id)
        video_path= helpers.path_of("../Video/"+video_id+".mp4")
        if not helpers.is_valid_file(video_path):
            print(video_id, "Not found")
        try:
            vec= katna_vid.get_vectors_for_video(video_path, op_path, 5)

            vec= get_avg_vec(vec)

            res.update({
                movie_id: vec,
            })
        except:
            could_not_do.append([movie_id, video_id])
            

    
    
    helpers.store_pkl(res, video_processed_op_oath)

    print("[*] Done")
    helpers.store_pkl(could_not_do, helpers.path_of("../objs/could_not_process_video_for.obj"))
    print("failed for: ")
    for i in could_not_do:
        print(i)


        


make_video_encoding()