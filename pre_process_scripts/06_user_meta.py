import helpers
import csv

users_meta_file= helpers.path_of("../Text/u.user")

occupation= ["administrator", "artist", "doctor", "educator", "engineer", "entertainment", "executive", "healthcare", "homemaker", "lawyer", "librarian", "marketing", "none", "other", "programmer", "retired", "salesman", "scientist", "student", "technician", "writer"]


user_meta_op_file= helpers.path_of("../objs/user_meta.obj")



def one_hot_occupation(occ):
    res= [0 for x in occupation]
    for index, val in enumerate(occupation):
        if val==occ:
            res[index]= 1
    return res

user_meta= dict()

with open(users_meta_file) as file:
    for line in file:
        items= list(csv.reader([line], delimiter="|"))[0]
        user_id, age, gender, occ= items[:4]
        user_id= int(user_id)
        age= (int(age)/100)
        gender= 0 if gender=='M' or gender=='m' else 1
        occ= one_hot_occupation(occ)

        user_meta_concated= [age]+[gender]+occ

        user_meta.update({
            user_id: user_meta_concated,
        })
    file.close()

print("META_LEN: ", len(user_meta_concated))

helpers.store_pkl(user_meta, user_meta_op_file)



