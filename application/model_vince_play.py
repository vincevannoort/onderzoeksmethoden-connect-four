# Personal files
from connect_four import ConnectFour, Board, Player

# To build the NN model
from tensorflow import keras

# Helper libraries
import numpy as np
import readchar

"""
Settings
"""    

print("Start loading model")
model = keras.models.load_model(f"connect_four_model_vince.h5")
print("Finished loading model")

first_player = Player("Bot", "A")
second_player = Player("Player", "B")
connect_four = ConnectFour(first_player, second_player)

"""
Game loop
"""
while True:
  print(f"Getting move from: {connect_four.current_player.name}.")
  if connect_four.current_player is first_player:
    column = np.argmax(model.predict(np.array([connect_four.board.get_one_hot_array(connect_four.current_player),])))
    connect_four.move(column)
  else:
    while True:
      try:
        print(f'Player: {connect_four.current_player.name}, select column ( 1 - 7 )?')
        column = int(readchar.readkey()) - 1
        break
      except:
        print('Not a valid number, try again')
    connect_four.move(column)

  connect_four.board.print_with_colors(first_player.signature, second_player.signature)
  
  
  if (connect_four.has_won()):
    print(f"{ first_player if connect_four.current_player is second_player else second_player } has won.")
    break