from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

img = load_img('./450nm.tiff')
x = img_to_array(img)
print (x)
print (len(x[0]))
