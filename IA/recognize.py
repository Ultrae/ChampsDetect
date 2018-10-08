from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import os
import sys

def recognize(model_file, path): # model_file : model + weight
    try:
        model = load_model(model_file)
    except IOError:
        print ('no model name ' + model_file)
        return [-1]

    seuil = 0.2
    cpt = 0
    bad_list = []
    for file in os.listdir(path):
        new_file = path + '/' + file
        img = load_img(new_file)
        x = img_to_array(img)
        x = x.reshape(1, x.shape[0], x.shape[1], x.shape[2]) # 3D to 4D

    value = model.predict(x)[0][0]
    if value < seuil:
        bad_list.append(cpt)
    cpt += 1
    return bad_list

if __name__ == '__main__':
    path = sys.argv[1]
    print (recognize('model.h5', path))  # path contains files
