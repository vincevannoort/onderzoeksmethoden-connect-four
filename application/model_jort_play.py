# Personal files
from connect_four import ConnectFour, Board, Player

# To build the NN model
from tensorflow import keras

# Helper libraries
import numpy as np
from random import choice, shuffle

"""
Settings
"""
MODEL_PATH = '../models/trained_with_random'
MODEL_NUMBER = 0
  
print("Start loading model")
model = keras.models.load_model(f"{MODEL_PATH}/model_jort_{MODEL_NUMBER}.h5")
print("Finished loading model")

first_player = Player("Bot", 'B', "model_jort")
second_player = Player("Player", 'S', "player")
connect_four = ConnectFour(first_player, second_player)

"""
Game loop
"""
amount_of_games = 0
amount_won_bot = 0
amount_won_random = 0

while(amount_of_games < 1000):
  while True:
    # print(f"move from: {connect_four.current_player.name}.")
    connect_four.current_player.play_move(connect_four, model)

    won_player = connect_four.has_won()
    if(won_player is not None):
      # print(f"{won_player.name} has won.")
      if(won_player == first_player):
        amount_won_bot += 1
      else:
        amount_won_random += 1
      connect_four.reset()
      break
    elif(connect_four.is_draw()):
      # print("It's a draw")
      connect_four.reset()
      break

    # print(connect_four.board)
  
  amount_of_games += 1
  if(amount_of_games % 100 == 0):
    print(f"Amount of Games: {amount_of_games}. Games won by bot: {((amount_won_bot/amount_of_games)*100):.2f}%. Games won by random: {((amount_won_random/amount_of_games)*100):.2f}%.")

    
