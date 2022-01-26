
from cgi import print_directory
from os import path
import helpers
import csv
'''
0  :  
1  :  Unnamed: 0
2  :  Unnamed: 0.1
3  :  Unnamed: 0.1.1
4  :  Unnamed: 0.1.1.1
5  :  Unnamed: 0.1.1.1.1
6  :  Unnamed: 0.1.1.1.1.1
7  :  movie id
8  :  movie title
9  :  release date
10  :  video release date
11  :  IMDb URL
12  :  unknown
13  :  Action
14  :  Adventure
15  :  Animation
16  :  Children's
17  :  Comedy
18  :  Crime
19  :  Documentary
20  :  Drama
21  :  Fantasy
22  :  Film-Noir
23  :  Horror
24  :  Musical
25  :  Mystery
26  :  Romance
27  :  Sci-Fi
28  :  Thriller
29  :  War
30  :  Western
31  :  Summary
32  :  Cast
33  :  Director
34  :  Rating
35  :  Runtime
36  :  No. of ratings
37  :  YT-Trailer ID
'''
items_main_file= helpers.path_of("../Text/items.csv")

# w2v_file= helpers.path_of("../word_vector_300d.vec")

op_dict= dict()

with open(items_main_file) as file:
    directors= set()
    count=0
    for line_no, line in enumerate(file):
        if line_no==0: continue
        items= list(csv.reader([line]))[0]
        id= int(items[7])
        genres= [int(x) for x in items[12:31]]
        director= items[33].lstrip(" ").rstrip(" ")
        if len(director)==0:
            print("skiping_for_director")
            continue
        rating= items[34].lstrip(" ").rstrip(" ")
        if len(rating)==0:
            print("skiping_for_ratings")
            continue
        rating= float(rating)
        casts= items[32].lstrip(" ").rstrip(" ").split("|")
        if len(casts) == 0:
            print("skiping_for_casts")
            continue
        summary= items[31]

        yt_id= items[37]

        op_dict.update({
            id: {
                "genre": genres,
                "director": director,
                "rating": rating,
                "casts": casts,
                "summary": summary,
                "yt-id": yt_id
            }
        })
    file.close()

# print(len(op_dict))
object_op_path= helpers.path_of("../objs/meta_raw.obj")
helpers.store_pkl(op_dict, object_op_path)




