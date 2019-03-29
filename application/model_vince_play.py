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
model_minimax = keras.models.load_model(f"../models/trained_with_minimax/model_vince_17500_moves.h5")
model_random = keras.models.load_model(f"../models/trained_with_random/model_jort_500000_moves.h5", compile=True)
print("Finished loading model")

first_player = Player("Bot", "B", "model_vince", model_minimax)
second_player = Player("Opposite", "O", "model_jort", model_random)
connect_four = ConnectFour(first_player, second_player)

"""
Game loop
"""
games_won = 0;
games_lost = 0;
games_total = 100;
while (games_won + games_lost) < games_total:
  # cls()
  connect_four.board.print_with_colors(first_player.signature, second_player.signature)
  connect_four.current_player.play_move(connect_four)
  player_that_has_won = connect_four.has_won()
  if (player_that_has_won is not None):
    connect_four.board.print_with_colors(first_player.signature, second_player.signature)
    print(f"{ player_that_has_won } has won.")
    if player_that_has_won is first_player:
      games_won += 1
    else:
      games_lost += 1
    connect_four.reset()

print(f'games won: {games_won}, games lost: {games_lost}')