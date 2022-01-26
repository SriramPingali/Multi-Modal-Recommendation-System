#
import keras
from keras_applications.resnext import ResNeXt50

from typing import List

from PIL import Image

import numpy as np

imageW, imageH= (224, 224)

model= ResNeXt50(
    weights="imagenet",
    backend= keras.backend,
    layers= keras.layers,
    models= keras.models,
    utils= keras.utils
)

def process_single_image(img_file:str):
    im= Image.open(img_file, 'r')
    im= im.resize((imageW, imageH, ))
    pixel_values= list(im.getdata())
    data= np.array(pixel_values, dtype=int).reshape(-1)
    def range_squish(x): return x/255
    data= range_squish(data)
    return data

def process_image(img_file_arr:List[str]):
    all_images= []
    for img_file in img_file_arr:
        data= process_single_image(img_file)
        if len(data)!= 150528:
            print(len(data))
        if len(data) == 50176:
            data= list(data)+list(data)+list(data)
            print(len(data))
        all_images.append(data)
    all_images= np.array(all_images, dtype=np.float32)
    all_images= all_images.reshape((-1, imageH, imageW, 3))
    assert len(all_images) == len(img_file_arr)
    return all_images


def apply_resnet50(img_file_arr:List[str]):
    ip= process_image(img_file_arr)
    res= model.predict(ip)
    return res





if __name__ == "__main__":
    images= [
        '../liv_data/tmp_files/0hu12MP7b1U_1.jpeg',
        '../liv_data/tmp_files/0hu12MP7b1U_1.jpeg',
        '../liv_data/tmp_files/0hu12MP7b1U_1.jpeg',
    ]
    vector= apply_resnet50(images)
    print(vector.shape)