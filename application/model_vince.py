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

type = 'random'
amount = 70

"""
Parse data
"""
with open(f'../data/{type}/data_unbiased_column_states_connect_four_game_{amount}.txt') as file:
    content = file.readlines()

data = [line.strip().split(";") for line in content[1:]] 
train_data = np.array([ np.fromstring(data_item[0][1:-1], dtype=int, sep=' ') for data_item in data ])
train_data = np.array([np.reshape(board, (height, width, 3)) for board in train_data])
train_labels = np.array([ np.fromstring(data_item[2][1:-1], sep=' ') for data_item in data ])

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    self.model = keras.Sequential([
      keras.layers.Conv2D(16, (3,3), input_shape=(height, width, 3), activation=tf.nn.relu),
      keras.layers.Conv2D(32, (3,3), input_shape=(height, width, 3), activation=tf.nn.relu),
      keras.layers.Flatten(),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      # keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(width, activation=tf.nn.sigmoid),
    ])

    self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  def train(self, train_data, train_labels):
    self.model.fit(train_data, train_labels, epochs=1000, batch_size=64)

connect_four_model = Connect4KerasModel()
connect_four_model.train(train_data, train_labels)
connect_four_model.model.save(f'../models/trained_with_{type}/model_vince_{amount}_moves.h5')