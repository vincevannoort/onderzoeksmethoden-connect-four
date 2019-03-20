import numpy as np
import keras 
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from ast import literal_eval

width = 7
height = 6
inputs = width * height * 3


"""
Parse data
"""
print(f'parse data.')
with open('../data/data_generated/data_row_unbiased_classify_connect_four_game_5_overfit.txt') as file:
    content = file.readlines()

data = [line.strip().split(";") for line in content[1:]] 
train_data = np.array([ np.fromstring(data_item[0][1:-1], dtype=int, sep=' ') for data_item in data ])
train_labels = np.array([ np.fromstring(data_item[2][1:-1], sep=' ') for data_item in data ])

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    self.model = Sequential([
      Dense(inputs, input_shape=(inputs,)),
      Activation('relu'),
      Dense(inputs),
      Activation('relu'),
      Dense(inputs),
      Activation('relu'),
      Dense(width),
      Activation('softmax'),
    ])

    self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # top_k_categorical_accuracy

  def train(self, train_data, train_labels):
    self.model.fit(train_data, train_labels, epochs=15, batch_size=32)


print(f'data & model ready, start training.')
connect_four_model = Connect4KerasModel()
connect_four_model.train(train_data, train_labels)
connect_four_model.model.save('connect_four_model_vince.h5')
input = train_data[0]
prediction = connect_four_model.model.predict(np.array([input,]))
print(prediction)
print(np.argmax(prediction))

# print(np.argmax(predicted[0]))
# # keras.backend.one_hot(input, num_classes)