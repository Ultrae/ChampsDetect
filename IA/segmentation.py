from PIL import Image
from reconnaissance import cut_expert
from reconnaissance import SIZE_CELL
from reconnaissance import SIZE_IMG
import cv2
import os
import random

coords = []
def select(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            coords.append((x - (x % SIZE_CELL), y - (y % SIZE_CELL)))

FOLDER_OF_PHOTO = 'bdd/0-018331-16000'
FOLDER_WHERE_SAVE = 'data/train/temp'
PHOTO_NAME = '466nm.tiff'
PHOTO_NUMBER = '0_'

imcv = cv2.imread(FOLDER_OF_PHOTO + '.png')
cv2.namedWindow('image', 0)

for x in range(0, SIZE_IMG, SIZE_CELL):
    for y in range(0, SIZE_IMG, SIZE_CELL):
        cv2.line(imcv, (0, y), (SIZE_IMG, y), (0, 255, 255))
        cv2.line(imcv, (x, 0), (x, SIZE_IMG), (0, 255, 255))
cv2.imshow('image', imcv)
cv2.resizeWindow('image', 600, 600)
cv2.setMouseCallback('image', select)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(coords)

cut_expert(FOLDER_OF_PHOTO + '/' + PHOTO_NAME, FOLDER_WHERE_SAVE, coords, PHOTO_NUMBER)
