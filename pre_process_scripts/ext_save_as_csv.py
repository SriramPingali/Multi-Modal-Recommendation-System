
import helpers


obj= helpers.load_pkl("../objs/enc_movie.obj")


save_filename= helpers.path_of("../csvs/enc_movie_meta_graph.csv")

file= open(save_filename, "w")

max_movie_id= max(obj.keys())
# print(max_movie_id)
enc_shape= len(obj.get(list(obj.keys())[0]))
print(enc_shape)


# for id in obj.keys():
#     data= list(obj.get(id))
#     file.write(str(id)+",")
#     for d_id in range(len(data)-1):
#         file.write(str(data[d_id])+",")
#     file.write(str(data[-1]))
#     file.write("\n")


for i in range(enc_shape):
    file.write(str(i)+",")
file.write(str(enc_shape))
file.write("\n")


for movie_id in range(1,max_movie_id+1):
    data= obj.get(movie_id)
    if data is None:
        data= [0 for _ in range(enc_shape)]
    else:
        data= list(data)
    for d_id in range(len(data)-1):
        file.write(str(data[d_id])+",")
    file.write(str(data[-1]))
    file.write("\n")
    

file.close()

