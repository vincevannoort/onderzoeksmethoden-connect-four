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
    column = connect_four.current_player.get_move(connect_four)
    connect_four.move(column)
    player_that_won = connect_four.has_won()
    if (player_that_won is not None):
      states.append((connect_four.board.get_one_hot_array(connect_four.current_player), column, True))
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
    current_player = connect_four.current_player
    next_states = connect_four.get_next_possible_states(connect_four.get_opponent())
    for (column, state) in next_states:
      if (state.has_won()):
        state_with_block = deepcopy(connect_four)
        state_with_block.move(column)
        states.append((state_with_block.board.get_one_hot_array(current_player), column, True))
        connect_four.reset()
        states_created += 1
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
  connect_four.reset()
  while states_created < states_to_create:
    current_player = connect_four.current_player
    column = connect_four.current_player.get_move(connect_four)
    connect_four.move(column)
    states_without_a_outcome.append((connect_four.board.get_one_hot_array(connect_four.current_player), column, current_player))

    if (connect_four.is_draw() or connect_four.has_won()):
      winning_player = connect_four.has_won()
      states_created += len(states_without_a_outcome)
      states += list(map(lambda state: (state[0], state[1], True if state[2] is winning_player else False), states_without_a_outcome))
      connect_four.reset()
  return states

if __name__ == '__main__':
  states_to_create = 30000
  generate_by_using = 'minimax'
  first_player = Player('first_player', 'F', generate_by_using)
  second_player = Player('second_player', 'S', generate_by_using)
  connect_four = ConnectFour(first_player, second_player)
  make_winning_move_states = generate_ability_to_make_winning_move_states(connect_four, int(states_to_create * 0.35), first_player, second_player)
  make_blocking_move_states = generate_ability_to_block_losing_move_states(connect_four, int(states_to_create * 0.35), first_player, second_player)
  make_random_move_states = generate_random_move_states(connect_four, int(states_to_create * 0.30), first_player, second_player)
  all_states_combined = make_winning_move_states + make_blocking_move_states + make_random_move_states


  with open(f'../data/{generate_by_using}_model_winloss_{states_to_create}.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(all_states_combined, make_winning_move_states_file)

  with open(f'../data/{generate_by_using}_model_columnchoice_{states_to_create}.txt', 'wb') as make_winning_move_states_file:
    pickle.dump(all_states_combined, make_winning_move_states_file)