import numpy
import os
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

SIZE_CELL = 100
SIZE_IMG = 1000

def cut(path_img, dir_save):
    img = Image.fromarray(numpy.array(Image.open(path_img)) // 256)
    img = img.convert("RGB")
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    for i in range(0, SIZE_IMG - SIZE_CELL, SIZE_CELL):
        for j in range(0, SIZE_IMG - SIZE_CELL, SIZE_CELL):
            area = (i, j, i + SIZE_CELL, j + SIZE_CELL)
            cropped_img = img.crop(area)
            cropped_img.save(dir_save + '/' + str(i) + '_' + str(j) + '.png', "PNG")
            cropped_img.close()
    img.close()


def cut_expert(path_img, dir_save, select_pts):
    img = Image.fromarray(numpy.array(Image.open(path_img)) // 256)
    img = img.convert("RGB")
    good_dir = dir_save + '/Good'
    bad_dir = dir_save + '/Bad'
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    if not os.path.exists(good_dir):
        os.makedirs(good_dir)
    if not os.path.exists(bad_dir):
        os.makedirs(bad_dir)
    for i in range(0, SIZE_IMG - SIZE_CELL, SIZE_CELL):
        for j in range(0, SIZE_IMG - SIZE_CELL, SIZE_CELL):
            area = (i, j, i + SIZE_CELL, j + SIZE_CELL)
            cropped_img = img.crop(area)
            if (i, j) in select_pts:
                cropped_img.save(bad_dir + '/' + str(i) + '_' + str(j) + '.png', "PNG")
                cropped_img.close()
            else:
                cropped_img.save(good_dir + '/' + str(i) + '_' + str(j) + '.png', "PNG")
                cropped_img.close()
    img.close()


def recognize(model_file, path):
  try:
    model = load_model(model_file)
    img = load_img(path)
  except IOError:
    return -1
  x = img_to_array(img)
  x = x.reshape(1, x.shape[0], x.shape[1], x.shape[2]) # 3D to 4D

  return model.predict(x)[0][0]

#print ("proba clean : " + str(recognize('model.h5', 'data/train/good/500_300.png')))
print ("proba clean : " + str(recognize('model.h5', 'data/train/bad/800_600.png')))
