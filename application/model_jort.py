# To build the NN model
import tensorflow as tf
from tensorflow import keras


# For logging the training
import tensorboard as Tensorboard

# Check if directories exists
import os

# Helper libraries
import numpy as np
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
    self.tensorboard = keras.callbacks.TensorBoard(log_dir=f'{self.log_path}/model_jort_{self.model_number}', histogram_freq=0, write_graph=True, write_images=True)
    """
    Keras Model
    """
    model = keras.Sequential([
      keras.layers.Conv2D(16, (3, 3), input_shape=(self.height, self.width, 3), activation=tf.nn.relu),
      keras.layers.Conv2D(32, (3, 3), input_shape=(self.height, self.width, 3), activation=tf.nn.relu),

      keras.layers.Flatten(),
      keras.layers.Dense(self.size, activation=tf.nn.relu),
      keras.layers.Dense(self.size, activation=tf.nn.relu),
      keras.layers.Dense(self.size, activation=tf.nn.relu),
      keras.layers.Dense(1, activation=tf.nn.sigmoid),
    ])
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

  def train(self, train_data:list, test_data:list):
    self.model.fit(train_data, test_data, verbose=1, epochs=self.epochs, callbacks=[self.tensorboard], validation_split=0.1, batch_size=64, use_multiprocessing=True)

  def train_batch(self, train_data_batch:list, train_label_batch:list):
    self.model.train_on_batch(train_data_batch, train_label_batch)

  def train_generator(self, input_path, batch_size, length):
    self.model.fit_generator(self.generator(input_path, batch_size, length, threading.Lock()), steps_per_epoch=length/batch_size, verbose=1, epochs=self.epochs, callbacks=[self.tensorboard], use_multiprocessing=True, workers=12)

  def save(self):
    self.model.save(f"{self.model_path}/model_jort_{self.model_number}.h5")

  def predict(self, train_data:list, test_data:list):
    predictions = self.model.predict(train_data)
    # Unpack: [[0.3], [0.5], [0.4]] -> [0.3, 0.5, 0.4]
    predictions = [prediction for sublist in predictions for prediction in sublist]
    # To print the predictions
    estimates = list(zip(predictions, test_data))
    [print(f"Prediction: {prediction:.2f} Real: {real}") for (prediction, real) in list(estimates)]
    return predictions

if __name__ == "__main__":
  model = Model(6, 7, '../data/model_logs', '../data/models')
  input_path = 'data_generated/data_win_classify_connect_four_game_100000.txt'
  amount_lines = model.get_length_data(input_path)
  model.train_generator(input_path, 64, amount_lines)
  # data = model.retrieve_data('data_generated/data_win_classify_connect_four_game_100000.txt')
  # (train_data, train_labels) = model.convert_data(data)
  # print("Starting with training model")
  # model.train(train_data, train_labels)
  model.save()
  # model.predict(np.array(train_data[0:35]), np.array(train_labels[0:35]))