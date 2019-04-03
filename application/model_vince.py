import numpy as np
import keras 
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.utils import to_categorical
from ast import literal_eval
from random import shuffle
import pickle

width = 7
height = 6
inputs = width * height

states_to_create = 100000
generated_by_using = 'random'
model = 'columnchoice'

"""
Parse data
"""
with open(f'../data/{generated_by_using}_model_{model}_{states_to_create}.txt', 'rb') as random_board_states_file:
  content = pickle.load(random_board_states_file)

train_data = np.array([board for (board, column, win) in content])
train_labels = np.array([to_categorical(column, 7) for (board, column, win) in content])

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    self.model = keras.Sequential([
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
      keras.layers.Flatten(),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(width, activation=tf.nn.sigmoid),
    ])

    self.model.compile(optimizer=keras.optimizers.Adam(lr=0.001), loss='mse', metrics=['accuracy','mae'])

  def train(self, train_data, train_labels):
    self.model.fit(train_data, train_labels, epochs=50, batch_size=width*3*3)

for index in range(1):
  connect_four_model = Connect4KerasModel()
  connect_four_model.train(train_data, train_labels)
  connect_four_model.model.save(f'../models/trained_with_{generated_by_using}/model_{model}_{states_to_create}_{index}.h5')