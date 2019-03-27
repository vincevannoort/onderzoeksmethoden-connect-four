# Personal files
from connect_four import ConnectFour, Board, Player

# To build the NN model
from tensorflow import keras

# Helper libraries
import numpy as np
import readchar
from minimax import Minimax
from random import choice
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

"""
Settings
"""    

print("Start loading model")
model = keras.models.load_model(f"connect_four_model_vince_unbiased.h5")
print("Finished loading model")

first_player = Player("Eva", "E")
second_player = Player("Vince", "V")
connect_four = ConnectFour(first_player, second_player)
connect_four.current_player = first_player

first_player_type = 'bot'
second_player_type = 'player'

"""
Game loop
"""
games_won = 0;
games_lost = 0;
games_total = 1000;
while (games_won + games_lost) < games_total:
  cls()
  connect_four.board.print_with_colors(first_player.signature, second_player.signature)
  if connect_four.current_player is first_player:
    board_representation = np.array(connect_four.board.get_one_hot_array(connect_four.current_player))
    board_representation = np.reshape(board_representation, (connect_four.board.height, connect_four.board.width, 3))
    prediction = model.predict(np.array([board_representation,]))
    possible_columns = connect_four.board.get_possible_columns_as_one_hot_array()
    print(prediction)
    for index, possible in enumerate(possible_columns.tolist()):
      if (int(possible) is 0):
        np.put(prediction, index, 0)
    print(prediction)
    column = np.argmax(prediction)
    connect_four.move(column)
  else:
    if second_player_type == 'player':
      while True:
        try:
          print(f'Player: {connect_four.current_player.name}, select column ( 1 - 7 )?')
          column = int(readchar.readkey()) - 1
          connect_four.move(column)
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

print(f'games won: {games_won}, games lost: {games_lost}')