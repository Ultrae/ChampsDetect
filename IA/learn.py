from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense, Input
from keras.models import load_model
from keras import backend as K
from keras.applications.vgg16 import VGG16
import numpy as np

import glob

def Vgg16(width, height, channel):
  input_tensor = Input(shape=(width, height, channel))
  vgg16 = VGG16(include_top=False, weights='imagenet',
          input_tensor=input_tensor)

  top_model = Sequential()
  top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
  top_model.add(Dense(512, activation='relu'))
  top_model.add(Dropout(0.5))
  top_model.add(Dense(256, activation='relu'))
  top_model.add(Dropout(0.5))
  top_model.add(Dense(1, activation='sigmoid'))

  model = Model(input=vgg16.input, output=top_model(vgg16.output))
  for layer in model.layers[:13]:
    layer.trainable = False

  return model

def Cnn():
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
  model.add(Dropout(0.2))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))

  return model

def learnImage(filepath): # Save model + weight in filepath
  img_width, img_height = 50, 50
  channel = 3
  nb_train_samples = 58
  nb_validation_samples = 58
  epochs = 100
  batch_size = 14
  train_data_dir = 'data/train' # Database for learning
  validation_data_dir = 'data/validation' # Database for testing

  if K.image_data_format() == 'channels_first':
    input_shape = (channel, img_width, img_height)
  else:
    input_shape = (img_width, img_height, channel)

  """
  model = Cnn()
  """

  model = Vgg16(img_width, img_height, channel)


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

  model.save_weights(filepath + '_weight.h5')
  model.save(filepath + '.h5')
  print('save in ' + filepath)

learnImage('model')
