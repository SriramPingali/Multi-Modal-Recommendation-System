from curses import meta
import helpers
import csv

meta_raw_path= helpers.path_of("../objs/meta_raw.obj")
meta_raw= helpers.load_pkl(meta_raw_path)

audio_file_path= helpers.path_of("../audio/OSmile_audioVectors.csv")

op_path= helpers.path_of("../objs/smile_processed.obj")

yt_movie= dict()
for movie_id in meta_raw.keys():
    d= meta_raw.get(movie_id)
    yt_id= d.get("yt-id")
    yt_movie.update({
        yt_id: movie_id,
    })


max_arr, min_arr= None, None
with open(audio_file_path) as file:
    for line_no, line in enumerate(file):
        if line_no==0: continue
        items= list(csv.reader([line]))[0]
        yt_id= items[0]
        data= [float(x) for x in items[1:]]
        if max_arr is None:
            max_arr= [-float('inf') for _ in data]
            min_arr= [float('inf') for _ in data]
        for ind in range(len(data)):
            max_arr[ind]= max(max_arr[ind], data[ind])
            min_arr[ind]= min(min_arr[ind], data[ind])
file.close()


res_dict= dict()
with open(audio_file_path) as file:
    for line_no, line in enumerate(file):
        if line_no==0: continue
        items= list(csv.reader([line]))[0]
        yt_id= items[0]
        data= [float(x) for x in items[1:]]
        for ind in range(len(data)):
            data[ind]= (data[ind]-min_arr[ind]) / (max_arr[ind]-min_arr[ind])
        movie_id= yt_movie.get(yt_id)
        if movie_id is not None:
            res_dict.update({
                movie_id: data,
            })
file.close()

print(len(res_dict.get(1)))
helpers.store_pkl(res_dict, op_path)