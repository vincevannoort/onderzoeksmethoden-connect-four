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

WIDTH = 7
HEIGHT = 6

with open('../data/c4_game_database.csv', newline="") as csvfile:
    data = list(csv.reader(csvfile))

# Deletes Header
del data[0]

# Remove empty spaces
data = [list(filter(None, row)) for row in data]

# Convert input to float
data = [list(map(float, row)) for row in data]

# TODO convert list to numpy array with shape of (HEIGHT, WIDTH)
input = [ row[:-2] for row in data ]
input = [np.asarray(row) for row in input]
input = np.asarray(input)
print(input.shape)

output = [ row[-1] for row in data ]

# Convert [-1, 0, 1] -> [0, 0,5, 1]
output =  [(i+1)/2 for i in output]
output = np.asarray(output)
print(output.shape)

"""
Keras Model
"""

# Creating the model
model = keras.Sequential([
  keras.layers.Flatten(input_shape=(HEIGHT, WIDTH)),
  keras.layers.Dense(HEIGHT * WIDTH, activation=tf.nn.sigmoid),
  keras.layers.Dense(1, activation=tf.nn.softmax),
])

model.compile(
  optimizer=tf.train.AdamOptimizer(),
  loss='binary_crossentropy',
  metrics=['accuracy']
)

print("Got here")
model.fit(input, output, verbose=1, epochs=1)
print("Got here 2")