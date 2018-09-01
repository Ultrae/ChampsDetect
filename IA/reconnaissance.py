import numpy
import os
import re
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import sys

SIZE_CELL = 50
SIZE_IMG = 1000

def get_savename(path_img, dir_save, i, j):
    return dir_save + '/' + re.search(".*[^(\.tiff)]", path_img).group(0) + '-' + str(i) + '_' + str(j) + '.png'

def cut(path_img, dir_save):
    img = Image.fromarray(numpy.array(Image.open(path_img)) // 256)
    img = img.convert("RGB")
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    for i in range(0, SIZE_IMG, SIZE_CELL):
        for j in range(0, SIZE_IMG, SIZE_CELL):
            # Crop
            area = (i, j, i + SIZE_CELL, j + SIZE_CELL)
            cropped_img = img.crop(area)
            # Cell name
            pattern = re.compile('[0-9]+nm.tiff')
            pos = pattern.search(path_img)
            tuple_pos = pos.span()
            filename = path_img[tuple_pos[0]:tuple_pos[1]]
            # Save cell
            cropped_img.save(get_savename(filename, dir_save, i, j))
            cropped_img.close()
    img.close()


def cut_expert(path_img, dir_save, select_pts):
    img = Image.fromarray(numpy.array(Image.open(path_img)) // 256)
    img = img.convert("RGB")
    good_dir = dir_save + '/good'
    bad_dir = dir_save + '/bad'
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    if not os.path.exists(good_dir):
        os.makedirs(good_dir)
    if not os.path.exists(bad_dir):
        os.makedirs(bad_dir)
    for i in range(0, SIZE_IMG, SIZE_CELL):
        for j in range(0, SIZE_IMG, SIZE_CELL):
            area = (i, j, i + SIZE_CELL, j + SIZE_CELL)
            cropped_img = img.crop(area)
            if (i, j) in select_pts:
                cropped_img.save(get_savename(path_img, bad_dir, i, j), "PNG")
                cropped_img.close()
            else:
                cropped_img.save(get_savename(path_img, good_dir, i, j), "PNG")
                cropped_img.close()
    img.close()


def recognize(model_file, path): # model_file : model + weight
  try:
    model = load_model(model_file)
  except IOError:
    print ('no good model')
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
    cpt += 1
    if value < seuil:
      bad_list.append(cpt)
  return bad_list

def color(img_r, img_g, img_b):
    R = numpy.array(Image.open(img_r)) // 256
    G = numpy.array(Image.open(img_g)) // 256
    B = numpy.array(Image.open(img_b)) // 256
    data = [(R[i // SIZE_IMG][i % SIZE_IMG], G[i // SIZE_IMG][i % SIZE_IMG], B[i // SIZE_IMG][i % SIZE_IMG])
            for i in range(SIZE_IMG * SIZE_IMG)]

    img = Image.new('RGB', (SIZE_IMG, SIZE_IMG))
    img.putdata(data)
    return img

if __name__ == '__main__':
  path = sys.argv[1]
  print (recognize('model.h5', path))
