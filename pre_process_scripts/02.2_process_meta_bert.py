

import helpers
import bert_encoder

import kg_builder

meta_raw_path= helpers.path_of("../objs/meta_raw.obj")
meta_raw= helpers.load_pkl(meta_raw_path)

meta_processed_op_oath= helpers.path_of("../objs/meta_processed.obj")

w2v_file_path= helpers.path_of("../word_vector_300d.vec")



def filter_and_preprocess_lines(lines_arr):
    res= list()
    for l in lines_arr:
        l= l.lstrip(" ").rstrip(" ")
        if len(l)==0: continue
        if len(l.split(" "))<4: continue
        res.append(l)
    return res

def concat_encoded(encoded_arr):
    res= list()
    for item in encoded_arr:
        res.extend(item)
    return res

def avg_encode(encoded_arr):
    res= [0 for x in range(len(encoded_arr[0]))]
    for enc in encoded_arr:
        for ind, val in enumerate(enc):
            res[ind]+=val
    for index in range(len(res)):
        res[index]= res[index]/len(encoded_arr)
    return res





def encode_description(meta_raw, lines_to_take):
    all_lines= []
    all_movie_id= list(meta_raw.keys()).copy()

    for movie_id in all_movie_id:
        movie_meta= meta_raw.get(movie_id)
        description= movie_meta.get("summary")
        all_lines.append(description)

    encoded= bert_encoder.encode(all_lines, get_avg_of_each_paragraph=True, max_lines_to_take=lines_to_take)

    res= dict()
    for index, movie_id in enumerate(all_movie_id):
        res.update({
            movie_id: encoded[index].tolist()
        })
    return res

# encode_description(meta_raw, 20)



def encode_director(meta_raw):

    all_movie_id= list(meta_raw.keys())

    director_split_vectors= dict()

    for movie_id in all_movie_id:
        movie_meta= meta_raw.get(movie_id)
        director_name= movie_meta.get("director")
        director_split= director_name.split(" ")
        for d in director_split:
            d= d.lower()
            director_split_vectors.update({
                d: False
            })


    with open(w2v_file_path) as file:
        for line in file:
            line= line.rstrip("\n")
            items= line.split(" ")
            word= items[0].lower()
            if director_split_vectors.get(word) is not None:
                vector= [float(x) for x in items[1:]]
                director_split_vectors.update({
                    word: vector,
                })
        file.close()

    director_encoding= dict()

    for movie_id in all_movie_id:
        movie_meta= meta_raw.get(movie_id)
        director_name= movie_meta.get("director")
        director_split= director_name.split(" ")
        enc= list()
        for d in director_split:
            d= d.lower()
            if director_split_vectors.get(d):
                enc.append(director_split_vectors.get(d))

        enc= helpers.to_same_shape(enc, 2)
        enc= avg_encode(enc)

        director_encoding.update({
            movie_id: enc,
        })

    return director_encoding

        

# encode_director(meta_raw)


def encode_genre(meta_raw):
    all_movie_id= list(meta_raw.keys())

    genre_encoded= dict()

    for movie_id in all_movie_id:
        movie_meta= meta_raw.get(movie_id)
        genre= movie_meta.get("genre")
        genre_encoded.update({
            movie_id: genre,
        })
    return genre_encoded
        
# encode_genre(meta_raw)


def encode_rating(meta_raw):
    all_movie_id= list(meta_raw.keys())

    rating_encoded= dict()

    for movie_id in all_movie_id:
        movie_meta= meta_raw.get(movie_id)
        rating= movie_meta.get("rating")

        rating= rating/10

        rating_encoded.update({
            movie_id: [rating],
        })
    return rating_encoded

# encode_rating(meta_raw)


def encode_everything():

    enc_desc= encode_description(meta_raw, 15)
    print("[*] Description encoding completed...\n")
    enc_genre= encode_genre(meta_raw)
    print("[*] Genre encoding completed...\n")
    enc_direc= encode_director(meta_raw)
    print("[*] Director encoding completed...\n")
    enc_rate= encode_rating(meta_raw)
    print("[*] Rating encoding completed...\n")

    metadata_encoded= dict()

    all_movie_id= list(meta_raw.keys())
    for movie_id in all_movie_id:
        de= enc_desc.get(movie_id)
        ge= enc_genre.get(movie_id)
        di= enc_direc.get(movie_id)
        ra= enc_rate.get(movie_id)

        enc_concated= list()
        enc_concated.extend(de)
        enc_concated.extend(ge)
        enc_concated.extend(di)
        enc_concated.extend(ra)
        
        print(len(enc_concated))
        metadata_encoded.update({
            movie_id: enc_concated,
        })

    # print(metadata_encoded.get(1))

    helpers.store_pkl(metadata_encoded, meta_processed_op_oath)
        



if __name__ == "__main__":
    encode_everything()


