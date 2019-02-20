from keras.models import Sequential
from keras.layers import Dense, Activation

width = 7
height = 6
inputs = width * height * 3

model = Sequential([
  Dense(inputs * 3, input_shape=(inputs,)),
  Activation('relu'),
  Dense(inputs * 3),
  Activation('relu'),
  Dense(width),
  Activation('softmax'),
])

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# model.fit(data, labels, epochs=10, batch_size=32)