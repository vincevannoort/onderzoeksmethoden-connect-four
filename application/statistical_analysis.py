from connect_four import ConnectFour, Board, Player
from copy import copy, deepcopy
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import keras
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning", "-w", help="amount of winning moves", type=int, default=7)
  parser.add_argument("--blocking", "-b", help="amount of blocking moves", type=int, default=7)
  parser.add_argument("--random", "-r", help="amount of random moves", type=int, default=0)
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", type=str, default='minimax')
  parser.add_argument("--amount", "-a", help="amount of models to create", type=int, default=1)
  args = parser.parse_args()


  print('start loading players')
  players = [Player(f'Column Choice {i}', 'F', 'model_vince', keras.models.load_model(f"../models/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_columnchoice_{i}.h5")) for i in range(args.amount)]
  players += [Player(f'Win Loss {i}', 'F', 'model_jort', keras.models.load_model(f"../models/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_winloss_{i}.h5")) for i in range(args.amount)]
  print(players)
  print('done loading players')

  with open(f'../statistics/tests/random_make_winning_move_states_1000.txt', 'rb') as make_winning_move_states_file:
    make_winning_move_states = pickle.load(make_winning_move_states_file)
  with open(f'../statistics/tests/random_make_blocking_move_states_1000.txt', 'rb') as make_blocking_move_states_file:
    make_blocking_move_states = pickle.load(make_blocking_move_states_file)
  with open(f'../statistics/tests/random_random_board_states_1000.txt', 'rb') as random_board_states_file:
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

    correctness_per_player.append((player.name, player.type, correct_make_winning_move_states, correct_make_blocking_move_states))

correctness_per_player_data = pd.DataFrame(correctness_per_player, columns = ['Player', 'Type', 'Winning moves', 'Blocking moves'])
with open(f'../statistics/dataframes/analysis.pickle', 'wb') as dataframe_file:
  pickle.dump(correctness_per_player_data, dataframe_file)