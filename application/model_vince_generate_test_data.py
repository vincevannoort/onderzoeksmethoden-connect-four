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
  states_to_create = 2500
  with open(f'../data/data_generated/data_row_classify_connect_four_game_{states_to_create}.txt', 'w') as row_classify_file, open(f'../data/data_generated/data_row_unbiased_classify_connect_four_game_{states_to_create}.txt', 'w') as unbiased_row_classify_file, open(f'../data/data_generated/data_win_classify_connect_four_game_{states_to_create}.txt', 'w') as win_classify_file:
    # file header
    row_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
    win_classify_file.write(f'board representation;signature;column_played;game_ended;bot_won\n')
      
    bot = Player('Bot', 'B')
    alpha_bot = 0.9
    opposite = Player('Opposite', 'O')
    alpha_opposite = 0.9

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

      # initialise_board_amount = randint(0, 10)
      # for _ in range(initialise_board_amount):
      #   connect_four.move(choice(connect_four.board.get_possible_columns()))

      while True:
        current_player = connect_four.current_player
        opposite_player = connect_four.switch_player(connect_four.current_player)
        possible_columns = connect_four.board.get_possible_columns()

        # stop if the game ended in a draw
        if connect_four.is_draw():
          print(f'draw!')
          break

        if current_player is bot:
          # minimax with a chance of alpha_bot %
          if uniform(0, 1) <= alpha_bot:
            mini_max = Minimax(connect_four.board)
            (best_moves, _) = mini_max.best_move(4, connect_four.board, current_player, opposite_player)
            column_to_play = choice(best_moves)
          else:
            column_to_play = choice(possible_columns)
        else:
          # minimax with a chance of opposite_bot %
          if uniform(0, 1) <= alpha_opposite:
            mini_max = Minimax(connect_four.board)
            (best_moves, _) = mini_max.best_move(4, connect_four.board, current_player, opposite_player)
            column_to_play = choice(best_moves)
          else:
            column_to_play = choice(possible_columns)
          
        connect_four.move(column_to_play)
        # print(f'column played: {column_to_play}')

        # setup a dict of states_per_player per player, since we only need the states_per_player from the winning player
        state_after_player_move = StateAfterMove(copy(connect_four.board), current_player, column_to_play, connect_four.has_won())

        # for opposite
        all_states.append(state_after_player_move)

        # for bot
        states_per_player[current_player].append(state_after_player_move)
        local_states_per_player[current_player].append(state_after_player_move)
        # print(f'append state for {current_player.name}')
        
        states_from_player_per_column[current_player][column_to_play].append(state_after_player_move)

        won_player = connect_four.has_won()
        if (won_player is not None):
          for column in states_from_player_per_column[won_player]:
            states_per_column[column] += states_from_player_per_column[won_player][column]

          if (won_player is bot):
            print(f'bot won!')
          else:
            print(f'opposite won!')

          # amount of states per column
          print(f'states per column:')
          for column in states_per_column:
            print(f'{len(states_per_column[column])}', end=' ')
          print()
          connect_four.board.print_with_colors(current_player.signature, opposite_player.signature)

          # amount of states per outcome
          loss_player = connect_four.switch_player(won_player)
          if (won_player is bot):
            states_per_outcome['win'] += local_states_per_player[won_player]
          else:
            states_per_outcome['loss'] += local_states_per_player[loss_player]
          # write files to game for jort
          break
    
    # TODO: add to state which player has won
    minimum_amount_of_outcomes = len(min(list(states_per_outcome.values()), key=len))
    print(f'minimum_amount_of_outcomes: {minimum_amount_of_outcomes}')
    for outcome in states_per_outcome:
      for state in states_per_outcome[outcome][:minimum_amount_of_outcomes]:
        win_classify_file.write(f'{state};{0 if outcome is "loss" else 1}\n')

    for player in states_per_player:
      for state in states_per_player[player]:
          row_classify_file.write(f'{state};\n')
        
    minimum_amount_of_column = len(min(list(states_per_column.values()), key=len))
    print(f'minimum_amount_of_column: {minimum_amount_of_column}')
    column_states_unbiased = []
    for column in states_per_column:
      shuffle(states_per_column[column])
      for state in states_per_column[column][:minimum_amount_of_column]:
          column_states_unbiased.append(state)

    shuffle(column_states_unbiased)
    for state in column_states_unbiased:
      unbiased_row_classify_file.write(f'{state};\n')
