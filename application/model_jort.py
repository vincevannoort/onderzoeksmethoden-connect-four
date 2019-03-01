# To build the NN Model
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

# For logging the training
import tensorboard as Tensorboard

# Check if Directories exists
import os

# Helper libraries
import numpy as np

import csv

"""
Settings
"""
HEIGHT = 6
WIDTH = 7
SIZE = HEIGHT * WIDTH
LOG_PATH = '../data/model_logs'
MODEL = 0
# CommandLine: python3 -m tensorboard.main --logdir {LOG_PATH}
tensorboard = keras.callbacks.TensorBoard(log_dir=f'{LOG_PATH}/model_{MODEL}', histogram_freq=0, write_graph=True, write_images=True)

with open('../data/c4_game_database.csv', newline="") as csvfile:
    data = list(csv.reader(csvfile))

# Deletes Header
del data[0]

# Remove empty spaces
data = [list(filter(None, row)) for row in data]

# Convert input to float
data = [list(map(float, row)) for row in data]

# TODO convert list to numpy array with shape of (HEIGHT, WIDTH)
input = [row[:SIZE] for row in data]
input = np.array(input)


output = [row[-1] for row in data]

# Convert [-1, 0, 1] -> [0, 0,5, 1]
output =  [(i+1)/2 for i in output]
output = np.array(output)

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

model.fit(input, output, verbose=1, epochs=3, callbacks=[tensorboard], validation_split=0.1)

def Predict(x):
  prediction = model.predict(np.array([input[x]]))
  print(f"Prediction: {prediction} Real: {output[x]}")

Predict(0)
Predict(1)
Predict(2)