from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.models import load_model
from keras import backend as K
import numpy as np

import glob

def assembly(path, num_channel): # path of training - number of chanel
  res = np.array([])
  if path != '':
    path += '/'

  for i in range (num_channel):
    files = glob.glob(path + str(i) + '*')
    if len(files) == 0:
      continue

    for file in files:
      print (file)
      img = load_img(file)
      x = img_to_array(img)
      np.concatenate((res, x))

  return res


def learnImage(filepath): # Save model + weight in filepath
  img_width, img_height = 50, 50
  channel = 3
  nb_train_samples = 480
  nb_validation_samples = 480
  epochs = 400
  batch_size = 39
  filepath = 'model.h5'
  train_data_dir = 'data/train' # Database
  validation_data_dir = 'data/validation'

  if K.image_data_format() == 'channels_first':
    input_shape = (channel, img_width, img_height)
  else:
    input_shape = (img_width, img_height, channel)

  model = Sequential()

  model.add(Conv2D(32, (3, 3), input_shape=input_shape))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Conv2D(32, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Conv2D(64, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))

  model.add(Flatten())
  model.add(Dense(64))
  model.add(Activation('relu'))
  model.add(Dropout(0.55))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))

  model.compile(loss='binary_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])

  train_datagen = ImageDataGenerator(
      rescale=1. / 255,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True)

  test_datagen = ImageDataGenerator(rescale=1. / 255)

  train_generator = train_datagen.flow_from_directory(
      train_data_dir,
      target_size=(img_width, img_height),
      batch_size=batch_size,
      class_mode='binary')

  validation_generator = test_datagen.flow_from_directory(
      validation_data_dir,
      target_size=(img_width, img_height),
      batch_size=batch_size,
      class_mode='binary')

  model.fit_generator(
      train_generator,
      steps_per_epoch=nb_train_samples // batch_size,
      epochs=epochs,
      validation_data=validation_generator,
      validation_steps=nb_validation_samples // batch_size)

  model.save(filepath)
  print('save')

learnImage('model.h5')
#assembly('data/train/bad', 4)

"""
new_model = load_model(filepath)

img = load_img('./data/train/good/500_300.png')

#img = load_img('./data/train/bad/800_600.png')
x = img_to_array(img)

x = x.reshape(1, x.shape[0], x.shape[1], x.shape[2])
# print (model.predict(x))

print (new_model.predict(x))
"""

"""
img = load_img('./450nm.tiff')
x = img_to_array(img)
print (x)
print (len(x[0]))
"""
