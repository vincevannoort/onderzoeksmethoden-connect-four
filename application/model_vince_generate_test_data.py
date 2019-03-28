from connect_four import ConnectFour, Board, Player
from random import choice, shuffle, uniform, randint
from copy import copy
import readchar
import os
import numpy as np
from minimax import Minimax

np.set_printoptions(linewidth = 300);

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class StateAfterMove:
  def __init__(self, board: Board, player: Player, column_to_play: int, game_won: bool):
    self.board = board
    self.player = player
    self.columns_to_play = np.zeros(7)
    np.put(self.columns_to_play, column_to_play, 1)
    self.game_won = game_won

  def __str__(self):
    return f'{np.array2string(np.array(self.board.get_one_hot_array(self.player)))};{self.player.signature};{np.array2string(self.columns_to_play)};{True if self.game_won else False}'

if __name__ == '__main__':
  # settings
  states_to_create = 1
  type = 'minimax' # random or minimax

  # generator
  with open(f'../data/{type}/data_unbiased_column_states_connect_four_game_{states_to_create}.txt', 'w') as unbiased_column_states_file, open(f'../data/{type}/data_unbiased_winloss_states_connect_four_game_{states_to_create}.txt', 'w') as unbiased_winloss_states_file:
    # file header
    unbiased_column_states_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
    unbiased_winloss_states_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
      
    bot = Player('Bot', 'B', type)
    opposite = Player('Opposite', 'O', type)

    # states
    all_states = list()
    states_per_player = dict()
    states_per_player_per_column = dict()
    states_per_column = dict()
    states_per_outcome = dict()

    # initialise dicts to not check if in dict
    states_per_outcome['win'] = []
    states_per_outcome['loss'] = []
    states_per_player[bot] = []
    states_per_player[opposite] = []
    states_per_player_per_column[bot] = dict()
    states_per_player_per_column[opposite] = dict()
    for i in range(7):
      states_per_player_per_column[bot][i] = []
      states_per_player_per_column[opposite][i] = []
      states_per_column[i] = []

    while (len(min(list(states_per_column.values()), key=len)) < states_to_create):
      connect_four = ConnectFour(bot, opposite)
      local_states_per_player = dict()
      local_states_per_player[bot] = []
      local_states_per_player[opposite] = []
      states_from_player_per_column = dict()
      states_from_player_per_column[bot] = dict()
      states_from_player_per_column[opposite] = dict()
      for i in range(7):
        states_from_player_per_column[bot][i] = []
        states_from_player_per_column[opposite][i] = []

      while True:
        current_player = connect_four.current_player
        opposite_player = connect_four.switch_player(connect_four.current_player)
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if connect_four.is_draw():
          print(f'draw!')
          break


        column_to_play = connect_four.current_player.get_move(connect_four)
        connect_four.move(column_to_play)
        state_after_player_move = StateAfterMove(copy(connect_four.board), current_player, column_to_play, connect_four.has_won())

        all_states.append(state_after_player_move)
        states_per_player[current_player].append(state_after_player_move)
        local_states_per_player[current_player].append(state_after_player_move)
        states_from_player_per_column[current_player][column_to_play].append(state_after_player_move)

        won_player = connect_four.has_won()
        loss_player = connect_four.switch_player(won_player)

        if (won_player is not None):
          print(f'{won_player.name} won!')
          for column in states_from_player_per_column[won_player]:
            states_per_column[column] += states_from_player_per_column[won_player][column]

          print(f'states per column:')
          for column in states_per_column:
            print(f'{len(states_per_column[column])}', end=' ')
          print()
          connect_four.board.print_with_colors(current_player.signature, opposite_player.signature)

          if (won_player is bot):
            states_per_outcome['win'] += local_states_per_player[won_player]
          else:
            states_per_outcome['loss'] += local_states_per_player[loss_player]

          # game finished
          break

    # win / loss - same amount of states
    minimum_amount_of_outcomes = len(min(list(states_per_outcome.values()), key=len))
    print(f'minimum_amount_of_outcomes: {minimum_amount_of_outcomes}')

    for outcome in states_per_outcome:
      for state in states_per_outcome[outcome][:minimum_amount_of_outcomes]:
        unbiased_winloss_states_file.write(f'{state};{0 if outcome is "loss" else 1}\n')
        
    # every column - same amount of states
    minimum_amount_of_column = len(min(list(states_per_column.values()), key=len))
    print(f'minimum_amount_of_column: {minimum_amount_of_column}')

    for column in states_per_column:
      shuffle(states_per_column[column])
      for state in states_per_column[column][:minimum_amount_of_column]:
          unbiased_column_states_file.write(f'{state};\n')