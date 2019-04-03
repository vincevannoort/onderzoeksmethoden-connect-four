import numpy as np
<<<<<<< HEAD
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
model = 'winloss'

"""
Parse data
"""
with open(f'../data/{generated_by_using}_model_{model}_{states_to_create}.txt', 'rb') as random_board_states_file:
  content = pickle.load(random_board_states_file)

train_data = np.array([board for (board, column, win) in content])
train_labels = np.array([int(win) for (board, column, win) in content])

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    self.model = keras.Sequential([
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
      keras.layers.Conv2D(64, (3,3), input_shape=(height, width, 2), activation=tf.nn.relu),
=======
import threading

class Model:
  def __init__(self, height:int, width:int, log_path:str, model_path:str):
    """
    Settings
    """
    self.height = height
    self.width = width
    self.size = height * width * 3
    self.log_path = log_path
    self.model_path = model_path
    self.epochs = 10
    def determine_model_number(counter):
      path = f"{self.model_path}/model_jort_{counter}.h5"
      while (os.path.isfile(path)):
        counter += 1
        path = f"{self.model_path}/model_jort_{counter}.h5"
      return counter
    self.model_number = determine_model_number(0)
    """
    Keras Model
    """
    model = keras.Sequential([
      keras.layers.Conv2D(16, (3, 3), input_shape=(self.height, self.width, 3), activation=tf.nn.relu),
      keras.layers.Conv2D(32, (3, 3), input_shape=(self.height, self.width, 3), activation=tf.nn.relu),

>>>>>>> 0a1041691076a5f68c29074927c00aa05e2f014f
      keras.layers.Flatten(),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(inputs, activation=tf.nn.relu),
      keras.layers.Dense(1, activation=tf.nn.sigmoid),
    ])
<<<<<<< HEAD
=======
    model.compile(
      optimizer=tf.train.RMSPropOptimizer(learning_rate=0.001),
      loss='binary_crossentropy',
      metrics=['accuracy']
    )
    self.model = model

  def retrieve_data(self, input_path:str):
    with open(f"../data/{input_path}") as txtfile:
      data = txtfile.readlines()
      del data[0]
      return data

  def retrieve_data_batch(self, input_path:str, offset:int, limit:int):
    """
    Start from offset = 1, because we want to skip the header of the file
    """
    result = []
    with open(f"../data/{input_path}") as txtfile:
      for i, line in enumerate(txtfile):
        if i >= offset and i < offset + limit:
          result.append(line)
        elif i >= offset + limit:
          break
    return result
  
  def get_length_data(self, input_path:str):
    count = 0
    with open(f"../data/{input_path}") as txtfile:
      for line in txtfile: count += 1
    return count

  def convert_data(self, data:list):
    data = [line.rstrip('\n').split(';') for line in data]
    train_data = np.array([np.fromstring(line[0][1:-1], dtype=int, sep=' ') for line in data])
    train_data = np.array([np.reshape(board, (self.height, self.width, 3)) for board in train_data])
    train_labels = np.array([float(line[4]) for line in data])

    return (train_data, train_labels)

  def create_tensorboard(self):
    # CommandLine: python3 -m tensorboard.main --logdir {LOG_PATH}
    return keras.callbacks.TensorBoard(log_dir=f'{self.log_path}/model_jort_{self.model_number}', histogram_freq=0, write_graph=True, write_images=True)


  def generator(self, input_path, batch_size, length, lock):
    """
    Start offset at one to remove the header
    """
    while True:
      with lock:
        print(offset)
        while offset < length:
          input_data_batch = self.retrieve_data_batch(input_path, offset, batch_size)
          (train_data_batch, train_label_batch) = self.convert_data(input_data_batch)
          yield (train_data_batch, train_label_batch)

          offset += batch_size       

  def train(self, train_data:list, test_data:list, tensorboard):
    self.model.fit(train_data, test_data, verbose=1, epochs=self.epochs, callbacks=[tensorboard], validation_split=0.05, batch_size=64, use_multiprocessing=True)

  def train_batch(self, train_data_batch:list, train_label_batch:list):
    self.model.train_on_batch(train_data_batch, train_label_batch)

  def train_generator(self, input_path, batch_size, length):
    self.model.fit_generator(self.generator(input_path, batch_size, length, threading.Lock()), steps_per_epoch=length/batch_size, verbose=1, epochs=self.epochs, callbacks=[self.tensorboard], use_multiprocessing=True, workers=12)
>>>>>>> 0a1041691076a5f68c29074927c00aa05e2f014f

    self.model.compile(optimizer=keras.optimizers.RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['accuracy','mae'])

  def train(self, train_data, train_labels):
    self.model.fit(train_data, train_labels, epochs=50, batch_size=width*3*3)

<<<<<<< HEAD
for index in range(1):
  connect_four_model = Connect4KerasModel()
  connect_four_model.train(train_data, train_labels)
  connect_four_model.model.save(f'../models/trained_with_{generated_by_using}/model_{model}_{states_to_create}_{index}.h5')
=======
if __name__ == "__main__":
  model = Model(6, 7, '../data/model_logs', '../models/trained_with_random')
  data = model.retrieve_data('data_generated/data_win_classify_connect_four_game_moves_500000.txt')
  (train_data, train_labels) = model.convert_data(data)
  tensorboard = model.create_tensorboard()
  print("Starting with training model")
  model.train(train_data, train_labels, tensorboard)
  model.save()
  model.predict(np.array(train_data[0:35]), np.array(train_labels[0:35]))
>>>>>>> 0a1041691076a5f68c29074927c00aa05e2f014f
