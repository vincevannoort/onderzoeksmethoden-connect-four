# Personal files
from connect_four import ConnectFour, Board, Player
from tensorflow import keras

# Helper libraries
import numpy as np
import readchar
from minimax import Minimax
from random import choice
import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

states_to_create = 100000
generated_by_using = 'random'

print("Start loading model")
# model_random_vince = keras.models.load_model(f"../models/trained_with_{generated_by_using}/model_vince_{states_to_create}_moves_0.h5")
model_random_vince = keras.models.load_model(f"../models/trained_with_{generated_by_using}/model_columnchoice_{states_to_create}_0.h5")
model_random_jort = keras.models.load_model(f"../models/trained_with_{generated_by_using}/model_winloss_{states_to_create}_0.h5",)
print("Finished loading model")

"""
CONFIGURATION
"""
configuration = 'player_vs_model_random_vince'
games_to_play = 1000
play_slow = False

if configuration is 'model_random_jort_vs_model_random_vince':
  first_player = Player("Vince", "V", "model_vince", model_random_vince)
  second_player = Player("Jort", "J", "model_jort", model_random_jort)
elif configuration is 'model_random_jort_vs_random':
  first_player = Player("Jort", "J", "model_jort", model_random_jort)
  second_player = Player("Random", "R", "random")
elif configuration is 'model_random_vince_vs_random':
  first_player = Player("Vince", "V", "model_vince", model_random_vince)
  second_player = Player("Random", "R", "random")
elif configuration is 'model_minimax_jort_vs_model_minimax_vince':
  pass
elif configuration is 'model_minimax_jort_vs_random':
  pass
elif configuration is 'model_minimax_vince_vs_random':
  pass
elif configuration is 'random_vs_random':
  first_player = Player("Random", "A", "random")
  second_player = Player("Random", "B", "random")
elif configuration is 'player_vs_model_random_vince':
  first_player = Player("Vince", "V", "player")
  second_player = Player("Bot Vince", "B", "model_vince", model_random_vince)
elif configuration is 'player_vs_model_random_jort':
  first_player = Player("Jort", "J", "player")
  second_player = Player("Bot Jort", "B", "model_jort", model_random_jort)
elif configuration is 'player_vs_player':
  first_player = Player("Vince", "V", "player")
  second_player = Player("Jort", "J", "player")

games_won = 0
games_lost = 0
games_draw = 0
connect_four = ConnectFour(first_player, second_player)

while (games_won + games_lost) < games_to_play:
  connect_four.current_player.play_move(connect_four)
  player_that_has_won = connect_four.has_won()

  if play_slow:
    cls()
    connect_four.board.print_with_colors(first_player.signature, second_player.signature)
    time.sleep(0.3)

  if (player_that_has_won is not None):
    if player_that_has_won is first_player:
      games_won += 1
    else:
      games_lost += 1
    connect_four.reset()
    
  if connect_four.is_draw():
    games_draw += 1
    connect_four.reset()

print(f'{games_draw} games ended in a draw.')
print(f'{first_player.name} has won {games_won} and lost {games_lost} games.')
print(f'{second_player.name} has won {games_lost} and lost {games_won} games.')