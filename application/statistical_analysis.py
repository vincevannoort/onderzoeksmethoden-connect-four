from connect_four import ConnectFour, Board, Player
from copy import copy, deepcopy
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
# TODO: Let jort compile his model using this 'import keras' instead of 'from tensorflow import keras'
import keras

if __name__ == '__main__':
  states_to_create = 10000
  generate_by_using = 'random'

  random_player = Player('Random', 'F', 'random')
  model_vince_player_500000 = Player('Vince 500000', 'F', 'model_vince', keras.models.load_model(f"../models/trained_with_random/model_vince_500000_moves.h5"))
  model_vince_player_10000 = Player('Vince 10000', 'F', 'model_vince', keras.models.load_model(f"../models/trained_with_random/model_vince_10000_moves.h5"))
  random_opponent = Player('Random', 'S', 'random')
  players = [random_player, model_vince_player_500000, model_vince_player_10000]

  with open(f'../statistics/tests/{generate_by_using}_make_winning_move_states_{states_to_create}.txt', 'rb') as make_winning_move_states_file:
    make_winning_move_states = pickle.load(make_winning_move_states_file)
  with open(f'../statistics/tests/{generate_by_using}_make_blocking_move_states_{states_to_create}.txt', 'rb') as make_blocking_move_states_file:
    make_blocking_move_states = pickle.load(make_blocking_move_states_file)
  with open(f'../statistics/tests/{generate_by_using}_random_board_states_{states_to_create}.txt', 'rb') as random_board_states_file:
    random_board_states = pickle.load(random_board_states_file)
  
  correctness_per_player = []
  for player in players:
    correct_make_winning_move_states = 0
    correct_make_blocking_move_states = 0

    for (connect_four, column) in make_winning_move_states:
      connect_four_adjusted = deepcopy(connect_four)
      connect_four_adjusted.first_player = player
      connect_four_adjusted.current_player = player
      predicted_move = connect_four_adjusted.get_move()
      if (predicted_move == column):
        correct_make_winning_move_states += 1

    for (connect_four, column) in make_blocking_move_states:
      connect_four_adjusted = deepcopy(connect_four)
      connect_four_adjusted.first_player = player
      connect_four_adjusted.current_player = player
      predicted_move = connect_four_adjusted.get_move()
      if (predicted_move == column):
        correct_make_blocking_move_states += 1

    correctness_per_player.append((player.name, correct_make_winning_move_states, correct_make_blocking_move_states))

correctness_per_player_data = pd.DataFrame(correctness_per_player, columns = ['Player', 'Winning moves', 'Blocking moves'])
print(correctness_per_player_data)
plot_winning = sns.barplot(x="Player", y="Winning moves", data=correctness_per_player_data)
plot_winning.set(ylim=(0, states_to_create))
plot_winning.figure.savefig(f"../statistics/images/winning-moves-{states_to_create}.png")
plot_blocking = sns.barplot(x="Player", y="Blocking moves", data=correctness_per_player_data)
plot_blocking.set(ylim=(0, states_to_create))
plot_blocking.figure.savefig(f"../statistics/images/blocking-moves-{states_to_create}.png")
# for (player, correct_make_winning_move_states, correct_make_blocking_move_states) in correctness_per_player:
#   print(f'player: {player}, winning moves: {correct_make_winning_move_states}/{states_to_create}, blocking move: {correct_make_blocking_move_states}/{states_to_create}')

    # print()
    # print(f'player: {player.name}')
    # print(f'correct make winning move states: {correct_make_winning_move_states}/{states_to_create}')
    # print(f'correct make blocking move states: {correct_make_blocking_move_states}/{states_to_create}')
  
