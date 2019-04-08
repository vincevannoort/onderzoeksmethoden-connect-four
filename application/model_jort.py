import numpy as np
import keras 
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.utils import to_categorical
from ast import literal_eval
from random import shuffle
import pickle
import argparse

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self, width, height):
    self.model = keras.Sequential([
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
      keras.layers.Flatten(),
      keras.layers.Dense(width * height, activation=tf.nn.relu),
      keras.layers.Dense(width * height, activation=tf.nn.relu),
      keras.layers.Dense(1, activation=tf.nn.sigmoid),
    ])

    self.model.compile(optimizer=keras.optimizers.RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['accuracy','mae'])

  def train(self, train_data, train_labels, batch_size):
    self.model.fit(train_data, train_labels, epochs=10, batch_size=batch_size)

if __name__ == '__main__':
  """
  example: python3.6 model_jort.py -w 7 -b 7 -r 0 -t minimax
  description: generate models given training data
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning", "-w", help="amount of winning moves", type=int, default=7)
  parser.add_argument("--blocking", "-b", help="amount of blocking moves", type=int, default=7)
  parser.add_argument("--random", "-r", help="amount of random moves", type=int, default=0)
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", type=str, default='minimax')
  parser.add_argument("--amount", "-a", help="amount of models to create", type=int, default=1)
  args = parser.parse_args()
  
  with open(f'../data/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_winloss.txt', 'rb') as board_states_file:
    content = pickle.load(board_states_file)

  train_data = np.array([board for (board, column, win) in content])
  train_labels = np.array([int(win) for (board, column, win) in content])

  for index in range(args.amount):
    connect_four_model = Connect4KerasModel(7, 6)
    connect_four_model.train(train_data, train_labels, 7 * 3 * 3)
    connect_four_model.model.save(f'../models/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_winloss_{index}.h5')
