# Personal files
from connect_four import ConnectFour, Board, Player

# To build the NN model
from tensorflow import keras

# Helper libraries
import numpy as np

"""
Settings
"""
MODEL_PATH = '../data/models'
MODEL_NUMBER = 0

def predict_board(column:int, board: Board, model):
  board = np.array([board.holes])
  prediction = model.predict(board)
  # Convert [[0.4]] -> 0.4
  prediction = prediction[0][0]
  return prediction
    

print("Start loading model")
model = keras.models.load_model(f"{MODEL_PATH}/model_jort_{MODEL_NUMBER}.h5")
print("Finished loading model")

connect_four = ConnectFour()
first_player = Player("Bot", 1)
second_player = Player("Player", -1)
current_player = first_player

"""
Game loop
"""
while True:
    
  print(f"move from: {current_player.name}.")
  if current_player is first_player:
    possible_boards = connect_four.possible_boards(first_player)
    (best_column, best_board) = max(possible_boards, key=lambda board: predict_board(*board, model))
    connect_four.move(first_player, best_column)
  else:
    move = int(input("Input move: "))
    connect_four.move(second_player, move)

  print(connect_four.board)
  
  if (connect_four.has_won(current_player)):
    print(f"{current_player.name} has won.")
    break
    
  current_player = first_player if current_player is second_player else second_player
