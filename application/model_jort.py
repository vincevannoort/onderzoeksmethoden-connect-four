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
  
  def predict(self, train_data, train_labels):
    predictions = self.model.predict(train_data)
    for x in range(len(predictions)):
      print(f"Prediction: {predictions[x]}. Label: {train_labels[x]}")
      

if __name__ == '__main__':
  """
  example: python3.6 model_jort.py -w 7 -b 7 -r 0 -t minimax
  description: generate models given training data
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning", "-w", help="amount of winning moves", type=int, default=100000)
  parser.add_argument("--blocking", "-b", help="amount of blocking moves", type=int, default=100000)
  parser.add_argument("--random", "-r", help="amount of random moves", type=int, default=200000)
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", type=str, default='random')
  parser.add_argument("--amount", "-a", help="amount of models to create", type=int, default=1)
  args = parser.parse_args()
  
  states = []
  if (args.winning > 0):
    with open(f'../data/{args.type}_winning_{args.winning}.pickle', 'rb') as board_states_file:
      states_from_file = pickle.load(board_states_file)
      states += states_from_file[:25000]

  if (args.blocking > 0):
    with open(f'../data/{args.type}_blocking_{args.blocking}.pickle', 'rb') as board_states_file:
      states_from_file = pickle.load(board_states_file)
      states += states_from_file[:25000]

  if (args.random > 0):
    with open(f'../data/{args.type}_random_{args.random}.pickle', 'rb') as board_states_file:
      states_from_file = pickle.load(board_states_file)
      states_from_file_winning = list(filter(lambda state: state[3], states_from_file))
      states_from_file_losing = list(filter(lambda state: not state[3], states_from_file))
      states += states_from_file_winning[:75000]
      states += states_from_file_losing[:75000]

  train_data = np.array([current_board for (_, current_board, _, _) in states])
  train_labels = np.array([int(win) for (_, _, _, win) in states])

  for index in range(args.amount):
    connect_four_model = Connect4KerasModel(7, 6)
    connect_four_model.train(train_data, train_labels, 7 * 3 * 3)
    # connect_four_model.predict(np.array(train_data[1:10]), np.array(train_labels[1:10]))
    connect_four_model.model.save(f'../models/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_winlose_{index}.h5')
