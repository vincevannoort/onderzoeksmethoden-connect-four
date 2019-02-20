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

with open('../data/c4_game_database.csv', newline="") as csvfile:
    data = list(csv.reader(csvfile))

# Deletes Header
del data[0]

# Remove empty spaces
data = [list(filter(None, row)) for row in data]

# Convert input to float
data = [list(map(float, row)) for row in data]

input = [ row[:-2] for row in data ]

output = [ row[-1] for row in data ]

"""
Keras Model
"""

Creating the model
model = keras.Sequential([
  keras.layers.Dense()
])