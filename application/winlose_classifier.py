import numpy as np
import keras 
import tensorflow as tf
from random import shuffle
import pickle
import argparse

class WinLoseClassifier:
  def __init__(self, args):
    self.height = 6
    self.width = 7
    self.epochs = 10
    self.batch_size = 7 * 3 * 3

    # Loading training data
    (train_states, train_labels) = self.loading_train_data(args)
    self.train_states = train_states
    self.train_labels = train_labels
    
  def create_model(self):
    model = keras.Sequential([
      keras.layers.Conv2D(64, (3,3), input_shape=(self.height, self.width, 2), activation=tf.nn.relu),
      keras.layers.Conv2D(64, (3,3), input_shape=(self.height, self.width, 2), activation=tf.nn.relu),
      keras.layers.Flatten(),
      keras.layers.Dense(self.width * self.height, activation=tf.nn.relu),
      keras.layers.Dense(self.width * self.height, activation=tf.nn.relu),
      keras.layers.Dense(1, activation=tf.nn.sigmoid),
    ])
    model.compile(optimizer=keras.optimizers.RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['accuracy','mae'])  
    return model

  def loading_train_data(self, args):
    states = []
    if(args.winning > 0):
      with open(f"../data/random_winning_100000.pickle", 'rb') as winning_states_file:
        winning_states = pickle.load(winning_states_file)
        states += winning_states[:args.winning]
    if(args.blocking > 0):
      with open(f"../data/random_blocking_100000.pickle", 'rb') as blocking_states_file:
        blocking_states = pickle.load(blocking_states_file)
        states += blocking_states[:args.blocking]
    if(args.random_winning + args.random_losing > 0):
      with open(f"../data/random_random_200000.pickle", 'rb') as random_states_file:
        random_states = pickle.load(random_states_file)
        random_winning_states = list(filter(lambda state: state[3], random_states))
        random_losing_states = list(filter(lambda state: not state[3], random_states))
        states += random_winning_states[:args.random_winning]
        states += random_losing_states[:args.random_losing]
    
    train_states = np.array([current_board for (_, current_board, _, _) in states])
    train_labels = np.array([int(win) for (_, _, _, win) in states])
    return (train_states, train_labels)


  def train(self):
    self.model.fit(self.train_states, self.train_labels, epochs=self.epochs, batch_size=self.batch_size)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning", "-w", help="amount of winning moves", type=int, default=25000)
  parser.add_argument("--blocking", "-b", help="amount of blocking moves", type=int, default=25000)
  parser.add_argument("--random_winning", "-rw", help="amount of random winning moves", type=int, default=25000)
  parser.add_argument("--random_losing", "-rl", help="amount of random losing moves", type=int, default=75000)
  parser.add_argument("--amount", "-a", help="amount of models to create", type=int, default=1)
  args = parser.parse_args()

  classifier = WinLoseClassifier(args)

  for index in range(args.amount):
    classifier.model = classifier.create_model()
    classifier.train()
    classifier.model.save(f"../models/t{args.winning + args.blocking + args.random_winning + args.random_losing}_w{args.winning}_b{args.blocking}_rw{args.random_winning}_rl{args.random_losing}_model_winlose_{index}.h5")