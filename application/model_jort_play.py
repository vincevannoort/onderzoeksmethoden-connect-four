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
MODEL_PATH = '../data/models'
MODEL_NUMBER = 11

def predict_board(column:int, board: Board, model, player: Player):
  board = np.array([board.get_one_hot_array(player)])
  board = np.reshape(board, (1, 6, 7, 3))
  prediction = model.predict(board)
  # Convert [[0.4]] -> 0.4
  prediction = prediction[0][0]
  # print(prediction)
  return prediction
    

print("Start loading model")
model = keras.models.load_model(f"{MODEL_PATH}/model_jort_{MODEL_NUMBER}.h5")
print("Finished loading model")

first_player = Player("Bot", 'B')
second_player = Player("Player", 'S')
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
    if(connect_four.current_player is first_player):
      possible_boards_columns = connect_four.possible_boards_columns(first_player)
      shuffle(possible_boards_columns)
      (best_column, best_board) = max(possible_boards_columns, key=lambda board_column: predict_board(*board_column, model, first_player))
      # print(best_column)
      connect_four.move(best_column)
    else:
      # move = int(input("Input move: "))
      move = choice(connect_four.board.get_possible_columns())
      connect_four.move(move)

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

    
