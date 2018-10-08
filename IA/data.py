import numpy
import os
import re
from PIL import Image

SIZE_CELL = 50
SIZE_IMG = 1000

def get_nb_digits(i):
    ndigits = 0
    if i == 0:
        return 1
    while i != 0:
        ndigits += 1
        i //= 10

    return ndigits

def get_savename(path_img, dir_save, i, j, no_file=''):
    i_ndigits = get_nb_digits(i)
    j_ndigits = get_nb_digits(j)

    name = dir_save + '/' + no_file + re.search(".*[^(\.tiff)]", path_img).group(0) + '-'

    n_zero = 3 - i_ndigits
    i_str = (str(0) * n_zero) + str(i)
    n_zero = 3 - j_ndigits
    j_str = (str(0) * n_zero) + str(j)

    name += i_str + '_' + j_str + '.png'

    return name

def cut(path_img, dir_save):
    img = Image.fromarray(numpy.array(Image.open(path_img)) // 256)
    img = img.convert("RGB")
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    for i in range(0, SIZE_IMG, SIZE_CELL):
        for j in range(0, SIZE_IMG, SIZE_CELL):
            #Crop
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

def cut_jpg_png(path_img, dir_save):
    img = Image.fromarray(numpy.array(Image.open(path_img)))
    img = img.convert("RGB")
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
    for i in range(0, SIZE_IMG, SIZE_CELL):
        for j in range(0, SIZE_IMG, SIZE_CELL):
            #Crop
            area = (i, j, i + SIZE_CELL, j + SIZE_CELL)
            cropped_img = img.crop(area)
            # Cell name
            pattern = re.compile('[0-9]+nm.[tiff|jpg|png]')
            pos = pattern.search(path_img)
            tuple_pos = pos.span()
            filename = path_img[tuple_pos[0]:tuple_pos[1]]
            # Save cell
            cropped_img.save(get_savename(filename, dir_save, i, j))
            cropped_img.close()
    img.close()


def cut_expert(path_img, dir_save, select_pts, no_file=''):
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
                cropped_img.save(get_savename(re.search('[^/]*$', path_img).group(0), bad_dir, i, j, no_file), "PNG")
                cropped_img.close()
            else:
                cropped_img.save(get_savename(re.search('[^/]*$', path_img).group(0), good_dir, i, j, no_file), "PNG")
                cropped_img.close()
    img.close()

def color(img_r, img_g, img_b):
    img_R = Image.open(img_r)
    R = numpy.array(img_R) // 256
    G = numpy.array(Image.open(img_g)) // 256
    B = numpy.array(Image.open(img_b)) // 256
    width = img_R.width
    data = [(R[i // width][i % width], G[i // width][i % width], B[i // width][i % width])
              for i in range(width * width)]

    img = Image.new('RGB', (width, width))
    img.putdata(data)
    return img
