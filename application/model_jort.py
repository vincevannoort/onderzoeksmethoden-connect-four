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

"""
Settings
"""
EPOCHS = 1
HEIGHT = 6
WIDTH = 7
SIZE = HEIGHT * WIDTH
LOG_PATH = '../data/model_logs'
MODEL_PATH = '../data/models'

def DetermineModelNumber(counter):
  path = f'{MODEL_PATH}/model_jort_{counter}'
  while (os.path.isdir(path)):
    counter += 1
    path = f'{MODEL_PATH}/model_jort_{counter}'
  return counter

MODEL_NUMBER = DetermineModelNumber(0)

"""
End of Settings
"""

with open('../data/data_from_internet/c4_game_database.csv', newline="") as csvfile:
    data = list(csv.reader(csvfile))

# Deletes Header
del data[0]

# Remove empty spaces
data = [list(filter(None, row)) for row in data]

# Convert input to float
data = [list(map(float, row)) for row in data]

train_data = [row[:SIZE] for row in data]
train_data = np.array(train_data)

test_data = [row[-1] for row in data]
# Convert [-1, 0, 1] -> [0, 0,5, 1]
test_data =  [(i+1)/2 for i in test_data]
test_data = np.array(test_data)

"""
Keras Model
"""
# Creating the model
model = keras.Sequential([
  keras.layers.Dense(SIZE, input_dim=SIZE, activation=tf.nn.tanh),
  keras.layers.Dense(SIZE, activation=tf.nn.tanh),
  keras.layers.Dense(SIZE, activation=tf.nn.tanh),
  keras.layers.Dense(SIZE, activation=tf.nn.tanh),
  keras.layers.Dense(1, activation=tf.nn.tanh),
])

model.compile(
  optimizer=tf.train.AdamOptimizer(),
  loss='mean_squared_error',
  metrics=['accuracy']
)

# Setup tensorboard
# CommandLine: python3 -m tensorboard.main --logdir {LOG_PATH}
tensorboard = keras.callbacks.TensorBoard(log_dir=f'{LOG_PATH}/model_jort_{MODEL_NUMBER}', histogram_freq=0, write_graph=True, write_images=True)
# Train the model with given data
model.fit(train_data, test_data, verbose=1, epochs=EPOCHS, callbacks=[tensorboard], validation_split=0.1)

# Saving the model
model.save(f"{MODEL_PATH}/model_jort_{MODEL_NUMBER}")

# To test my model
def Predict(x):
  prediction = model.predict(np.array([train_data[x]]))
  print(f"Prediction: {prediction} Real: {test_data[x]}")

Predict(0)
Predict(1)
Predict(2)