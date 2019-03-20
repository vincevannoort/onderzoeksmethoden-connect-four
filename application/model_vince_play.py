# Personal files
from connect_four import ConnectFour, Board, Player

# To build the NN model
from tensorflow import keras

# Helper libraries
import numpy as np
import readchar
from random import choice

"""
Settings
"""    

print("Start loading model")
model = keras.models.load_model(f"connect_four_model_vince.h5")
print("Finished loading model")

first_player = Player("Bot", "B")
second_player = Player("Player", "S")
connect_four = ConnectFour(first_player, second_player)

first_player_type = 'bot'
second_player_type = 'random'

"""
Game loop
"""
games_won = 0;
games_lost = 0;
games_total = 1000;
while (games_won + games_lost) < 1000:
  try:
    if connect_four.current_player is first_player:
      prediction = model.predict(np.array([connect_four.board.get_one_hot_array(connect_four.current_player),]))
      possible_columns = connect_four.board.get_possible_columns_as_one_hot_array()
      for index, possible in enumerate(possible_columns.tolist()):
        if (int(possible) is 0):
          np.put(prediction, index, 0)
      column = np.argmax(prediction)
      connect_four.move(column)
    else:

      if second_player_type == 'player':
        while True:
          try:
            print(f'Player: {connect_four.current_player.name}, select column ( 1 - 7 )?')
            column = int(readchar.readkey()) - 1
            break
          except:
            print('Not a valid number, try again')

      if second_player_type == 'random':
        while True:
          possible_columns = connect_four.board.get_possible_columns()
          column = choice(connect_four.board.get_possible_columns())
          if (column in possible_columns):
            break
        connect_four.move(choice(connect_four.board.get_possible_columns()))

    player_that_has_won = connect_four.has_won()
    if (player_that_has_won is not None):
      connect_four.board.print_with_colors(first_player.signature, second_player.signature)
      print(f"{ player_that_has_won } has won.")
      if player_that_has_won is first_player:
        games_won += 1
      else:
        games_lost += 1

      # reset game
      connect_four.reset()

  except:
    connect_four.reset()

print(f'games won: {games_won}, games lost: {games_lost}')