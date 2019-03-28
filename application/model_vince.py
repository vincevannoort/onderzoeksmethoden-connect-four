import numpy as np
import keras 
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from ast import literal_eval
from random import shuffle

width = 7
height = 6
inputs = width * height * 3


"""
Parse data
"""
# print(f'parse data.')
with open('../data/data_generated/data_row_unbiased_classify_connect_four_game_100_overfit.txt') as file:
    content = file.readlines()

data = [line.strip().split(";") for line in content[1:]] 
shuffle(data)
train_data = np.array([ np.fromstring(data_item[0][1:-1], dtype=int, sep=' ') for data_item in data ])
train_data = np.array([np.reshape(board, (height, width, 3)) for board in train_data])
train_labels = np.array([ np.fromstring(data_item[2][1:-1], sep=' ') for data_item in data ])

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    # self.model = Sequential([
    #   Dense(inputs, input_shape=(inputs,)),
    #   Activation('relu'),
    #   Dense(inputs * 5),
    #   Activation('relu'),
    #   Dense(inputs * 2),
    #   Activation('relu'),
    #   Dense(width),
    #   Activation('softmax'),
    # ])
    self.model = keras.Sequential([
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 3), activation=tf.nn.relu),
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 3), activation=tf.nn.relu),
      keras.layers.BatchNormalization(),
      # keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 3), activation=tf.nn.relu),
      # keras.layers.MaxPooling2D(pool_size=(2,2)),
      keras.layers.Flatten(),
      # keras.layers.Dense(inputs * 3, activation=tf.nn.relu),
      # keras.layers.Dense(inputs * 2, activation=tf.nn.relu),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(width, activation=tf.nn.sigmoid),
    ])

    self.model.compile(optimizer=keras.optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004), loss='categorical_crossentropy', metrics=['accuracy'])
    # self.model.compile(optimizer='adam', loss='poisson', metrics=['accuracy'])

  def train(self, train_data, train_labels):
    config = tf.ConfigProto(device_count={"CPU": 8})
    keras.backend.tensorflow_backend.set_session(tf.Session(config=config))
    self.model.fit(train_data, train_labels, epochs=5, batch_size=64, validation_split=0.05)


# print(f'data & model ready, start training.')
connect_four_model = Connect4KerasModel()
connect_four_model.train(train_data, train_labels)
connect_four_model.model.save('connect_four_model_vince_unbiased.h5')
input = train_data[0]
prediction = connect_four_model.model.predict(np.array([input,]))
print(prediction)
print(np.argmax(prediction))

# print(np.argmax(predicted[0]))
# # keras.backend.one_hot(input, num_classes)