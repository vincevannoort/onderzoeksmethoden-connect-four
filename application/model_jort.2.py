# To build the NN model
import tensorflow as tf
from tensorflow import keras

# For logging the training
import tensorboard as Tensorboard

# Check if directories exists
import os

# Helper libraries
import numpy as np
import csv
from functools import reduce

class Model:
  def __init__(self, height:int, width:int, log_path:str, model_path:str):
    """
    Settings
    """
    self.height = height
    self.width = width
    self.size = height * width
    self.log_path = log_path
    self.model_path = model_path
    def determine_model_number(counter):
      path = f'{self.model_path}/model_jort_{counter}'
      while (os.path.isfile(path)):
        counter += 1
        path = f'{self.model_path}/model_jort_{counter}'
      return counter
    self.model_number = determine_model_number(0)
    """
    Keras Model
    """
    model = keras.Sequential([
      keras.layers.Dense(self.size, input_dim=self.size, activation=tf.nn.tanh),
      keras.layers.Dense(self.size, activation=tf.nn.tanh),
      keras.layers.Dense(self.size, activation=tf.nn.tanh),
      keras.layers.Dense(self.size, activation=tf.nn.tanh),
      keras.layers.Dense(1, activation=tf.nn.tanh),
    ])
    model.compile(
      optimizer=tf.train.AdamOptimizer(),
      loss='mean_squared_error',
      metrics=['accuracy']
    )
    self.model = model

  def retrieve_data(self, input_path:str):
    # input_path: 'data_from_internet/c4_game_database.csv'
    with open(f"../data/{input_path}", newline="") as csvfile:
      data = list(csv.reader(csvfile))
      return data

  def convert_data(self, data:list):
    # Deletes Header
    del data[0]

    # Remove empty spaces
    data = [list(filter(None, row)) for row in data]
    # Convert input to float
    data = [list(map(float, row)) for row in data]

    train_data = [row[:self.size] for row in data]
    train_data = np.array(train_data)

    test_data = [row[-1] for row in data]
    # Convert [-1, 0, 1] -> [0, 0,5, 1]
    test_data =  [(i+1)/2 for i in test_data]
    test_data = np.array(test_data)

    return (train_data, test_data)

  def create_tensorboard(self):
    # CommandLine: python3 -m tensorboard.main --logdir {LOG_PATH}
    return keras.callbacks.TensorBoard(log_dir=f'{self.log_path}/model_jort_{self.model_number}', histogram_freq=0, write_graph=True, write_images=True)

  def train(self, tensorboard, train_data:list, test_data:list, epochs:int):
    self.model.fit(train_data, test_data, verbose=1, epochs=epochs, callbacks=[tensorboard], validation_split=0.1)

  def save(self):
    self.model.save(f"{self.model_path}/model_jort_{self.model_number}")

  def predict(self, train_data:list, test_data:list):
    predictions = self.model.predict(train_data)
    # Unpack: [[0.3], [0.5], [0.4]] -> [0.3, 0.5, 0.4]
    predictions = [prediction for sublist in predictions for prediction in sublist]
    estimates = list(zip(predictions, test_data))
    [print(f"Prediction: {prediction:.2f} Real: {real}") for (prediction, real) in list(estimates)]

if __name__ == "__main__":
  model = Model(6, 7, '../data/model_logs', '../data/models')
  data = model.retrieve_data('data_from_internet/c4_game_database.csv')
  (train_data, test_data) = model.convert_data(data)
  tensorboard = model.create_tensorboard()
  model.train(tensorboard, train_data, test_data, 1)
  model.save()
  model.predict(np.array(train_data[0:3]), np.array(test_data[0:3]))