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
  parser.add_argument("--winning1", "-w1", help="amount of winning moves", type=int, default=75000)
  parser.add_argument("--blocking1", "-b1", help="amount of blocking moves", type=int, default=75000)
  parser.add_argument("--random1", "-r1", help="amount of random moves", type=int, default=0)
  parser.add_argument("--winning2", "-w2", help="amount of winning moves", type=int, default=50000)
  parser.add_argument("--blocking2", "-b2", help="amount of blocking moves", type=int, default=50000)
  parser.add_argument("--random2", "-r2", help="amount of random moves", type=int, default=50000)
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", type=str, default='random')
  parser.add_argument("--amount", "-a", help="amount of models to create", type=int, default=100)
  args = parser.parse_args()


  print('start loading players')
  random_player = Player(f'random', 'S', 'random')
  players_vince = [Player(f'cc{i}', 'F', 'model_vince', keras.models.load_model(f"../models/{args.type}_t{args.winning1 + args.blocking1 + args.random1}_w{args.winning1}_b{args.blocking1}_r{args.random1}_model_columnchoice_{i}.h5")) for i in range(args.amount)]
  player_vince = deepcopy(players_vince[0])
  player_vince.signature = 'S'
  players_jort = [Player(f'wl{i}', 'F', 'model_jort', keras.models.load_model(f"../models/{args.type}_t{args.winning2 + args.blocking2 + args.random2}_w{args.winning2}_b{args.blocking2}_r{args.random2}_model_winloss_{i}.h5")) for i in range(args.amount)]
  player_jort = deepcopy(players_jort[0])
  player_jort.signature = 'S'
  players = players_vince + players_jort
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
    won_against_random = 0
    draw_against_random = 0
    won_against_opposite = 0
    draw_against_opposite = 0
    steps_taken_on_filled_boards_wins = dict()

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

    for connect_four in random_board_states:
      connect_four_adjusted = deepcopy(connect_four)
      connect_four_adjusted.first_player = player
      connect_four_adjusted.second_player = random_player
      moves_played = 0
      while not(connect_four_adjusted.is_draw() or connect_four_adjusted.has_won()):
        try:
          if connect_four_adjusted.current_player is player:
            moves_played += 1
          connect_four_adjusted.play_move()
        except:
          print(not connect_four_adjusted.is_draw())
          print(connect_four_adjusted.has_won() is not None)
          connect_four_adjusted.board.print_with_colors(player.signature, None)
          break

      if (connect_four_adjusted.is_draw()):
        draw_against_random += 1
      
      if (connect_four_adjusted.has_won() is player):
        won_against_random += 1
        if moves_played in steps_taken_on_filled_boards_wins:
          steps_taken_on_filled_boards_wins[moves_played] += 1
        else:
          steps_taken_on_filled_boards_wins[moves_played] = 1

    
    for connect_four in random_board_states[:100]:
      connect_four_adjusted = deepcopy(connect_four)
      connect_four_adjusted.first_player = player
      connect_four_adjusted.second_player = player_jort if player.type == 'model_vince' else player_vince

      while not(connect_four_adjusted.is_draw() or connect_four_adjusted.has_won()):
        connect_four_adjusted.play_move()

      if (connect_four_adjusted.is_draw()):
        draw_against_opposite += 1

      if (connect_four_adjusted.has_won() is player):
        won_against_opposite += 1

    print(f'done for player: {player.name}')
    correctness_per_player.append((player.name, player.type, correct_make_winning_move_states, correct_make_blocking_move_states, won_against_random, draw_against_random, steps_taken_on_filled_boards_wins, won_against_opposite, draw_against_opposite))

correctness_per_player_data = pd.DataFrame(correctness_per_player, columns = ['Player', 'Type', 'Winning moves', 'Blocking moves', 'Won against random', 'Draw against random', 'Steps to Win', 'Won against opposite', 'Draw against opposite'])
print(correctness_per_player_data)
with open(f'../statistics/dataframes/analysis_{args.amount}.pickle', 'wb') as dataframe_file:
  pickle.dump(correctness_per_player_data, dataframe_file)