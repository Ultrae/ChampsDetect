import numpy
import os
from PIL import Image

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
            cropped_img.save(dir_save + '\\' + str(i) + '_' + str(j) + '.png', "PNG")
            cropped_img.close()
    img.close()

