from connect_four import ConnectFour, Board, Player
from random import choice, shuffle, uniform, randint
from copy import copy, deepcopy
import numpy as np
import pickle
np.set_printoptions(linewidth = 300)

def generate_ability_to_make_winning_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generates board states where the player is only one move away from winning
  """
  states_created = 0
  states = []
  connect_four.reset()
  while states_created < states_to_create:
    current_state = deepcopy(connect_four)
    column_played = connect_four.current_player.get_move(connect_four)
    connect_four.move(column_played)
    player_that_won = connect_four.has_won()
    if (player_that_won is not None):
      states.append((current_state, column_played))
      connect_four.reset()
      states_created += 1
    if (connect_four.is_draw()):
      connect_four.reset()
  return states

def generate_ability_to_block_losing_move_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generates board states where the player is only one move away from losing
  """
  states_created = 0
  states = []
  connect_four.reset()
  while states_created < states_to_create:
    current_state = deepcopy(connect_four)
    next_states = connect_four.get_next_possible_states(connect_four.get_opponent())
    for (column, state) in next_states:
      if (state.has_won()):
        states.append((current_state, column))
        connect_four.reset()
        states_created += 1
        continue
    connect_four.play_move()
    if (connect_four.is_draw() or connect_four.has_won()):
      connect_four.reset()
  return states

def generate_partly_filled_board_states(connect_four: ConnectFour, states_to_create, first_player: Player, second_player: Player):
  """
  generate board with a couple moves already, where the games has not yet be won.
  """
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
  return states

if __name__ == '__main__':
  states_to_create = 10000
  generate_by_using = 'random'
  first_player = Player('first_player', 'F', generate_by_using)
  second_player = Player('second_player', 'S', generate_by_using)
  connect_four = ConnectFour(first_player, second_player)
  make_winning_move_states = generate_ability_to_make_winning_move_states(connect_four, states_to_create, first_player, second_player)
  make_blocking_move_states = generate_ability_to_block_losing_move_states(connect_four, states_to_create, first_player, second_player)
  random_board_states = generate_partly_filled_board_states(connect_four, states_to_create, first_player, second_player)

  with open(f'../statistics/tests/{generate_by_using}_make_winning_move_states_{states_to_create}.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(make_winning_move_states, make_winning_move_states_file)
  with open(f'../statistics/tests/{generate_by_using}_make_blocking_move_states_{states_to_create}.txt', 'wb') as make_blocking_move_states_file:
    pickle.dump(make_blocking_move_states, make_blocking_move_states_file)
  with open(f'../statistics/tests/{generate_by_using}_random_board_states_{states_to_create}.txt', 'wb') as random_board_states_file:
    pickle.dump(random_board_states, random_board_states_file)

  
