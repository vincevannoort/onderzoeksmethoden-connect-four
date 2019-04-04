from connect_four import ConnectFour, Board, Player
from random import choice, shuffle, uniform, randint
from copy import copy, deepcopy
import numpy as np
import sys
import pickle
import argparse

def generate_ability_to_make_winning_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generates board states where the player is only one move away from winning
  """
  states_created = 0
  states = []
  states_to_create_per_column = int((states_to_create / 7))
  states_count = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }
  connect_four.reset()
  while states_created < states_to_create:
    column = connect_four.current_player.get_move(connect_four)
    connect_four.move(column)
    player_that_won = connect_four.has_won()
    if (player_that_won is not None):
      if (states_count[column] < states_to_create_per_column):
        states.append((connect_four.board.get_one_hot_array(connect_four.current_player), column, True))
        states_created += 1
        states_count[column] += 1
      connect_four.reset()
    if (connect_four.is_draw()):
      connect_four.reset()
  return states

def generate_ability_to_block_losing_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generates board states where the player is only one move away from losing
  """
  states_created = 0
  states = []
  states_to_create_per_column = int((states_to_create / 7))
  states_count = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }
  connect_four.reset()
  while states_created < states_to_create:
    current_player = connect_four.current_player
    next_states = connect_four.get_next_possible_states(connect_four.get_opponent())
    for (column, state) in next_states:
      if (state.has_won()):
        if (states_count[column] < states_to_create_per_column):
          state_with_block = deepcopy(connect_four)
          state_with_block.move(column)
          states.append((state_with_block.board.get_one_hot_array(current_player), column, True))
          states_created += 1
          states_count[column] += 1
        connect_four.reset()
        continue
    connect_four.play_move()
    if (connect_four.is_draw() or connect_four.has_won()):
      connect_four.reset()
  return states

def generate_random_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generate board with a couple moves already, where the games has not yet be won.
  """
  states_created = 0
  states = []
  states_without_a_outcome = []
  states_to_create_per_column = int((states_to_create / 7))
  states_count = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }
  connect_four.reset()
  while states_created < states_to_create:
    current_player = connect_four.current_player
    column = connect_four.current_player.get_move(connect_four)
    connect_four.move(column)
    states_without_a_outcome.append((connect_four.board.get_one_hot_array(connect_four.current_player), column, current_player))

    if (connect_four.is_draw() or connect_four.has_won()):
      winning_player = connect_four.has_won()
      for (board, column, player) in states_without_a_outcome:
        if (states_count[column] < states_to_create_per_column):
          states.append((state_with_block.board.get_one_hot_array(current_player), column, True if player is winning_player else False))
          states_created += 1
          states_count[column] += 1
      states_without_a_outcome = []
      connect_four.reset()
  return states

if __name__ == '__main__':
  """
  example: python3.6 generate_training_data.py -w 7 -b 7 -r 0 -t minimax
  description: generate data with 7 winning moves, 7 blocking moves and 0 random moves using minimax
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("--winning", "-w", help="amount of winning moves", type=int, default=7)
  parser.add_argument("--blocking", "-b", help="amount of blocking moves", type=int, default=7)
  parser.add_argument("--random", "-r", help="amount of random moves", type=int, default=0)
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", default='minimax')
  args = parser.parse_args()

  print(f'total states: {args.winning + args.blocking + args.random}')
  print(f'winning moves to create: {args.winning}')
  print(f'blocking moves to create: {args.blocking}')
  print(f'random moves to create: {args.random}')
  print(f'type of moves: {args.type}')

  states_to_create = 14
  generate_by_using = 'minimax'
  first_player = Player('first_player', 'F', generate_by_using)
  second_player = Player('second_player', 'S', generate_by_using)
  connect_four = ConnectFour(first_player, second_player)
  make_winning_move_states = generate_ability_to_make_winning_move_states(connect_four, args.winning, first_player, second_player)
  make_blocking_move_states = generate_ability_to_block_losing_move_states(connect_four, args.blocking, first_player, second_player)
  make_random_move_states = generate_random_move_states(connect_four, args.random, first_player, second_player)
  all_states_combined = make_winning_move_states + make_blocking_move_states + make_random_move_states

  with open(f'../data/{args.type}/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_winloss.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(all_states_combined, make_winning_move_states_file)

  with open(f'../data/{args.type}/{args.type}_t{args.winning + args.blocking + args.random}_w{args.winning}_b{args.blocking}_r{args.random}_model_columnchoice.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(all_states_combined, make_winning_move_states_file)