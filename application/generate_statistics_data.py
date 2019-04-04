from connect_four import ConnectFour, Board, Player
from random import choice, shuffle, uniform, randint
from copy import copy, deepcopy
import numpy as np
import sys
import pickle
import argparse
import math

def generate_ability_to_make_winning_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generates board states where the player is only one move away from winning
  """
  states_created = 0
  states = []
  states_to_create_per_column = math.ceil(states_to_create/7)
  print(f'\nstart generate_ability_to_make_winning_move_states, total states: {states_to_create}, states per column: {states_to_create_per_column}')
  states_count = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }
  connect_four.reset()
  while states_created < states_to_create:
    current_state = deepcopy(connect_four)
    column = connect_four.current_player.get_move(connect_four)
    connect_four.move(column)
    player_that_won = connect_four.has_won()
    if (player_that_won is not None):
      if (states_count[column] < states_to_create_per_column):
        states.append((current_state, column))
        states_created += 1
        states_count[column] += 1
        if states_created % 100 is 0:
          print(f'{states_created}/{states_to_create} are created for winning moves, 1: {states_count[0]}, 2: {states_count[1]}, 3: {states_count[2]}, 4: {states_count[3]}, 5: {states_count[4]}, 6: {states_count[5]}, 7: {states_count[6]}')
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
  states_to_create_per_column = math.ceil(states_to_create/7)
  print(f'\nstart generate_ability_to_block_losing_move_states, total states: {states_to_create}, states per column: {states_to_create_per_column}')
  states_count = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 }
  connect_four.reset()
  while states_created < states_to_create:
    current_state = deepcopy(connect_four)
    next_states = connect_four.get_next_possible_states(connect_four.get_opponent())
    for (column, state) in next_states:
      if (state.has_won()):
        if (states_count[column] < states_to_create_per_column):
          states.append((current_state, column))
          states_created += 1
          states_count[column] += 1
          if states_created % 100 is 0:
            print(f'{states_created}/{states_to_create} are created for blocking moves, 1: {states_count[0]}, 2: {states_count[1]}, 3: {states_count[2]}, 4: {states_count[3]}, 5: {states_count[4]}, 6: {states_count[5]}, 7: {states_count[6]}')
        connect_four.reset()
        continue
    connect_four.play_move()
    if (connect_four.is_draw() or connect_four.has_won()):
      connect_four.reset()
  return states

def generate_partly_filled_board_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generate board with a couple moves already, where the games has not yet be won.
  """
  print(f'\nstart generate_partly_filled_board_states, total states: {states_to_create}')
  states_created = 0
  states = []
  connect_four.reset()
  while states_created < states_to_create:
    moves_to_play = randint(8, 22)
    for move in range(moves_to_play):
      connect_four.play_move()
    if (connect_four.is_draw() or connect_four.has_won()):
      connect_four.reset()
    else:
      states.append(deepcopy(connect_four))
      connect_four.reset()
      states_created += 1
      if states_created % 100 is 0:
        print(f'{states_created}/{states_to_create} are created for random filled boards')
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
  parser.add_argument("--type", "-t", help="type of moves generated (either 'minimax' or 'random')", type=str, default='minimax')
  args = parser.parse_args()

  print(f'total states: {args.winning + args.blocking + args.random}')
  print(f'winning moves to create: {args.winning}')
  print(f'blocking moves to create: {args.blocking}')
  print(f'random moves to create: {args.random}')
  print(f'type of moves: {args.type}')

  first_player = Player('first_player', 'F', args.type)
  second_player = Player('second_player', 'S', args.type)
  connect_four = ConnectFour(first_player, second_player)
  
  make_winning_move_states = generate_ability_to_make_winning_move_states(connect_four, args.winning, first_player, second_player)
  make_blocking_move_states = generate_ability_to_block_losing_move_states(connect_four, args.blocking, first_player, second_player)
  make_random_filled_states = generate_partly_filled_board_states(connect_four, args.random, first_player, second_player)

  with open(f'../statistics/tests/{args.type}_make_winning_move_states_{args.winning}.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(make_winning_move_states, make_winning_move_states_file)
  with open(f'../statistics/tests/{args.type}_make_blocking_move_states_{args.blocking}.txt', 'wb') as make_blocking_move_states_file:
    pickle.dump(make_blocking_move_states, make_blocking_move_states_file)
  with open(f'../statistics/tests/{args.type}_random_board_states_{args.random}.txt', 'wb') as random_board_states_file:
    pickle.dump(make_random_filled_states, random_board_states_file)