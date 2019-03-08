import numpy as np
import keras 
from keras.models import Sequential
from keras.layers import Dense, Activation
from ast import literal_eval

width = 7
height = 6
inputs = width * height * 3


"""
Parse data
"""
print(f'parse data.')
with open('../data/data_generated/data_row_classify_connect_four_game_10000.txt') as file:
    content = file.readlines()

data = [line.strip().split(";") for line in content[1:]] 
test_data = np.array([np.array(literal_eval(data_item[0])) for data_item in data])
test_labels = np.array([int(data_item[2]) for data_item in data])
test_labels_one_hot = np.zeros((test_labels.size, 7))
for index, test_label in enumerate(test_labels):
  label = test_labels[index]
  test_labels_one_hot[index][label] = 1

"""
Setup model
"""
class Connect4KerasModel:
  def __init__(self):
    self.model = Sequential([
      Dense(inputs * 3, input_shape=(inputs,)),
      Activation('relu'),
      Dense(inputs * 3),
      Activation('relu'),
      Dense(width),
      Activation('softmax'),
    ])
    self.model.compile(optimizer=keras.optimizers.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

  def train(self, test_data, test_labels_one_hot):
    self.model.fit(test_data, test_labels_one_hot, epochs=25, batch_size=32)


print(f'data & model ready, start training.')
connect_four_model = Connect4KerasModel()
connect_four_model.train(test_data, test_labels_one_hot)
input = test_data[0]
prediction = connect_four_model.model.predict(np.array([input,]))
print(prediction)
print(np.argmax(prediction))

# print(np.argmax(predicted[0]))
# # keras.backend.one_hot(input, num_classes)